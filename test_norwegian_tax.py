import tax_norway as tax



def test_all_cases(_class=tax.NorwegianTax, atol=1e-8, rtol=1e-5):
    """
    Run through all the cases in the .ini file

    So this tests the calculated tax vs the tax written to the config (which originally comes from the Norwegian tax authority's homepage)
    """
    obj = _class()
    return obj.tax_ties_with_config(do_all=True, atol=atol, rtol=rtol)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
