

__can_cache__ = True
__tabulate_avail__ = True
__plotly_avail__ = True
__config_name__ = 'taxes.ini'


import json
import os
import configparser
import requests
import numpy as np
import pandas as pd

try:
    import caching3 as cache
except ImportError as err:
    # pdb.set_trace()
    __can_cache__ = False
    print("Failed to import caching lib: %s" % err.msg)

try:
    import plotly.io as pio
except ImportError as err:
    __plotly_avail__ = True
    print("Failed to import plotting lib: %s" % err.msg)


def get_request(url='', refresh=False, headers_=None,
                method='get', payload_=None):
    """
    simple wrapper to avoid querying multiple times
    meaningless if cache library not available

    """
    # print __file__
    if __can_cache__:
        cache_key = cache.create_cache_key(
            locals(), cache.current_function_name())
        ret_val = cache.extract_cache_data(cache_key, refresh)
    else:
        ret_val = None
    # pdb.set_trace()
    if ret_val is None:
        if headers_ is None:
            if method == 'get':
                ret_val = requests.get(url)
            elif method == 'post':
                if payload_ is not None:
                    # print("got to the right place")
                    ret_val = requests.post(
                        url, data=json.dumps(payload_), headers=headers_)
                else:
                    ret_val = requests.post(url)
            else:
                raise NotImplementedError(
                    "Method == '%s' not implemented" % method)
        else:
            if method == 'get':
                ret_val = requests.get(url, headers=headers_)
            elif method == 'post':
                if payload_ is not None:
                    # print("got to the right place")
                    ret_val = requests.post(url, data=json.dumps(
                        payload_, cls=NpEncoder), headers=headers_)
                else:
                    ret_val = requests.post(url)
            else:
                raise Exception("Unknown method == '%s'" % method)

        if __can_cache__:
            cache.set_gp_cache(cache_key, ret_val)
    return ret_val
