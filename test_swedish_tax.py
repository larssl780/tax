import pytest
import tax_sweden as tax



def test_all_cases(_class=tax.SwedishTax, atol=1e-8, rtol=1e-5):
    """
    Run through all the cases in the .ini file

    So this tests the calculated tax vs the tax written to the config (which originally comes from the Norwegian tax authority's homepage)
    """
    obj = _class()
    ret_val = obj.tax_ties_with_config(do_all=True, atol=atol, rtol=rtol)
    print('rv = ', ret_val)
    if ret_val is not True:
        return pytest.fail("Test failed on these cases: %s"%(','.join(map(str,ret_val))))
    

    ret_val = obj.tax_ties_with_web(do_all=True, atol=atol, rtol=rtol)
    if ret_val is not True:
        return pytest.fail("Test worked vs config but failed on web-tests: failed on these cases: %s"%(','.join(map(str,ret_val))))  
    return pytest.ExitCode.OK


if __name__ == '__main__':
    pytest.main([__file__])
