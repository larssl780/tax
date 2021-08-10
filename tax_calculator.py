"""

This is the base class for all the jurisdictions

==attributes that the inheriting class needs to implement==

* payload (to pass to the web request)
* tax_url
* tax()
* official_tax()
* parsed_official_response - parse the response from the web request into a dataframe or such-like - this will then form the basis for the official_tax



==files needed==
* [jurisdiction]_test_cases.ini
* eg. test_norwegian_tax.py (test-file that runs through the cases specified in the .ini file)


==common parameter file==

* taxes.ini (this contains all the constants for the various jurisdictions and tax years)


"""
import os
from functools import lru_cache
import configparser
import numpy as np
from tqdm import tqdm
import requests
import pandas as pd
import tax_utils as tut


class TaxCalculator:
    def __init__(self, jurisdiction='n/a', case_idx=None,
                 tax_url='', tax_year=None):
        # TODO: this is fragile to define in two places, work out later
        self._jurisdiction = jurisdiction
        self._case_idx = case_idx
        case_file = '%s_test_cases.ini' % jurisdiction.lower()
        self._case_file = case_file
        self._tax_url = tax_url
        self._tax_year = tax_year
        self._case_numbers = sorted(map(int, list(set(self.case_file_data.keys()) - set(['DEFAULT']))))
        if self._case_idx is not None:
            inputs = tut.inputs_for_case_number(
                self._case_idx, case_file=case_file, include_correct_tax=False)

            if inputs is not None:
                for field, val in inputs.items():
                    if hasattr(self, field):
                        # print('%s: %s'%(field, str(val)))
                        setattr(self, field, val)

        self._headers = {'Accept': 'application/json, text/plain, */*',
                         'Accept-Language': 'en-US,en;q=0.5',
                         'Cache-Control': 'no-cache',
                         'Connection': 'keep-alive',
                         'DNT': '1',
                         'Pragma': 'no-cache',
                         'Referer': 'http://stats.nba.com/',
                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
                         'content-type': 'application/json',
                         'x-nba-stats-origin': 'stats',
                         'x-nba-stats-token': 'true'}

    @property
    def case_idx(self):
        return self._case_idx

    @case_idx.setter
    def case_idx(self, value):
        # print("Trying to set case_idx to %s" % value)
        if value is not None:
            # self._case_idx = value
            self.__init__(case_idx=value)
            inputs = tut.inputs_for_case_number(
                value, case_file=self._case_file, include_correct_tax=False)

            for field, val in inputs.items():
                if hasattr(self, field):
                    # print('%s: %s'%(field, str(val)))
                    setattr(self, field, val)

    @property
    def headers(self):
        return self._headers

    @property
    def tax_url(self):
        return self._tax_url

    @tax_url.setter
    def tax_url(self, value):
        self._tax_url = value

    @property
    def jurisdiction(self):
        return self._jurisdiction

    @property
    def tax_year(self):
        return self._tax_year

    @tax_year.setter
    def tax_year(self, value):
        self._tax_year = value

    @property
    def tax_parameters(self):
        return tut.tax_parameters(
            jurisdiction=self.jurisdiction, tax_year=self.tax_year)

    @lru_cache(maxsize=None)
    def parameter(self, pname='', divisor=1):
        ret_val = self.tax_parameters.getfloat(pname)

        if ret_val is None:
            raise Exception("No such parameter ('%s')!" % (pname))
        return ret_val / divisor

    @property
    def case_file(self):
        # filename = '%s_test_cases.ini'%self.jurisdiction
        assert os.path.exists(
            self._case_file), "'%s' doesn't exist!" % self._case_file
        return self._case_file

    @property
    def case_file_data(self):
        cases = configparser.ConfigParser()
        cases.read(self.case_file)
        return dict(cases)

    @property
    def case_numbers(self):
        return self._case_numbers
    def tax(self):
        return 0

    def official_tax(self, session=None, refresh=False):
        return 0

    def config_tax(self):
        return tut.config_tax(self.case_idx, case_file=self.case_file)

    def tax_ties_with_config(
            self, do_all=False, atol=1e-8, rtol=1e-5, verbose=False):
        """
        Check that the computed tax ties with the tax stored in the config file
        """
        if not do_all:
            return np.allclose(self.config_tax(), self.tax())

        case_numbers = tut.all_case_numbers(case_file=self.case_file)
        # print(case_numbers)
        observed = []
        expected = []
        for case_idx in tqdm(case_numbers):
            # print("working on case number %d" % case_idx)

            setattr(self, 'case_idx', case_idx)
            # self.case_idx =
            # pdb.set_trace()
            # print("After setting case idx, it's now %d"%self.case_idx)
            observed.append(self.tax())
            expected.append(self.config_tax())

        # pdb.set_trace()
        if verbose:
            print("==Expected==")
            print(expected)
            print("==Observed==")
            print(observed)
        if not np.allclose(observed, expected, atol=atol, rtol=rtol):
            exp = np.array(expected)
            obs = np.array(observed)
            good_idx = np.abs(exp - obs) <= (atol + rtol * np.abs(obs))
            # pdb.set_trace()
            bad_idx = np.where(~good_idx)[0]
            print("Some checks failed!")
            return bad_idx

        print("All tests passed!")

        return True

    def tax_ties_with_web(self, do_all=False, atol=1e-8,
                          rtol=1e-5, refresh=False, verbose=False):
        """
        this will (obviously hit the tax authority web server)
        """
        if not do_all:
            return np.allclose(self.official_tax(), self.tax())

        case_numbers = tut.all_case_numbers(case_file=self.case_file)
        observed = []
        expected = []
        with requests.Session() as sesh:
            for case_idx in tqdm(case_numbers):
                setattr(self, 'case_idx', case_idx)
                observed.append(self.tax())
                expected.append(
                    self.official_tax(session=sesh, refresh=refresh))
                # if verbose:

        if not np.allclose(observed, expected, atol=atol, rtol=rtol):
            exp = np.array(expected)
            obs = np.array(observed)

            good_idx = np.abs(exp - obs) <= (atol + rtol * np.abs(obs))
            bad_idx = np.where(~good_idx)[0]

            print("Some checks failed!")
            if verbose:
                out = []
                for idx in bad_idx:
                    out.append([idx, exp[idx], obs[idx]])
                print(pd.DataFrame(out, columns=['case', 'exp', 'obs']))
            return bad_idx
        print("All tests passed!")
        if verbose:
            print("==Expected==")
            print(expected)
            print("==Observed==")
            print(observed)
        return True

    def payload(self):
        """
        dummy that will be filled in by inheriting class
        """
        return None

    def query_web_for_tax_results(self, refresh=False, session=None):
        """
        post the request to xxx

        does this work, asking the child class to provide the payload?
        """
        if session is None:
            res = tut.get_request(
                self.tax_url,
                method='post',
                payload_=self.payload(),
                headers_=self.headers,
                refresh=refresh)
        else:
            res = tut.post_request_from_session(
                url=self.tax_url,
                payload_=self.payload(),
                headers=self.headers,
                refresh=refresh,
                session=session)
        return res


    
    def dump_config_answers(self):
        """
        for excel file
        """

        out = []
        for case_idx in self.case_numbers:
            # input_struct = {}
            for k, value in self.case_file_data['%d' % case_idx].items():
                if k == 'tax':
                    out.append([case_idx, value])

        return pd.DataFrame(out, columns=['Case', 'Skatt'])

    def __repr__(self):
        return '%s - %d' % (self.jurisdiction, self.case_idx)