class NpEncoder(json.JSONEncoder):
    """
    Needed for when we produce the test cases (since they get created with np.int64s instead of ints, which JSONEncoder can't handle)
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def tax_parameters(jurisdiction='NO', tax_year=None):
    """
    this reads in the parameters from the config and makes them easily usable from other functions
    """

    if not os.path.exists(__config_name__):
        raise Exception(
            "You need a file called '%s' with all relevant tax parameters in it!" % (__config_name__))

    if tax_year is None:
        tax_year = pd.to_datetime('today').year
    key = '%s-%d' % (jurisdiction, tax_year)
    config = configparser.ConfigParser()
    config.read(__config_name__)
    try:
        return config[key]
    except BaseException:
        raise Exception("Tax year = %d not implemented for %s jurisdiction" % (tax_year, jurisdiction))

def tax_round(in_float):
    """
    For values exactly halfway between rounded decimal values, NumPy
    rounds to the nearest even value. Thus 1.5 and 2.5 round to 2.0,
    -0.5 and 0.5 round to 0.0, etc.
    """
    if in_float == int(in_float):
        return int(in_float)

    _lo = np.floor(in_float)
    _hi = np.ceil(in_float)
    dist_to_hi = abs(in_float - _hi)
    dist_to_lo = abs(in_float - _lo)
    if dist_to_hi <= dist_to_lo:
        return int(_hi)
    # elif dist_to_lo < dist_to_hi:
    return int(_lo)
def big_fmt(val):
    """
    format with thousandsd separator
    """
    if pd.isnull(val):
        return 'n/a'

    if isinstance(val, str):
        return val

    return '{:,}'.format(int(round(val, 0))).strip()


def display_df(frame, title=None, header_size=1):
    """
    Show the dataframe in the browser
    """
    if not __plotly_avail__:
        raise Exception("You don't have plotly installed")
    raw = frame.to_html(index=False)
    if title is not None:
        raw = '<h%d>%s</h%d>%s' % (header_size, title, header_size, raw)
    pio._base_renderers.open_html_in_browser(raw)

def check_config_cases_vs_web(verbose=False, rtol=1e-5, atol=1e-8, case_file='no_test_cases.ini', official_func=None):
    """
    Mostly to catch fat fingers when punching in test cases

    example usage:


    import tax_norway as tn
    import tax_utils as tut
    tut.check_config_cases_vs_web(official_func=tn.produce_tax_results)
    """
    cases = configparser.ConfigParser()
    cases.read(case_file)
    case_numbers = sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))
    with requests.Session() as sesh:
        for idx in case_numbers:
            assert check_test_case_config_vs_web(
                case_idx=idx, session=sesh, verbose=verbose, atol=atol, rtol=rtol, official_func=official_func), "Tax for case %s is off!" % idx

    print("All tax figures in config tested successfully!")

def check_test_case_config_vs_web(
        case_idx=0, verbose=True, refresh=True, session=None, rtol=1e-5, atol=1e-8, case_file='no_test_cases.ini', official_func=None):
    """
    this checks the config tax number vs the web number
    """
    input_struct = {}
    cases = configparser.ConfigParser()
    cases.read(case_file)
    
    for k, value in cases['%d' % case_idx].items():
        if k != 'tax':
            input_struct[k] = value

    for k, value in input_struct.items():
        if value.isdigit():
            input_struct[k] = float(value)
        elif value.replace('.', '').isdigit():
            input_struct[k] = float(value)
        elif value.replace('e', '').isdigit():
            input_struct[k] = eval(value)
    # pdb.set_trace()
    # input_struct['return_fields'] = ['all']
    input_struct['refresh'] = refresh
    official = official_func(**input_struct, session=session)

    exp = official.tax.sum()
    obs = config_tax(case_idx=case_idx, case_file=case_file)
    if verbose:
        print("Correct tax is %.1f" % exp)
        print("Config tax is %.1f" % obs)
    res_ok = np.abs(obs - exp) <= (atol + rtol * np.abs(exp))
    return res_ok



def config_tax(case_idx=0, correct_tax_field='tax', case_file='no_test_cases.ini'):
    """
    what is the 'correct' tax as per the config
    """
    input_struct = inputs_for_case_number(case_idx, case_file=case_file, include_correct_tax=True)
    return input_struct.get(correct_tax_field, None)

def check_test_case_config_vs_calculation(
        case_idx=0, verbose=True, atol=1e-8, rtol=1e-5, return_breakdown=False, case_file='no_test_cases.ini', calc_func=None, correct_tax_field='tax'):
    """
    this checks the config tax number vs the our calculated number
    """

    input_struct = inputs_for_case_number(case_idx, case_file=case_file, include_correct_tax=True)
    
    config_tax_ = input_struct[correct_tax_field]
    del input_struct[correct_tax_field]
    calculated = calc_func(**input_struct)

    if return_breakdown:
        return calculated

    
    obs = calculated
    exp = config_tax_
    if verbose:
        print(
            "[%d]: Calculated tax = %.1f, config tax = %.1f" %
            (case_idx, obs, exp))
    res_ok = np.abs(obs - exp) <= (atol + rtol * np.abs(exp))
    return res_ok

def inputs_for_case_number(case_idx=0, case_file='no_test_cases.ini', include_correct_tax=False, correct_tax_field='tax'):
    """
    helper function
    """
    input_struct = {}
    cases = configparser.ConfigParser()
    cases.read(case_file)
   
    for k, value in cases['%d' % case_idx].items():
        if k != correct_tax_field:
            input_struct[k] = value
        elif k == correct_tax_field and include_correct_tax:
            input_struct[k] = value
   

    for k, value in input_struct.items():
        if value.isdigit():
            input_struct[k] = float(value)
        elif value.replace('.', '').isdigit():
            input_struct[k] = float(value)
        elif value.replace('e', '').isdigit():
            input_struct[k] = eval(value)

    
    return input_struct

def all_case_numbers(case_file='no_test_cases.ini'):
    """
    helper function
    """
    cases = configparser.ConfigParser()
    cases.read(case_file)
    return sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))

def check_calculations_vs_config(
        verbose=False, start_at_case=None, rtol=1e-5, atol=1e-8, stop_at_failure=True, case_file='no_test_cases.ini', calc_func=None):
    """
    check that our calculations tied with the hardcoded values int he config


    example usage:
    import tax_norway as tn
    import tax_utils as tut
    tut.check_calculations_vs_config(verbose=True, start_at_case=None, rtol=1e-5, stop_at_failure=True, calc_func=tn.tax_calculation)
    """
    cases = configparser.ConfigParser()
    cases.read(case_file)
    case_numbers = sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))
    # pdb.set_trace()
    for idx in case_numbers:
        if start_at_case is not None and idx < start_at_case:
            continue
        if stop_at_failure:
            assert check_test_case_config_vs_calculation(
                case_idx=idx, verbose=verbose, rtol=rtol, atol=atol, case_file=case_file, calc_func=calc_func), "Tax for case %s is off!" % idx
        else:
            if not check_test_case_config_vs_calculation(
                    case_idx=idx, verbose=verbose, rtol=rtol, atol=atol, case_file=case_file, calc_func=calc_func):
                print("Tax for case %s is off!" % idx)
                continue

    print("All tax figures in config tested successfully!")

def read_file_as_string(filename):
    """
    util func
    """
    with open(filename, 'r') as fil:
        return fil.read()

def syncsort(a_arr, b_arr):
    """
    sorts a in ascending order (and b will tag along, so each element of b is still associated with the right element in a)

    """
    a_arr, b_arr = (list(t) for t in zip(*sorted(zip(a_arr, b_arr))))
    return a_arr, b_arr

def get_request_from_session(session=None, url='', refresh=False, headers=None):
    """
    don't want the session object as part o fthe cache key
    """

    if __can_cache__:
        ck = cache.create_cache_key({'url':url})
        rv = cache.extract_cache_data(ck, refresh)
        if rv is not None:
            return rv
    rv = session.get(url, headers=headers)
    if __can_cache__:
        cache.set_gp_cache(ck, rv)
    return rv

def value_is_numeric_type(X):
    X = np.asanyarray(X)
    
    if (X.dtype.char in np.typecodes['AllFloat']) or (X.dtype.char in np.typecodes['Integer']):
        return True
    return False
def post_request_from_session(session=None, url='', refresh=False, headers=None, payload_=None):
    """
    don't want the session object as part o fthe cache key
    """

    if __can_cache__:
        ck = cache.create_cache_key({'url':url, 'pl':payload_})
        rv = cache.extract_cache_data(ck, refresh)
        if rv is not None:
            return rv
    rv = session.post(url, headers=headers, data=json.dumps(payload_, cls=NpEncoder))
    if __can_cache__:
        cache.set_gp_cache(ck, rv)
    return rv