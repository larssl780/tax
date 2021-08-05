import tax_norway as tax
import pytest


def test_all_cases(_class=tax.NorwegianTax, atol=1e-8, rtol=1e-5):
    """
    Run through all the cases in the .ini file

    So this tests the calculated tax vs the tax written to the config (which originally comes from the Norwegian tax authority's homepage)
    """
    obj = _class()
    ret_val = obj.tax_ties_with_config(do_all=True, atol=atol, rtol=rtol)
    # print('rv = ', rv)
    if ret_val is not True:
        assert False, "Test failed on these cases: %s" % (
            ','.join(map(str, ret_val)))
    else:
        assert ret_val

    ret_val = obj.tax_ties_with_web(do_all=True, atol=atol, rtol=rtol)
    if ret_val is not True:
        assert False, "Test worked vs config but failed on web-tests: failed on these cases: %s" % (','.join(map(str, ret_val)))
    else:
        assert ret_val


if __name__ == '__main__':

    pytest.main([__file__])
