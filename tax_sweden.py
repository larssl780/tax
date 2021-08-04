
"""
query() hits skatteverket's homepage
query takes payload argument
parse_response calls query
read_tax uses parse_response


The class can have its parameters set manually, but basic use-case is to have it driven off
a config file (se_test_cases.ini) with various scenarios together with what the correct tax should be (manually maintained).
There's also (perhaps more useful) to automatically query skatteverket to check what the correc tax should be.
This can help us capture whenever tax rules change.
The tests are run daily on github via test_swedish_tax.py


"""
import pdb
import copy
import datetime
from functools import lru_cache
from tqdm import tqdm
import numpy as np
import pandas as pd
import requests
import tax_utils as tut


class SwedishTax:
    """
    to facilitate easy input

    """

    def __init__(self, salary=0, birth_year=1978, tax_year=None, listed_funds_and_shares_profit=0, listed_funds_and_shares_loss=0, int_inc_tax_withheld=0, int_inc_tax_not_withheld=0, rental_income=0, unlisted_funds_profit=0, sale_private_property_profit=0,
                 sale_private_property_loss=0, interest_expense=0, municipality='Partille', unlisted_funds_loss=0, standard_income=0, sale_commercial_property_profit=0, sale_commercial_property_loss=0, investor_deduction=0,
                 qualified_shares_profit_loss=0, unlisted_shares_profit_loss=0, case_idx=None):

        self._salary = salary
        self._birth_year = birth_year
        self._tax_year = tax_year
        self._listed_funds_and_shares_profit = listed_funds_and_shares_profit
        self._listed_funds_and_shares_loss = listed_funds_and_shares_loss
        self._int_inc_tax_withheld = int_inc_tax_withheld
        self._int_inc_tax_not_withheld = int_inc_tax_not_withheld
        self._rental_income = rental_income
        self._unlisted_funds_profit = unlisted_funds_profit
        self._sale_private_property_profit = sale_private_property_profit
        self._sale_private_property_loss = sale_private_property_loss
        self._interest_expense = interest_expense
        self._municipality = municipality
        self._unlisted_funds_loss = unlisted_funds_loss
        self._standard_income = standard_income
        self._sale_commercial_property_profit = sale_commercial_property_profit
        self._sale_commercial_property_loss = sale_commercial_property_loss
        self._investor_deduction = investor_deduction
        self._qualified_shares_profit_loss = qualified_shares_profit_loss
        self._unlisted_shares_profit_loss = unlisted_shares_profit_loss
        self._tax_breakdown_dict = {}

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

        self._tax_url = "https://app.skatteverket.se/gateway-skut-skatteutrakning/skatteberakning-fysisk/rakna-ut-skatt"

        self._case_file = 'se_test_cases.ini'

        self._income_deduction = None
        self._job_deduction = None

        if case_idx is not None:
            self._case_idx = case_idx
            inputs = tut.inputs_for_case_number(
                case_idx, case_file=self._case_file, include_correct_tax=False)

            for field, val in inputs.items():
                if hasattr(self, field):
                    # print('%s: %s'%(field, str(val)))
                    setattr(self, field, val)

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        assert isinstance(value, dict), "headers should be a dict"
        self._headers = value

    @property
    def tax_url(self):
        return self._tax_url

    @tax_url.setter
    def tax_url(self, value):
        assert isinstance(value, str), "URL needs to be a string"
        self._tax_url = value

    @property
    def tax_breakdown_dict(self):
        return self._tax_breakdown_dict

    @tax_breakdown_dict.setter
    def tax_breakdown_dict(self, value):
        assert isinstance(value, dict), "tax breakdown dict should be a dict"
        self._tax_breakdown_dict = value

    @property
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        self._birth_year = value

    @property
    def tax_year(self):
        if self._tax_year is None:
            return pd.to_datetime('today').year
        return self._tax_year

    @property
    def listed_funds_and_shares_profit(self):

        return self._listed_funds_and_shares_profit

    @listed_funds_and_shares_profit.setter
    def listed_funds_and_shares_profit(self, value):
        assert tut.value_is_numeric_type(
            value), "listed_funds_and_shares_profit should be a number!"
        self._listed_funds_and_shares_profit = value

    @property
    def listed_funds_and_shares_loss(self):
        return self._listed_funds_and_shares_loss

    @listed_funds_and_shares_loss.setter
    def listed_funds_and_shares_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "listed_funds_and_shares_loss should be a number!"
        self._listed_funds_and_shares_loss = value

    @property
    def int_inc_tax_withheld(self):
        return self._int_inc_tax_withheld

    @int_inc_tax_withheld.setter
    def int_inc_tax_withheld(self, value):
        assert tut.value_is_numeric_type(
            value), "int_inc_tax_withheld should be a number!"
        self._int_inc_tax_withheld = value

    @property
    def int_inc_tax_not_withheld(self):
        return self._int_inc_tax_not_withheld

    @int_inc_tax_not_withheld.setter
    def int_inc_tax_not_withheld(self, value):
        assert tut.value_is_numeric_type(
            value), "int_inc_tax_not_withheld should be a number!"
        self._int_inc_tax_not_withheld = value

    @property
    def rental_income(self):
        return self._rental_income

    @rental_income.setter
    def rental_income(self, value):
        assert tut.value_is_numeric_type(
            value), "rental_income should be a number!"
        self._rental_income = value

    @property
    def unlisted_funds_profit(self):
        return self._unlisted_funds_profit

    @unlisted_funds_profit.setter
    def unlisted_funds_profit(self, value):
        assert tut.value_is_numeric_type(
            value), "unlisted_funds_profit should be a number!"
        self._unlisted_funds_profit = value

    @property
    def sale_private_property_profit(self):
        return self._sale_private_property_profit

    @sale_private_property_profit.setter
    def sale_private_property_profit(self, value):
        assert tut.value_is_numeric_type(
            value), "sale_private_property_profit should be a number!"
        self._sale_private_property_profit = value

    @property
    def sale_private_property_loss(self):
        return self._sale_private_property_loss

    @sale_private_property_loss.setter
    def sale_private_property_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "sale_private_property_loss should be a number!"
        self._sale_private_property_loss = value

    @property
    def interest_expense(self):
        return self._interest_expense

    @interest_expense.setter
    def interest_expense(self, value):
        assert tut.value_is_numeric_type(
            value), "interest_expense should be a number!"
        self._interest_expense = value

    @property
    def municipality(self):
        return self._municipality

    @municipality.setter
    def municipality(self, value):
        self._municipality = value

    @property
    def unlisted_funds_loss(self):
        return self._unlisted_funds_loss

    @unlisted_funds_loss.setter
    def unlisted_funds_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "unlisted_funds_loss should be a number!"
        self._unlisted_funds_loss = value

    @property
    def standard_income(self):
        return self._standard_income

    @standard_income.setter
    def standard_income(self, value):
        assert tut.value_is_numeric_type(
            value), "standard_income should be a number!"
        self._standard_income = value

    @property
    def sale_commercial_property_profit(self):
        return self._sale_commercial_property_profit

    @sale_commercial_property_profit.setter
    def sale_commercial_property_profit(self, value):
        assert tut.value_is_numeric_type(
            value), "sale_commercial_property_profit should be a number!"
        self._sale_commercial_property_profit = value

    @property
    def sale_commercial_property_loss(self):
        return self._sale_commercial_property_loss

    @sale_commercial_property_loss.setter
    def sale_commercial_property_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "sale_commercial_property_loss should be a number!"
        self._sale_commercial_property_loss = value

    @property
    def investor_deduction(self):
        return self._investor_deduction

    @investor_deduction.setter
    def investor_deduction(self, value):
        assert tut.value_is_numeric_type(
            value), "investor_deduction should be a number!"
        if value > self.parameter('max_investor_deduction'):
            raise Exception(
                "The max investor_deduction (investeraravdrag) is %d" %
                self.parameter('max_investor_deduction'))
        self._investor_deduction = value

    @property
    def qualified_shares_profit_loss(self):
        return self._qualified_shares_profit_loss

    @qualified_shares_profit_loss.setter
    def qualified_shares_profit_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "qualified_shares_profit_loss should be a number!"
        self._qualified_shares_profit_loss = value

    @property
    def unlisted_shares_profit_loss(self):
        return self._unlisted_shares_profit_loss

    @unlisted_shares_profit_loss.setter
    def unlisted_shares_profit_loss(self, value):
        assert tut.value_is_numeric_type(
            value), "unlisted_shares_profit_loss should be a number!"
        self._unlisted_shares_profit_loss = value

    @property
    def case_idx(self):
        return self._case_idx

    @case_idx.setter
    def case_idx(self, value):
        # print("Trying to set case_idx to %s" % value)
        if value is not None:
            self._case_idx = value
            self.__init__()
            inputs = tut.inputs_for_case_number(
                value, case_file=self._case_file, include_correct_tax=False)

            for field, val in inputs.items():
                if hasattr(self, field):
                    # print('%s: %s'%(field, str(val)))
                    setattr(self, field, val)
        # self._case_idx = value

    @property
    def tax_parameters(self):
        return tut.tax_parameters(jurisdiction='SE', tax_year=self.tax_year)

    @lru_cache(maxsize=None)
    def parameter(self, pname='', divisor=1):
        # print("Getting parameter = '%s'"%pname)
        # if not len(pname):
        #   pdb.set_trace()
        return self.tax_parameters.getfloat(pname) / divisor

    @property
    def case_file(self):
        return self._case_file

    @property
    def income_deduction(self):
        if self._income_deduction is None:
            return np.floor(min(max(self.parameter('skattereduktionForvarvsinkomst_procent', 100) * (self.taxable_income() -
                                                                                                     self.parameter('skattereduktionForvarvsinkomst_golv')), 0), self.parameter('skattereduktionForvarvsinkomst_tak')))
        return self._income_deduction

    @income_deduction.setter
    def income_deduction(self, value):
        # assert isinstance(value, float), "Income deduction needs to be float, not %s"%(str(type(value)))
        self._income_deduction = value

    @property
    def job_deduction(self):
        if self._job_deduction is None:
            return self.jobbskatteavdrag()
        return self._job_deduction

    @job_deduction.setter
    def job_deduction(self, value):
        self._job_deduction = value

    @property
    def lower_limit_for_income_tax(self):
        return np.floor(self.parameter('pris_bas_belopp') *
                        self.parameter('skatt_lagre_inkomst_multipel'))

    @property
    def funeral_rate(self):
        if self.municipality == 'Stockholm':
            return 0.065 / 100
        if self.municipality == 'Tranas':
            return 0.24 / 100

        return 0.253 / 100

    @property
    def funeral_fee(self):
        return np.floor(self.funeral_rate * self.taxable_income())

    def old_age_limit_year(self):
        """
        over a certain age, the various rates etc change
        """
        old_age_cutoff = datetime.date(
            self.tax_year, 1, 1) - pd.DateOffset(years=66)
        return old_age_cutoff.year

    def qualified_shares_income_taxation(self):
        """
        returns the extra income we need to add and then the extra capital_income we need to add
        Detta ar blankett K10
        """
        extra_unlisted_funds_loss = 0
        extra_salary = 0
        extra_listed_funds_and_shares_profit = 0

        if abs(self.qualified_shares_profit_loss) > 1e-4:

            if self.qualified_shares_profit_loss < 0:
                # this is point 3.4b in the K10 form:
                extra_unlisted_funds_loss += abs(
                    self.qualified_shares_profit_loss) * 2 / 3
            else:
                # we assume no dividend, so we end up at 3.7b of K10:
                # pdb.set_trace()
                # qualified_shares_income_limit =
                # upper_limit_employment_income =
                qualified_profit = max(
                    self.qualified_shares_profit_loss -
                    self.parameter('gransbelopp_forenkling'),
                    0)
                employment_income = min(
                    qualified_profit,
                    self.parameter('upper_limit_employment_income'))
                # gets taxed as employment income
                extra_salary += employment_income
                # residual = qualified_profit - employment_income
                # work out what should be tax as capital income (this we'll add to
                # the listed_funds_and_share_profit):
                capital_gain = max(
                    self.qualified_shares_profit_loss - employment_income, 0)
                # assume we don't have any "sparat utdelningsutrymme", the belowe
                # captures points 3.12-3.13 in the K10 form:
                to_be_taxed_as_capital = 0
                if self.parameter('gransbelopp_forenkling') > capital_gain:
                    to_be_taxed_as_capital += (2 / 3) * capital_gain
                else:
                    to_be_taxed_as_capital += (2 / 3) * \
                        self.parameter('gransbelopp_forenkling')
                to_be_taxed_as_capital += max(capital_gain -
                                              self.parameter('gransbelopp_forenkling'), 0)
                extra_listed_funds_and_shares_profit += to_be_taxed_as_capital

        return extra_salary, extra_listed_funds_and_shares_profit, extra_unlisted_funds_loss

    def adjusted_attribute_value(self, attribute='salary'):
        """
        returns the extra income we need to add and then the extra capital_income we need to add
        Detta ar blankett K10

        If you earn money through your company, some of that money could be reclassified as employment income etc, 
        so we need this extra calculation step.
        """
        extra_unlisted_funds_loss = 0
        extra_salary = 0
        extra_listed_funds_and_shares_profit = 0
        extra_listed_loss = 0

        if abs(self.qualified_shares_profit_loss) > 1e-4:

            if self.qualified_shares_profit_loss < 0:
                # this is point 3.4b in the K10 form:
                extra_unlisted_funds_loss += abs(
                    self.qualified_shares_profit_loss) * 2 / 3
            else:
                # we assume no dividend, so we end up at 3.7b of K10:
                # pdb.set_trace()
                # qualified_shares_income_limit =
                # upper_limit_employment_income =
                qualified_profit = max(
                    self.qualified_shares_profit_loss -
                    self.parameter('gransbelopp_forenkling'),
                    0)
                employment_income = min(
                    qualified_profit,
                    self.parameter('upper_limit_employment_income'))
                # gets taxed as employment income
                extra_salary += employment_income
                # residual = qualified_profit - employment_income
                # work out what should be tax as capital income (this we'll add to
                # the listed_funds_and_share_profit):
                capital_gain = max(
                    self.qualified_shares_profit_loss - employment_income, 0)
                # assume we don't have any "sparat utdelningsutrymme", the belowe
                # captures points 3.12-3.13 in the K10 form:
                to_be_taxed_as_capital = 0
                if self.parameter('gransbelopp_forenkling') > capital_gain:
                    to_be_taxed_as_capital += (2 / 3) * capital_gain
                else:
                    to_be_taxed_as_capital += (2 / 3) * \
                        self.parameter('gransbelopp_forenkling')
                to_be_taxed_as_capital += max(capital_gain -
                                              self.parameter('gransbelopp_forenkling'), 0)
                extra_listed_funds_and_shares_profit += to_be_taxed_as_capital

        # return extra_salary, extra_listed_funds_and_shares_profit,
        # extra_unlisted_funds_loss

        if self.unlisted_shares_profit_loss < 0:
            extra_listed_loss += (5 / 6) * \
                abs(self.unlisted_shares_profit_loss)
        else:
            extra_listed_funds_and_shares_profit += (
                5 / 6) * self.unlisted_shares_profit_loss
        if attribute == 'salary':
            return self.salary + extra_salary
        if attribute == 'listed_funds_and_shares_profit':
            return self.listed_funds_and_shares_profit + \
                extra_listed_funds_and_shares_profit
        if attribute == 'unlisted_funds_loss':
            return self.unlisted_funds_loss + extra_unlisted_funds_loss
        if attribute == 'listed_funds_and_shares_loss':
            return self.listed_funds_and_shares_loss + extra_listed_loss
        raise Exception("Attributed == '%s' not handled!" % attribute)

    def unqualified_shares_income_taxation(self):
        """
        returns the extra income we need to add and then the extra capital_income we need to add
        Detta ar blankett K12
        Om vinst, 5/6 * belopp till 7.4 (where would we add it in code?) Profit should go to listed_funds_and_shares_profit
        Om förlust 5/6 * belopp till 8.3 goes to listed_loss
        """

        extra_listed_funds_and_shares_profit = 0
        extra_listed_loss = 0

        if self.unlisted_shares_profit_loss < 0:
            extra_listed_loss += (5 / 6) * \
                abs(self.unlisted_shares_profit_loss)
        else:
            extra_listed_funds_and_shares_profit += (
                5 / 6) * self.unlisted_shares_profit_loss

        return extra_listed_funds_and_shares_profit, extra_listed_loss

    def _basic_deduction_base_case(self):

        # TODO: Add these as parameters, will change
        if self.salary_rounded() <= self.parameter('ga_m1') * self.parameter('pris_bas_belopp'):
            # A in s/s
            return 0.423 * self.parameter('pris_bas_belopp')
        if self.salary_rounded() <= self.parameter('ga_m2') * self.parameter('pris_bas_belopp'):
            # B in s/s
            return 0.423 * self.parameter('pris_bas_belopp') + 0.2 * (
                self.salary_rounded() - self.parameter('ga_m1') * self.parameter('pris_bas_belopp'))
        if self.salary_rounded() <= self.parameter('ga_m3') * self.parameter('pris_bas_belopp'):
            # C in s/s
            return 0.77 * self.parameter('pris_bas_belopp')
        if self.salary_rounded() <= self.parameter('ga_m4') * self.parameter('pris_bas_belopp'):
            return 0.77 * self.parameter('pris_bas_belopp') - 0.1 * (
                self.salary_rounded() - self.parameter('ga_m3') * self.parameter('pris_bas_belopp'))

            # E in the spreadsheet
        return 0.293 * self.parameter('pris_bas_belopp')

    def _basic_deduction_extra(self):
        # extra = 0
        if self.birth_year <= self.old_age_limit_year():
            if self.salary_rounded() <= self.parameter('ega_m1') * self.parameter('pris_bas_belopp'):
                return 0.687 * self.parameter('pris_bas_belopp')
            if self.salary_rounded() <= self.parameter('ega_m2') * self.parameter('pris_bas_belopp'):
                return 0.885 * \
                    self.parameter('pris_bas_belopp') - \
                    0.2 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m3') * self.parameter('pris_bas_belopp'):
                return 0.6 * \
                    self.parameter('pris_bas_belopp') + \
                    0.057 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m4') * self.parameter('pris_bas_belopp'):
                return 0.34 * \
                    self.parameter('pris_bas_belopp') - \
                    0.169 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m5') * self.parameter('pris_bas_belopp'):
                return 0.44 * self.salary_rounded() - 0.48 * self.parameter('pris_bas_belopp')

            if self.salary_rounded() <= self.parameter('ega_m6') * self.parameter('pris_bas_belopp'):
                return 0.207 * \
                    self.parameter('pris_bas_belopp') + \
                    0.228 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m7') * self.parameter('pris_bas_belopp'):
                return 0.995 * \
                    self.parameter('pris_bas_belopp') + \
                    0.128 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m8') * self.parameter('pris_bas_belopp'):
                return 2.029 * self.parameter('pris_bas_belopp')
            if self.salary_rounded() <= self.parameter('ega_m9') * self.parameter('pris_bas_belopp'):
                return 9.023 * \
                    self.parameter('pris_bas_belopp') - \
                    0.62 * self.salary_rounded()
            if self.salary_rounded() <= self.parameter('ega_m10') * self.parameter('pris_bas_belopp'):
                # extra = 1.654 * basbelopp - 0.045 * salary
                return 1.253 * self.parameter('pris_bas_belopp')
            if self.salary_rounded() <= self.parameter('ega_m11') * self.parameter('pris_bas_belopp'):
                return 2.03 * \
                    self.parameter('pris_bas_belopp') - \
                    0.0574 * self.salary_rounded()

            return 0.215 * self.parameter('pris_bas_belopp')
        return 0

    def basic_deduction(self):
        """
        grundavdrag

        the extra for 65+ is described here:
        https://www.regeringen.se/4a6f30/contentassets/23ff11528fc54f918a144c067b44672e/ytterligare-skattesankningar-for-personer-over-65-ar.pdf
        """
        
        return min(np.ceil((self._basic_deduction_base_case() + self._basic_deduction_extra()) / 100) * 100, self.salary_rounded())

    def _jobbskatteavdrag_older(self):
        """
        older people have a different deduction than working-age people:
        """
        # TODO: get limits and rates from params file
        if self.birth_year > self.old_age_limit_year():
            return 0

        if self.salary_rounded() <= self.parameter('jsa_g1'):
            return 0.2 * self.salary_rounded()
        if self.salary_rounded() <= self.parameter('jsa_g2'):
            return 15e3 + 0.05 * self.salary_rounded()
        if self.salary_rounded() <= self.parameter('jsa_g3'):
            return 30e3

        return 30e3 - 0.03 * (self.salary_rounded() - self.parameter('jsa_g3'))

    def _jobbskatteavdrag_base_case(self):
        # TODO: get limits and rates from params file
        if self.birth_year <= self.old_age_limit_year():
            return 0
        if self.salary_rounded() <= self.parameter('jsa_m1') * self.parameter('pris_bas_belopp'):
            return self.parameter('kommunalskatt_%s' % self.municipality,
                                  100) * (self.salary_rounded() - self.basic_deduction())
        if self.salary_rounded() <= self.parameter('jsa_m2') * self.parameter('pris_bas_belopp'):
            return (self.parameter('jsa_m1') * self.parameter('pris_bas_belopp') + 0.3405 * (self.salary_rounded() - self.parameter('jsa_m1') * self.parameter(
                'pris_bas_belopp')) - self.basic_deduction()) * self.parameter('kommunalskatt_%s' % self.municipality, 100)
        if self.salary_rounded() <= self.parameter('jsa_m3') * self.parameter('pris_bas_belopp'):
            return (1.703 * self.parameter('pris_bas_belopp') + 0.128 * (self.salary_rounded() - self.parameter('jsa_m2') * self.parameter(
                'pris_bas_belopp')) - self.basic_deduction()) * self.parameter('kommunalskatt_%s' % self.municipality, 100)
        if self.salary_rounded() <= self.parameter('jsa_m4') * self.parameter('pris_bas_belopp'):
            return (2.323 * self.parameter('pris_bas_belopp') - self.basic_deduction()
                    ) * self.parameter('kommunalskatt_%s' % self.municipality, 100)

        return (2.323 * self.parameter('pris_bas_belopp') - self.basic_deduction()) * self.parameter('kommunalskatt_%s' %
                                                                                                     self.municipality, 100) - 0.03 * (self.salary_rounded() - self.parameter('jsa_m4') * self.parameter('pris_bas_belopp'))

    def jobbskatteavdrag(self):
        """
        break this out into own function since it's quite finicky
        """
        return np.floor(self._jobbskatteavdrag_older() +
                        self._jobbskatteavdrag_base_case())

    def net_interest(self):
        return self.int_inc_tax_not_withheld + \
            self.int_inc_tax_withheld - self.interest_expense

    def net_listed_funds_and_shares(self):
        return self.adjusted_attribute_value(
            'listed_funds_and_shares_profit') - self.adjusted_attribute_value('listed_funds_and_shares_loss')

    def net_unlisted_funds_and_shares(self):
        return self.unlisted_funds_profit - \
            self.parameter('olistad_forlust_avdrags_multipel') * \
            self.adjusted_attribute_value('unlisted_funds_loss')

    def net_property(self):
        ret_val = self.sale_private_property_profit * \
            self.parameter('vinst_avdrag_privat_fastighet_taljare') / \
            self.parameter('vinst_avdrag_privat_fastighet_namnare')
        ret_val -= self.sale_private_property_loss * \
            self.parameter('forlust_avdrag_privat_fastighet')
        ret_val += self.parameter('vinst_avdrag_kommers_fastighet') * \
            self.sale_commercial_property_profit
        ret_val -= self.parameter('forlust_avdrag_kommers_fastighet') * \
            self.sale_commercial_property_loss
        return ret_val

    def capital_surplus_deficit(self):
        """
        # overskottUnderskottKapital:
        # divide into different areas:
        #  standard_income  (no offsetting reduction)
        #  rental income (no offsetting reduction, since it's already net of costs)
        #  Ranta  (income vs expenses, net 100% multiplier)
        #  Fondandelar (profits vs loss, net is 70% multiplier)
        #  Fondandelar ej marknadsnoterade (profits vs loss, net is 70% multiplier)
        #  Forsaljning privatbostad (profit vs loss, net is 50% multipllier)
        #  Forsäljning näringsbostad (p vs l, net is 63%)
        """

        surplus_deficit = 0
        surplus_deficit += self.standard_income
        surplus_deficit += self.rental_income
        surplus_deficit += self.net_interest()
        if self.net_listed_funds_and_shares() < 0:
            surplus_deficit += self.parameter(
                'listade_instrument_forlust_avdrags_multipel') * self.net_listed_funds_and_shares()
        else:
            surplus_deficit += self.net_listed_funds_and_shares()

        surplus_deficit += self.net_unlisted_funds_and_shares()
        surplus_deficit += self.net_property()
        surplus_deficit -= self.investor_deduction

        return surplus_deficit

    def _skatte_reduktion(self, netto_underskott):
        """
        helper function
        """
        
        return np.floor(self.parameter('skatte_reduktion_forsta_niva') * min(self.parameter('tak_skattereduktion'), netto_underskott) +
                        self.parameter('skatte_reduktion_andra_niva') * max(netto_underskott - self.parameter('tak_skattereduktion'), 0))

    def capital_income_tax(self, verbose=False):
        """
        returns cap_tax, cap_tax_reduction, cap_tax_basis

        """
        surplus_deficit = self.capital_surplus_deficit()

        cap_tax_reduction = 0
        state_rate = self.parameter('statlig_skatt', 100)
        is_surplus = True
        # pdb.set_trace()
        if surplus_deficit < 0:
            cap_tax = 0
            is_surplus = False
            surplus_deficit = abs(surplus_deficit)
            cap_tax_reduction_calc = self._skatte_reduktion(surplus_deficit)
            if verbose:
                print("Calculated tax reduction cap is %f and the calculated deduction is %f" % (
                    self.tax_reduction_cap(), cap_tax_reduction_calc))
            cap_tax_reduction = max(
                min(self.tax_reduction_cap(), cap_tax_reduction_calc), 0)
        else:
            cap_tax = state_rate * surplus_deficit

        return cap_tax, cap_tax_reduction, np.ceil(surplus_deficit), is_surplus

    def taxable_income(self):
        return np.floor(self.adjusted_attribute_value(
            'salary') / 100) * 100 - self.basic_deduction()

    def municipal_tax(self):
        return np.floor(self.taxable_income(
        ) * self.parameter('kommunalskatt_%s' % self.municipality, 100))

    def salary_rounded(self):
        return np.floor(self.adjusted_attribute_value('salary') / 100) * 100

    def state_income_tax(self):
        return self.parameter('statlig_inkomst_skatt', 100) * \
            max(self.taxable_income() - self.parameter('skiktgrans'), 0)

    def absolute_pension_cutoff(self):
        return self.parameter('allman_pension_noll', 100) * \
            self.parameter('inkomst_bas_belopp')
        # abs_pension_cap = pension_ceil_mult * inkomst_bas_belopp

    def absolute_pension_cap(self):
        return self.parameter('allman_pension_tak') * \
            self.parameter('inkomst_bas_belopp')

    def pension(self):
        pension = 0 if self.adjusted_attribute_value('salary') < self.absolute_pension_cutoff() else min(
            self.parameter('allman_pension_procent', 100) * self.adjusted_attribute_value('salary'), self.absolute_pension_cap() * self.parameter('allman_pension_procent') / 100)

        return np.floor(pension / 100) * 100

    def tax_reduction_cap(self):
        # print('hej')
        return self.municipal_tax() + self.state_income_tax() - self.job_deduction - \
            self.income_deduction - self.pension()

    def public_service_cost(self):
        return min(self.parameter('public_service_avgift'), self.parameter(
            'public_service_percent', 100) * self.taxable_income())

    def tax(self):

        cap_tax, cap_tax_reduction, cap_tax_basis, is_surplus = self.capital_income_tax()

        # pdb.set_trace()
        hypo_pension_reduction = self.pension()
        if not is_surplus or abs(cap_tax_basis) < 1e-4:
            if self.tax_reduction_cap() < 0:
                # if birth_year > limit_year:
                orig_jsa = copy.deepcopy(self.job_deduction)
                residual = 0
                if abs(self.tax_reduction_cap()) > self.job_deduction:
                    residual = abs(self.tax_reduction_cap()) - \
                        self.job_deduction
                    self.job_deduction = 0
                else:
                    self.job_deduction = self.job_deduction + self.tax_reduction_cap()

                if residual > 0:
                    # pdb.set_trace()
                    if hypo_pension_reduction >= residual:
                        hypo_pension_reduction -= residual
                    else:
                        print("Not sure what deduction to decrease!?")
                        pdb.set_trace()
                else:
                    self.job_deduction = self.job_deduction + self.income_deduction
                    self.income_deduction = 0
                print(
                    "Changing jobbskatteavdrag from %.0f to %.0f" %
                    (orig_jsa, self.job_deduction))

        non_zero_surplus = False
        if is_surplus:
            non_zero_surplus = cap_tax_basis > 0

        if abs(self.municipal_tax()) > 1e-4:
            pension_reduction = hypo_pension_reduction
        else:
            if not non_zero_surplus:

                pension_reduction = 0
            else:
                pension_reduction = self.pension()

        # pdb.set_trace()
        if abs(self.municipal_tax()) < 1e-4:
            # we can't get this deduction if we don't pay any muni tax:
            # https://www4.skatteverket.se/rattsligvagledning/edition/2021.1/2940.html
            # ('avrakning av reduktionen')
            self.job_deduction = 0

        if self.adjusted_attribute_value(
                'salary') > self.lower_limit_for_income_tax:
            total_tax = self.municipal_tax() + cap_tax + self.pension() - pension_reduction + self.funeral_fee + \
                self.public_service_cost() - self.job_deduction - self.income_deduction + \
                self.state_income_tax() - cap_tax_reduction
        else:
            total_tax = 0

        # total_tax ties with 'slutligSkatt' in the skatteverket calculator, but that's not what we actually end up paying,
        # this catches that

        self.tax_breakdown_dict = {'slutligSkatt': total_tax - self.parameter('statlig_skatt', 100) * self.int_inc_tax_withheld, 'kommunalInkomstskatt': self.municipal_tax(), 'statligInkomstskattKapitalinkomst': cap_tax, 'allmanPensionsavgift': self.pension(), 'skattereduktionAllmanPensionsavgift': pension_reduction,
                                   'begravningsavgift': self.funeral_fee, 'publicServiceAvgift': self.public_service_cost(), 'skattereduktionArbetsinkomster': self.job_deduction, 'skattereduktionForvarvsinkomst': self.income_deduction,
                                   'statligInkomstskattForvarvsinkomst': self.state_income_tax(), 'overskottUnderskottKapital': cap_tax_basis, 'forvarvsinkomst': self.adjusted_attribute_value('salary'),
                                   'faststalldForvarvsinkomst': self.salary_rounded(), 'beskattningsbarForvarvsinkomst': self.taxable_income(), 'grundavdrag': self.basic_deduction(), 'kommunalLandstingsSkattesats': self.parameter('kommunalskatt_%s' % self.municipality, 100),
                                   'skattereduktionUnderskottKapital': cap_tax_reduction, 'avdragenSkattPaKapital': self.parameter('statlig_skatt', 100) * self.int_inc_tax_withheld}
        return total_tax - \
            self.parameter('statlig_skatt', 100) * self.int_inc_tax_withheld

    def tax_ties_with_config(
            self, do_all=False, atol=1e-8, rtol=1e-5):
        """
        Check that the computed tax ties with the tax stored in the config file
        """
        if not do_all:
            return np.allclose(tut.config_tax(
                self.case_idx, case_file=self.case_file), self.tax())

        case_numbers = tut.all_case_numbers(case_file=self.case_file)
        observed = []
        expected = []
        for case_idx in tqdm(case_numbers):
            # print("working on case number %d" % case_idx)
            setattr(self, 'case_idx', case_idx)
            # self.case_idx =
            # pdb.set_trace()
            observed.append(self.tax())
            expected.append(
                tut.config_tax(
                    self.case_idx,
                    case_file=self.case_file))

        # pdb.set_trace()
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

    def payload(self):
        """
        FIXME can read municipal rate etc from api? Not important right now


        """
        data = {}
        data['allmannaAvdrag'] = {'socialforsakringsavgifter': 'null'}

        # calculate profit/loss from selling qualified shares in small companies:
        # parameters = tax_parameters(tax_year=tax_year)

        salary = self.salary
        unlisted_funds_loss = self.unlisted_funds_loss
        listed_funds_and_shares_profit = self.listed_funds_and_shares_profit
        listed_funds_and_shares_loss = self.listed_funds_and_shares_loss

        extra_salary, extra_listed_funds_and_shares_profit, extra_unlisted_funds_loss = self.qualified_shares_income_taxation()

        unlisted_funds_loss += extra_unlisted_funds_loss
        salary += extra_salary
        listed_funds_and_shares_profit += extra_listed_funds_and_shares_profit

        extra_listed_funds_and_shares_profit, extra_listed_loss = self.unqualified_shares_income_taxation()
        listed_funds_and_shares_profit += extra_listed_funds_and_shares_profit
        listed_funds_and_shares_loss += extra_listed_loss

        # pdb.set_trace()
        if abs(listed_funds_and_shares_loss) > 1e-4:
            listed_loss = '%d' % listed_funds_and_shares_loss
        else:
            listed_loss = 'null'

        vinstSmahusBostadsratt = 'null'
        forlustSmahusBostadsratt = 'null'
        if abs(self.sale_private_property_profit) > 1e-4:
            vinstSmahusBostadsratt = '%d' % self.sale_private_property_profit

        if abs(self.sale_private_property_loss) > 1e-4:
            forlustSmahusBostadsratt = '%d' % self.sale_private_property_loss

        inkomstrantorSkatteavdrag = 'null'
        inkomstrantorUtanSkatteavdrag = 'null'
        if abs(self.int_inc_tax_withheld) > 1e-4:
            inkomstrantorSkatteavdrag = '%d' % self.int_inc_tax_withheld

        if abs(self.int_inc_tax_not_withheld) > 1e-4:
            inkomstrantorUtanSkatteavdrag = '%d' % self.int_inc_tax_not_withheld

        ranteutgifter = 'null'

        if abs(self.interest_expense) > 1e-4:
            ranteutgifter = '%d' % self.interest_expense

        forlustFondandelarInteMarknadsnoterade = 'null'
        if abs(unlisted_funds_loss) > 1e-4:
            forlustFondandelarInteMarknadsnoterade = '%d' % unlisted_funds_loss

        schablonintakt = 'null'
        if abs(self.standard_income) > 1e-4:
            schablonintakt = '%d' % self.standard_income

        forlustNaringsfastighetNaringsbostadsratt = 'null'
        if abs(self.sale_commercial_property_loss) > 1e-4:
            forlustNaringsfastighetNaringsbostadsratt = '%d' % self.sale_commercial_property_loss

        vinstNaringsfastighetNaringsbostadsratt = 'null'
        if abs(self.sale_commercial_property_profit) > 1e-4:
            vinstNaringsfastighetNaringsbostadsratt = '%d' % self.sale_commercial_property_profit

        investeraravdrag = 'null'
        if abs(self.investor_deduction) > 1e-4:
            investeraravdrag = '%d' % self.investor_deduction
        # if tax_year is None:
        #     tax_year = pd.to_datetime('today').year
        income_start = datetime.date(self.tax_year, 1, 1).strftime('%Y-%m-%d')
        income_end = datetime.date(self.tax_year, 12, 1).strftime('%Y-%m-%d')

        data['avdragKapital'] = {'forlustAktierFondandelarMarknadsnoterade': listed_loss,
                                 'forlustFondandelarInteMarknadsnoterade': forlustFondandelarInteMarknadsnoterade,
                                 'forlustNaringsfastighetNaringsbostadsratt': forlustNaringsfastighetNaringsbostadsratt,
                                 'forlustSmahusBostadsratt': forlustSmahusBostadsratt,
                                 'investeraravdrag': investeraravdrag,
                                 'ranteutgifter': ranteutgifter}
        data['avdragTjanst'] = {'dubbelBosattning': 'null', 'ovrigaUtgifterBrutto': 'null',
                                'resorTillOchFranArbetetBrutto': 'null', 'tjansteresor': 'null'}

        data['uppgifterAvlidnaSjomanUtInvandrade'] = {'avlidenAr': 'null',
                                                      'bosattManader': '12',
                                                      'dagarFjarrfart': 'null',
                                                      'dagarNarfart': 'null',
                                                      'folkbokford': 'true',
                                                      'inUtvandrad': 'false',
                                                      'invandradManad': 'null',
                                                      'utvandradManad': 'null'}

        data['utlandskForsakringAvkastningsskatt'] = {'skatteunderlagKapitalforsakring': 'null',
                                                      'skatteunderlagPensionsforsakring': 'null'}

        data['underlagSkattreduktion'] = {'fackforeningsavgift': 'null',
                                          'gava': 'null',
                                          'hasAvdragFromArbetsgivare': 'false',
                                          'preliminarFornybarElkWh': 'null',
                                          'regionalSkattereduktion': 'false',
                                          'rotarbeteFaktura': 'null',
                                          'rotarbeteForman': 'null',
                                          'rutarbeteFaktura': 'null',
                                          'rutarbeteForman': 'null'}

        data['tjansteinkomster'] = {'hittillsUnderAret': {'allmanPensionTjanstepensionHittills': 'null',
                                                          'avdragenSkatt': 'null',
                                                          'kostnadsersattningarHittills': 'null',
                                                          'loneinkomsterHittills': 'null',
                                                          'period': {'fromDate': income_start, 'tomDate': income_end},
                                                          'sjukAktivitetsersattningLonHittills': 'null',
                                                          'sjukAktivitetsersattningPensionHittills': 'null',
                                                          'sjukpenningAKassaMmHittills': 'null'},
                                    'restenAvAret': {'allmanPensionTjanstepensionResten': 'null',
                                                     'inkomstFrom': 'null',
                                                     'isHelar': 'true',
                                                     'kostnadsersattningarResten': 'null',
                                                     'loneinkomsterResten': '%d' % salary,
                                                     'period': {'fromDate': '2021-12-01', 'tomDate': '2021-12-01'},
                                                     'sjukAktivitetsersattningLonResten': 'null',
                                                     'sjukAktivitetsersattningPensionResten': 'null',
                                                     'sjukpenningAKassaMmResten': 'null'}}

        data['grunduppgifter'] = {'fodelsear': self.birth_year,
                                  'inkomstar': pd.to_datetime('today').year,
                                  'kommunkod': 'null',
                                  'showRegionalSkattereduktion': 'false',
                                  'skatteAvgiftssatser': {'avgiftssatsBegravningsavgift': 0.253,
                                                          'avgiftssatsKyrkoavgift': 'null',
                                                          'avgiftssatsSamfundsavgift': 'null',
                                                          'kommunalLandstingsSkattesats': 31.44,
                                                          'summaKommunalskattAvgifter': 'null'},
                                  'skattesatserTyp': '0'}
        data['inkomsterKapital'] = {'egenInbetalningSkatt': 'null',
                                    'inkomstUthyrningPrivatbostad': '%d' % self.rental_income,
                                    'inkomstrantor': 'null',
                                    'inkomstrantorSkatteavdrag': inkomstrantorSkatteavdrag,
                                    'inkomstrantorUtanSkatteavdrag': inkomstrantorUtanSkatteavdrag,
                                    'schablonintakt': schablonintakt,
                                    'trettioProcentAvInkomstrantorSkatteavdrag': 0,
                                    'vinstAktierFondandelarMarknadsnoterade': '%d' % listed_funds_and_shares_profit,
                                    'vinstFondandelarInteMarknadsnoterade': '%d' % self.unlisted_funds_profit,
                                    'vinstNaringsfastighetNaringsbostadsratt': vinstNaringsfastighetNaringsbostadsratt,
                                    'vinstSmahusBostadsratt': vinstSmahusBostadsratt}
        data['naringsfastigheter'] = {'underlagFastighetsavgift': {'fastighetsavgiftHalvHyreshus': 'null',
                                                                   'fastighetsavgiftHelHyreshus': 'null'},
                                      'underlagFastighetsskatt': {'fastighetsskattHyreshusTomt': 'null',
                                                                  'fastighetsskattIndustri': 'null',
                                                                  'fastighetsskattLokal': 'null',
                                                                  'fastighetsskattVatten': 'null',
                                                                  'fastighetsskattVind': 'null'}}

        data['naringsverksamhet'] = {'aktivNaringsverksamhet': {'overskottAktivNaringsverksamhet': 'null',
                                                                'sjukpenningAktivNaringsverksamhet': ''},
                                     'allmannaAvdragDto': {'allmantAvdragUnderskottNaringsverksamhet': 'null'},
                                     'arbetsgivareSocialaAvgifter': {'inkomsterIngaSocialaAvgifter': 'null',
                                                                     'kostnaderIngaSocialaAvgifter': 'null'},
                                     'avkastningsskattPensionskostnader': {'underlagAvkastningsskattPension': 'null'},
                                     'nedsattningEgenavgifter': {'regionaltNedsattningsbelopp': 'null'},
                                     'passivNaringsverksamhet': {'overskottPassivNaringsverksamhet': 'null'},
                                     'rantefordelning': {'negativRantefordelning': 'null',
                                                         'positivRantefordelning': 'null'},
                                     'sarskildLoneskattPensionskostnader': {'underlagPensionskostnaderAnstallda': 'null',
                                                                            'underlagPensionskostnaderEgen': 'null'},
                                     'underlagExpansionsfondsskatt': {'minskningExpansionsfond': 'null',
                                                                      'okningExpansionsfond': 'null',
                                                                      'underlagAterforingExpansionsfondsskatt': 'null'}}
        data['ovrigaTjansteinkomster'] = {'ersattningFranVinstandelsstiftelseMmUtanPgiOchJobbskatteavdrag': 'null',
                                          'hobbyinkomster': 'null',
                                          'inkomsterFranFamansbolag': 'null',
                                          'ovrigaInkomsterUtanPgi': 'null'}
        data['pensionsforhallandenKarensuppgifter'] = {'allmanPensionHelaAret': 'false',
                                                       'antalDagarKarensEnDag': 'null',
                                                       'antalDagarKarensFjortonDagar': 'null',
                                                       'antalDagarKarensNittioDagar': 'null',
                                                       'antalDagarKarensSextioDagar': 'null',
                                                       'antalDagarKarensSjuDagar': 365,
                                                       'antalDagarKarensTrettioDagar': 'null',
                                                       'helSjukAktivitetsersattning': 'false',
                                                       'manuelltUnderlagForSlfPaAktivNrvJanTillJun2019': 'null'}
        data['skattOvrigt'] = {'avrakningUtlandskSkatt': 'null',
                               'egenInbetalningSkatt': 'null',
                               'preliminarSkatt': 'null'}
        data['smahusAgarlagenhet'] = {'underlagFastighetsavgift': {'fastighetsavgiftHalvSmahus': 'null',
                                                                   'fastighetsavgiftHelSmahus': 'null',
                                                                   'skrivenHelaAret': 'null',
                                                                   'underlagSkattereduktionFastighetsavgiftHalvAvgift': '',
                                                                   'underlagSkattereduktionFastighetsavgiftHelAvgift': ''},
                                      'underlagFastighetsskatt': {'fastighetsskattSmahusTomt': 'null'}}
        return data

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
        return True

    def tax_breakdown(self):
        """
        simple breakdown of the components making up tax. so far quite unstructured
        """
        self.tax()
        raw = self.tax_breakdown_dict
        return pd.DataFrame(raw, index=['0'])

    def query_web_for_tax_results(self, refresh=False, session=None):
        """
        post the request to skatteverket.se
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
        return res.json()

    def official_tax(self, refresh=False, session=None):
        """
        would be great if we didn't have to do the extra step here...
        """
        resp = self.parsed_official_response(refresh=refresh, session=session)
        slutlig_skatt = resp.query("item == 'slutligSkatt'").value.item()

        return slutlig_skatt - \
            self.parameter('statlig_skatt', 100) * self.int_inc_tax_withheld

    def parsed_official_response(self, refresh=False, session=None):
        """
        make a dataframe from the structure returned by the web query
        """

        raw = self.query_web_for_tax_results(refresh=refresh, session=session)
        if 'leafs' not in raw:
            # this means something is wrong
            # pdb.set_trace()
            raise Exception(raw['technicalMessage'])

        res = raw['leafs']
        # pdb.set_trace()
        out = [[res[6]['apiText'], res[6]['leafs'][0]
                ['apiText'], float(res[6]['leafs'][0]['value'])]]

        skiplist = [
            'skillnadPrognos',
            'skatteavdragRestenPerManadPrognosHelar']

        out.append([res[4]['apiText'], res[4]['leafs'][0]['apiText'],
                    float(res[4]['leafs'][0]['value'].replace(',', '.')) / 100])

        for ele in res[5]['leafs']:
            out.append(
                [res[5]['apiText'], ele['apiText'], float(ele['value'])])
        for ele in res[7]['leafs']:
            if ele['apiText'] not in skiplist:
                out.append(
                    [res[7]['apiText'], ele['apiText'], float(ele['value'])])

        return pd.DataFrame(out, columns=['group', 'item', 'value'])
