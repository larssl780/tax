import webbrowser
import numpy as np
import pandas as pd
import tax_utils as tut
from tax_calculator import TaxCalculator


class NorwegianTax(TaxCalculator):
    """
    to facilitate easy input
    add random text to trigger a code push...
    """

    def __init__(self, salary=0, birth_year=1978, tax_year=None, gains_from_sale_fondskonto_share_comp=0, gains_from_sale_fondskonto_interest_comp=0, gains_from_sale_of_shares_ask=0, property_taxable_value=0, pension=0, pension_months=12, pension_percent=100, property_sale_proceeds=0, rental_income=0, property_sale_loss=0, bank_deposits=0,
                 bank_interest_income=0, interest_expenses=0, dividends=0, mutual_fund_dividends=0, gains_from_sale_of_shares=0, mutual_fund_interest_comp_profit=0, mutual_fund_interest_comp_profit_combi_fund=0, mutual_fund_share_comp_profit=0, mutual_fund_share_comp_profit_combi_fund=0, loss_fondskonto_shares=0, loss_fondskonto_interest=0, loss_ask_sale=0,
                 loss_from_sale_of_shares=0, loss_from_sale_mutual_fund_share_comp=0, loss_from_sale_mutual_fund_share_comp_combi_fund=0, loss_from_sale_mutual_fund_interest_comp=0,
                 loss_from_sale_mutual_fund_interest_comp_combi_fund=0, mutual_fund_wealth_share_comp=0, mutual_fund_wealth_interest_comp=0, wealth_in_shares=0, wealth_in_unlisted_shares=0, wealth_ask_cash=0, wealth_ask_shares=0, wealth_fondskonto_cash_interest=0, wealth_fondskonto_shares=0, municipality='0402', case_idx=None):

        self._salary = salary
        self._birth_year = birth_year

        if tax_year is None:
            tax_year = pd.to_datetime('today').year

        tax_url = "https://skatteberegning.app.skatteetaten.no/%d" % tax_year
        self._gains_from_sale_fondskonto_share_comp = gains_from_sale_fondskonto_share_comp
        self._gains_from_sale_fondskonto_interest_comp = gains_from_sale_fondskonto_interest_comp
        self._gains_from_sale_of_shares_ask = gains_from_sale_of_shares_ask
        self._property_taxable_value = property_taxable_value
        self._pension = pension
        self._pension_months = pension_months
        self._pension_percent = pension_percent
        self._property_sale_proceeds = property_sale_proceeds
        self._rental_income = rental_income
        self._property_sale_loss = property_sale_loss
        self._bank_deposits = bank_deposits
        self._bank_interest_income = bank_interest_income
        self._interest_expenses = interest_expenses
        self._dividends = dividends
        self._mutual_fund_dividends = mutual_fund_dividends
        self._gains_from_sale_of_shares = gains_from_sale_of_shares
        self._mutual_fund_interest_comp_profit = mutual_fund_interest_comp_profit
        self._mutual_fund_interest_comp_profit_combi_fund = mutual_fund_interest_comp_profit_combi_fund
        self._mutual_fund_share_comp_profit = mutual_fund_share_comp_profit
        self._mutual_fund_share_comp_profit_combi_fund = mutual_fund_share_comp_profit_combi_fund
        self._loss_fondskonto_shares = loss_fondskonto_shares
        self._loss_fondskonto_interest = loss_fondskonto_interest
        self._loss_ask_sale = loss_ask_sale
        self._loss_from_sale_of_shares = loss_from_sale_of_shares
        self._loss_from_sale_mutual_fund_share_comp = loss_from_sale_mutual_fund_share_comp
        self._loss_from_sale_mutual_fund_share_comp_combi_fund = loss_from_sale_mutual_fund_share_comp_combi_fund
        self._loss_from_sale_mutual_fund_interest_comp = loss_from_sale_mutual_fund_interest_comp
        self._loss_from_sale_mutual_fund_interest_comp_combi_fund = loss_from_sale_mutual_fund_interest_comp_combi_fund
        self._mutual_fund_wealth_share_comp = mutual_fund_wealth_share_comp
        self._mutual_fund_wealth_interest_comp = mutual_fund_wealth_interest_comp
        self._wealth_in_shares = wealth_in_shares
        self._wealth_in_unlisted_shares = wealth_in_unlisted_shares
        self._wealth_ask_cash = wealth_ask_cash
        self._wealth_ask_shares = wealth_ask_shares
        self._wealth_fondskonto_cash_interest = wealth_fondskonto_cash_interest
        self._wealth_fondskonto_shares = wealth_fondskonto_shares
        self._municipality = municipality

        super().__init__(
            jurisdiction='NOR',
            tax_year=tax_year,
            tax_url=tax_url,
            case_idx=case_idx)

    @staticmethod
    def tax_payable(basis=0, rate=0, limit=0, deduction=0,
                    apply_rounding=False):
        """
        convenient utility function
        """
        retval = max(basis - deduction - limit, 0) * rate

        if apply_rounding:
            return tut.tax_round(retval)
        return retval

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value

    @property
    def municipality(self):
        return self._municipality

    @municipality.setter
    def municipality(self, value):
        self._municipality = value

    @property
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        self._birth_year = value

    @property
    def gains_from_sale_fondskonto_share_comp(self):
        return self._gains_from_sale_fondskonto_share_comp

    @gains_from_sale_fondskonto_share_comp.setter
    def gains_from_sale_fondskonto_share_comp(self, value):
        self._gains_from_sale_fondskonto_share_comp = value

    @property
    def gains_from_sale_fondskonto_interest_comp(self):
        return self._gains_from_sale_fondskonto_interest_comp

    @gains_from_sale_fondskonto_interest_comp.setter
    def gains_from_sale_fondskonto_interest_comp(self, value):
        self._gains_from_sale_fondskonto_interest_comp = value

    @property
    def gains_from_sale_of_shares_ask(self):
        return self._gains_from_sale_of_shares_ask

    @gains_from_sale_of_shares_ask.setter
    def gains_from_sale_of_shares_ask(self, value):
        self._gains_from_sale_of_shares_ask = value

    @property
    def property_taxable_value(self):
        return self._property_taxable_value

    @property_taxable_value.setter
    def property_taxable_value(self, value):
        self._property_taxable_value = value

    @property
    def pension(self):
        return self._pension

    @pension.setter
    def pension(self, value):
        self._pension = value

    @property
    def pension_months(self):
        return self._pension_months

    @pension_months.setter
    def pension_months(self, value):
        self._pension_months = value

    @property
    def pension_percent(self):
        return self._pension_percent

    @pension_percent.setter
    def pension_percent(self, value):
        self._pension_percent = value

    @property
    def property_sale_proceeds(self):
        return self._property_sale_proceeds

    @property_sale_proceeds.setter
    def property_sale_proceeds(self, value):
        self._property_sale_proceeds = value

    @property
    def rental_income(self):
        return self._rental_income

    @rental_income.setter
    def rental_income(self, value):
        self._rental_income = value

    @property
    def property_sale_loss(self):
        return self._property_sale_loss

    @property_sale_loss.setter
    def property_sale_loss(self, value):
        self._property_sale_loss = value

    @property
    def bank_deposits(self):
        return self._bank_deposits

    @bank_deposits.setter
    def bank_deposits(self, value):
        self._bank_deposits = value

    @property
    def bank_interest_income(self):
        return self._bank_interest_income

    @bank_interest_income.setter
    def bank_interest_income(self, value):
        self._bank_interest_income = value

    @property
    def interest_expenses(self):
        return self._interest_expenses

    @interest_expenses.setter
    def interest_expenses(self, value):
        self._interest_expenses = value

    @property
    def dividends(self):
        return self._dividends

    @dividends.setter
    def dividends(self, value):
        self._dividends = value

    @property
    def mutual_fund_dividends(self):
        return self._mutual_fund_dividends

    @mutual_fund_dividends.setter
    def mutual_fund_dividends(self, value):
        self._mutual_fund_dividends = value

    @property
    def gains_from_sale_of_shares(self):
        return self._gains_from_sale_of_shares

    @gains_from_sale_of_shares.setter
    def gains_from_sale_of_shares(self, value):
        self._gains_from_sale_of_shares = value

    @property
    def mutual_fund_interest_comp_profit(self):
        return self._mutual_fund_interest_comp_profit

    @mutual_fund_interest_comp_profit.setter
    def mutual_fund_interest_comp_profit(self, value):
        self._mutual_fund_interest_comp_profit = value

    @property
    def mutual_fund_interest_comp_profit_combi_fund(self):
        return self._mutual_fund_interest_comp_profit_combi_fund

    @mutual_fund_interest_comp_profit_combi_fund.setter
    def mutual_fund_interest_comp_profit_combi_fund(self, value):
        self._mutual_fund_interest_comp_profit_combi_fund = value

    @property
    def mutual_fund_share_comp_profit(self):
        return self._mutual_fund_share_comp_profit

    @mutual_fund_share_comp_profit.setter
    def mutual_fund_share_comp_profit(self, value):
        self._mutual_fund_share_comp_profit = value

    @property
    def mutual_fund_share_comp_profit_combi_fund(self):
        return self._mutual_fund_share_comp_profit_combi_fund

    @mutual_fund_share_comp_profit_combi_fund.setter
    def mutual_fund_share_comp_profit_combi_fund(self, value):
        self._mutual_fund_share_comp_profit_combi_fund = value

    @property
    def loss_fondskonto_shares(self):
        return self._loss_fondskonto_shares

    @loss_fondskonto_shares.setter
    def loss_fondskonto_shares(self, value):
        self._loss_fondskonto_shares = value

    @property
    def loss_fondskonto_interest(self):
        return self._loss_fondskonto_interest

    @loss_fondskonto_interest.setter
    def loss_fondskonto_interest(self, value):
        self._loss_fondskonto_interest = value

    @property
    def loss_ask_sale(self):
        return self._loss_ask_sale

    @loss_ask_sale.setter
    def loss_ask_sale(self, value):
        self._loss_ask_sale = value

    @property
    def loss_from_sale_of_shares(self):
        return self._loss_from_sale_of_shares

    @loss_from_sale_of_shares.setter
    def loss_from_sale_of_shares(self, value):
        self._loss_from_sale_of_shares = value

    @property
    def loss_from_sale_mutual_fund_share_comp(self):
        return self._loss_from_sale_mutual_fund_share_comp

    @loss_from_sale_mutual_fund_share_comp.setter
    def loss_from_sale_mutual_fund_share_comp(self, value):
        self._loss_from_sale_mutual_fund_share_comp = value

    @property
    def loss_from_sale_mutual_fund_share_comp_combi_fund(self):
        return self._loss_from_sale_mutual_fund_share_comp_combi_fund

    @loss_from_sale_mutual_fund_share_comp_combi_fund.setter
    def loss_from_sale_mutual_fund_share_comp_combi_fund(self, value):
        self._loss_from_sale_mutual_fund_share_comp_combi_fund = value

    @property
    def loss_from_sale_mutual_fund_interest_comp(self):
        return self._loss_from_sale_mutual_fund_interest_comp

    @loss_from_sale_mutual_fund_interest_comp.setter
    def loss_from_sale_mutual_fund_interest_comp(self, value):
        self._loss_from_sale_mutual_fund_interest_comp = value

    @property
    def loss_from_sale_mutual_fund_interest_comp_combi_fund(self):
        return self._loss_from_sale_mutual_fund_interest_comp_combi_fund

    @loss_from_sale_mutual_fund_interest_comp_combi_fund.setter
    def loss_from_sale_mutual_fund_interest_comp_combi_fund(self, value):
        self._loss_from_sale_mutual_fund_interest_comp_combi_fund = value

    @property
    def mutual_fund_wealth_share_comp(self):
        return self._mutual_fund_wealth_share_comp

    @mutual_fund_wealth_share_comp.setter
    def mutual_fund_wealth_share_comp(self, value):
        self._mutual_fund_wealth_share_comp = value

    @property
    def mutual_fund_wealth_interest_comp(self):
        return self._mutual_fund_wealth_interest_comp

    @mutual_fund_wealth_interest_comp.setter
    def mutual_fund_wealth_interest_comp(self, value):
        self._mutual_fund_wealth_interest_comp = value

    @property
    def wealth_in_shares(self):
        return self._wealth_in_shares

    @wealth_in_shares.setter
    def wealth_in_shares(self, value):
        self._wealth_in_shares = value

    @property
    def wealth_in_unlisted_shares(self):
        return self._wealth_in_unlisted_shares

    @wealth_in_unlisted_shares.setter
    def wealth_in_unlisted_shares(self, value):
        self._wealth_in_unlisted_shares = value

    @property
    def wealth_ask_cash(self):
        return self._wealth_ask_cash

    @wealth_ask_cash.setter
    def wealth_ask_cash(self, value):
        self._wealth_ask_cash = value

    @property
    def wealth_ask_shares(self):
        return self._wealth_ask_shares

    @wealth_ask_shares.setter
    def wealth_ask_shares(self, value):
        self._wealth_ask_shares = value

    @property
    def wealth_fondskonto_cash_interest(self):
        return self._wealth_fondskonto_cash_interest

    @wealth_fondskonto_cash_interest.setter
    def wealth_fondskonto_cash_interest(self, value):
        self._wealth_fondskonto_cash_interest = value

    @property
    def wealth_fondskonto_shares(self):
        return self._wealth_fondskonto_shares

    @wealth_fondskonto_shares.setter
    def wealth_fondskonto_shares(self, value):
        self._wealth_fondskonto_shares = value

    @property
    def share_related_income(self):
        return self.gains_from_sale_fondskonto_share_comp + self.dividends + self.mutual_fund_dividends + self.gains_from_sale_of_shares + self.gains_from_sale_of_shares_ask + self.mutual_fund_share_comp_profit + \
            self.mutual_fund_share_comp_profit_combi_fund - self.loss_fondskonto_shares - self.loss_from_sale_of_shares - \
            self.loss_from_sale_mutual_fund_share_comp - \
            self.loss_from_sale_mutual_fund_share_comp_combi_fund - self.loss_ask_sale

    @property
    def interest_related_income(self):
        return self.gains_from_sale_fondskonto_interest_comp - self.interest_expenses + self.mutual_fund_interest_comp_profit + self.mutual_fund_interest_comp_profit_combi_fund + \
            self.bank_interest_income - self.loss_fondskonto_interest - self.loss_from_sale_mutual_fund_interest_comp - \
            self.loss_from_sale_mutual_fund_interest_comp_combi_fund

    @property
    def property_related_income(self):
        return self.rental_income + self.property_sale_proceeds - self.property_sale_loss

    @property
    def non_pension_income(self):
        return self.salary + self.share_related_income + \
            self.interest_related_income + self.property_related_income

    @property
    def income_tax_basis(self):
        if abs(self.non_pension_income) < 1e-4:
            return max(self.pension - self.pension_only_minimum_deduction, 0)
        if abs(self.pension) < 1e-4:
            return max(self.salary - self.salary_only_minimum_deduction + self.parameter('share_income_grossup')
                       * self.share_related_income + self.interest_related_income + self.property_related_income, 0)

        return max(self.salary + self.pension - self.pension_and_income_minimum_deduction + self.parameter('share_income_grossup')
                   * self.share_related_income + self.interest_related_income + self.property_related_income, 0)

    @property
    def state_wealth_tax_basis(self):

        return (self.mutual_fund_wealth_share_comp + self.wealth_in_shares + self.wealth_in_unlisted_shares + self.wealth_ask_shares + self.wealth_fondskonto_shares) * \
            self.parameter('percentage_of_taxable_wealth_cap_shares') + self.bank_deposits + self.property_taxable_value + \
            self.mutual_fund_wealth_interest_comp + \
            self.wealth_fondskonto_cash_interest + self.wealth_ask_cash

    @property
    def pension_deduction_raw(self):
        return max(min(self.pension * self.parameter('pension_deduction_multiplier'),
                       self.parameter('max_pension_deduction')), self.parameter('min_pension_deduction'))

    @property
    def income_deduction_raw(self):
        return max(min(self.salary * self.parameter('deduction_multiplier'),
                       self.parameter('max_deduction_limit')), self.parameter('min_deduction_limit'))

    @property
    def pension_and_income_minimum_deduction(self):
        """
        does what it says
        """

        if (abs(self.pension) < 1e-4) and (abs(self.salary) < 1e-4):
            return 0

        # you can't deduct more than what you earn:
        income_deduction = min(self.income_deduction_raw, self.salary)

        combo_deduction = self.pension_deduction_raw + \
            max(min(self.salary * self.parameter('deduction_multiplier'), self.parameter('max_deduction_limit')),
                min(self.parameter('min_pension_deduction'), self.salary, self.pension))

        return min(max(income_deduction, combo_deduction),
                   self.parameter('max_deduction_limit'))

    @property
    def salary_only_minimum_deduction(self):
        """

        this could be read from db, of course
        https://www.skatteetaten.no/en/rates/minimum-standard-deduction/
        """
        return int(min(self.income_deduction_raw, self.salary))

    @property
    def pension_only_minimum_deduction(self):
        """
        does what it says
        """
        return min(self.pension_deduction_raw, self.pension)

    @property
    def bracket_tax(self):
        """
        Calculates the bracket tax
        """

        tot_inc = self.salary + self.pension

        if tot_inc <= self.parameter('trinnskatt_l1'):
            return 0
        if self.parameter('trinnskatt_l1') < tot_inc <= self.parameter(
                'trinnskatt_l2'):
            return tut.tax_round(self.parameter(
                'trinnskatt_r1') * (tot_inc - self.parameter('trinnskatt_l1')))
        if self.parameter('trinnskatt_l2') < tot_inc <= self.parameter(
                'trinnskatt_l3'):
            return tut.tax_round(self.parameter('trinnskatt_r2') * (tot_inc - self.parameter('trinnskatt_l2')) +
                                 self.parameter('trinnskatt_r1') * (self.parameter('trinnskatt_l2') - self.parameter('trinnskatt_l1')))
        if self.parameter('trinnskatt_l3') < tot_inc <= self.parameter(
                'trinnskatt_l4'):
            return tut.tax_round(self.parameter('trinnskatt_r3') * (tot_inc - self.parameter('trinnskatt_l3')) + self.parameter('trinnskatt_r2') *
                                 (self.parameter('trinnskatt_l3') - self.parameter('trinnskatt_l2')) + self.parameter('trinnskatt_r1') * (self.parameter('trinnskatt_l2') - self.parameter('trinnskatt_l1')))

        return tut.tax_round(self.parameter('trinnskatt_r4') * (tot_inc - self.parameter('trinnskatt_l4')) + self.parameter('trinnskatt_r3') * (self.parameter('trinnskatt_l4') -
                                                                                                                                                self.parameter('trinnskatt_l3')) + self.parameter('trinnskatt_r2') * (self.parameter('trinnskatt_l3') - self.parameter('trinnskatt_l2')) + self.parameter('trinnskatt_r1') * (self.parameter('trinnskatt_l2') - self.parameter('trinnskatt_l1')))

    @property
    def age(self):
        return pd.to_datetime('today').year - self.birth_year

    @property
    def bracket_tax_level(self):
        """
        for debugging the excel sheet
        """

        tot_inc = self.salary + self.pension

        if tot_inc <= self.parameter('trinnskatt_l1'):
            return "Below level 1"

        if self.parameter('trinnskatt_l1') < tot_inc <= self.parameter(
                'trinnskatt_l2'):
            return "Between level 1 and 2"

        if self.parameter('trinnskatt_l2') < tot_inc <= self.parameter(
                'trinnskatt_l3'):
            return "Between lebel 2 and 3"
        if self.parameter('trinnskatt_l3') < tot_inc <= self.parameter(
                'trinnskatt_l4'):
            return "Between level 3 and 4"
        return "Above level 4"

    @property
    def attribute_map(self):
        karta = {'salary': '2.1.1', 'pension': '2.2.1', 'bank_interest_income': '3.1.1',
                 'interest_expenses': '3.3.1', 'property_taxable_value': '4.3.2', 'property_sale_proceeds': '2.8.4',
                 'property_sale_loss': '3.3.6', 'rental_income': '2.8.2', 'bank_deposits': '4.1.1',
                 'gains_from_sale_fondskonto_share_comp': '3.1.4', 'gains_from_sale_fondskonto_interest_comp': '3.1.4',
                 'dividends': '3.1.5', 'mutual_fund_dividends': '3.1.6', 'gains_from_sale_of_shares': '3.1.8',
                 'gains_from_sale_of_shares_ask': '3.1.8'}

        for field in ['mutual_fund_interest_comp_profit', 'mutual_fund_interest_comp_profit_combi_fund',
                   'mutual_fund_share_comp_profit', 'mutual_fund_share_comp_profit_combi_fund']:
            karta[field] = '3.1.9'
        for field in ['loss_fondskonto_shares', 'loss_fondskonto_interest']:
            karta[field] = '3.3.7'
        for field in ['loss_ask_sale', 'loss_from_sale_of_shares']:
            karta[field] = '3.3.8'
        for field in ['loss_from_sale_mutual_fund_share_comp', 'loss_from_sale_mutual_fund_share_comp_combi_fund',
                   'loss_from_sale_mutual_fund_interest_comp', 'loss_from_sale_mutual_fund_interest_comp_combi_fund']:
            karta[field] = '3.3.9'
        karta['mutual_fund_wealth_share_comp'] = '4.1.4'
        karta['mutual_fund_wealth_interest_comp'] = '4.1.5'
        karta['wealth_in_shares'] = '4.1.7'
        for field in ['wealth_in_unlisted_shares',
                   'wealth_ask_cash', 'wealth_ask_shares']:
            karta[field] = '4.1.8'
        for field in ['wealth_fondskonto_cash_interest',
                   'wealth_fondskonto_shares']:
            karta[field] = '4.5.2'
        return karta

    def compare_calculated_tax_vs_correct_tax(
            self, atol=1e-8, rtol=1e-6, check_basis=False):
        """
        compares the config vs our calculations
        It gives a more detailed breakdown so you can compare the components such as different basis etc.
        """

        df_calc = self.tax_breakdown()

        df_true = self.parsed_official_response()

        out = []

        elements = [['Formueskatt stat', 'formueskattTilStat'], ['Formueskatt kommune', 'formueskattTilKommune'],
                    ['Inntektsskatt til kommune', 'inntektsskattTilKommune'], [
                        'Inntektsskatt til fylkeskommune', 'inntektsskattTilFylkeskommune'],
                    ['Fellesskatt', 'fellesskatt'], ['Trinnskatt', 'trinnskatt'], ['Trygdeavgift', 'sumTrygdeavgift'], ['Sum skattefradrag', 'Sum skattefradrag']]

        for calc_comp, correct_comp in elements:
            tax_calc = df_calc.query("Skatt == '%s'" % calc_comp)
            tax_calc_basis = tax_calc['Grunnlag'].item()
            tax_calc_value = tut.tax_round(tax_calc['Beloep'].item())
            # pdb.set_trace()
            # if 'Inntekt' in calc_comp:
            #   pdb.set_trace()
            tax_correct = df_true.query("tax_type == '%s'" % correct_comp)

            if tax_correct.empty:
                tax_correct_basis = 0
            else:
                tax_correct_basis = tax_correct['tax_basis'].item()

            if 'skattefradrag' in calc_comp:
                tax_calc_value *= -1

            if not tax_correct.empty:
                tax_correct_value = tax_correct['tax'].item()
            else:
                tax_correct_value = 0

            error_basis = np.abs(tax_calc_basis - tax_correct_basis)
            tol_basis = atol + rtol * np.abs(tax_correct_basis)

            error_value = np.abs(tax_calc_value - tax_correct_value)
            tol_value = atol + rtol * np.abs(tax_correct_value)

            basis_pass = (error_basis <= tol_basis)
            value_pass = (error_value <= tol_value)

            if check_basis:

                test_string = ''
                if basis_pass and value_pass:
                    test_string = '++'
                elif basis_pass and not value_pass:
                    test_string = '+-'
                elif value_pass and not basis_pass:
                    test_string = '-+'
                else:
                    test_string = '--'
            else:
                test_string = '+' if value_pass else '-'

            if check_basis:
                out.append([calc_comp,
                            tax_calc_basis,
                            tax_correct_basis,
                            tax_calc_value,
                            tax_correct_value,
                            error_basis,
                            error_value,
                            tol_basis,
                            tol_value,
                            test_string])
            else:
                out.append([calc_comp, tax_calc_value, tax_correct_value,
                            error_value, tol_value, test_string])

        # check total tax:
        # pdb.set_trace()
        total_calculated_tax = df_calc.query(
            "Skatt == 'Din Skatt'").Beloep.item()
        total_tax = df_true.query("tax_type == 'total'").tax.item()

        error_value = np.abs(total_calculated_tax - total_tax)
        tol_value = atol + rtol * np.abs(total_tax)

        basis_pass = True
        value_pass = (error_value <= tol_value)

        if check_basis:
            test_string = '+' + '+' if value_pass else '-'
            out.append(['Total skatt', np.nan, np.nan, total_calculated_tax,
                        total_tax, 0, error_value, 0, tol_value, test_string])
        else:
            test_string = '+' if value_pass else '-'
            out.append(['Total skatt', total_calculated_tax,
                        total_tax, error_value, tol_value, test_string])

        if check_basis:
            return pd.DataFrame(out, columns=['component', 'basis_calc', 'basis_corr', 'value_calc',
                                              'value_corr', 'basis_error', 'value_error', 'basis_tol', 'value_tol', 'test_pass'])
        return pd.DataFrame(out, columns=[
                            'component', 'value_calc', 'value_corr', 'value_error', 'value_tol', 'test_pass'])

    def state_wealth_tax(self):
        return self.tax_payable(basis=self.state_wealth_tax_basis, rate=self.parameter(
            'state_wealth_tax_rate'), limit=self.parameter('wealth_tax_lower_limit'))

    def municipal_wealth_tax(self):
        return self.tax_payable(basis=self.state_wealth_tax_basis, rate=self.parameter(
            'municipal_wealth_tax_rate'), limit=self.parameter('wealth_tax_lower_limit'))

    def explain_attribute(self, attr='pension'):
        assert attr in self.attribute_map, "'%s' is not a valid attribute!" % attr
        return self.explain_tax_item(self.attribute_map[attr])

    def explain_tax_item(self, item_no='3.1.8'):
        """
        just show the web-page for the item
        """

        text = item_no.replace('.', '/')
        url = "https://www.skatteetaten.no/person/skatt/skattemelding/finn-post/%s" % text
        return webbrowser.open(url)

    def _income_tax(self, basis_name='felles', apply_rounding=True):
        """
        some gentle indirection
        """

        if basis_name == 'felles':
            return self.tax_payable(basis=self.income_tax_basis, rate=self.parameter('felles_tax_rate'),
                                    deduction=self.parameter('personal_deduction'), apply_rounding=apply_rounding)
        if basis_name == 'fylke':

            return self.tax_payable(basis=self.income_tax_basis, rate=self.parameter('fylke_tax_rate'),
                                    deduction=self.parameter('personal_deduction'), apply_rounding=apply_rounding)

        if basis_name == 'kommun':

            return self.tax_payable(basis=self.income_tax_basis, rate=self.parameter('municipal_tax_rate'),
                                    deduction=self.parameter('personal_deduction'), apply_rounding=apply_rounding)

        raise Exception(
            "We only basis in {felles, fylke, kommun}, not '%s'" %
            basis_name)

    def municipal_income_tax(self):
        return self._income_tax(basis_name='kommun')

    def common_income_tax(self):
        return self._income_tax(basis_name='felles')

    def county_income_tax(self):
        return self._income_tax(basis_name='fylke')

    def national_insurance(self, apply_rounding=False):
        """
        [NO]
        seems to be 8.2% above 81.4k, goes up linearly from low limit to that?
        ah, it can't be more than 25% of the amount above the lower limit (this isn't mentioned on the official site)
        https://no.wikipedia.org/wiki/Trygdeavgift

        """

        rate = self.parameter('trygde_rate')

        if self.age > self.parameter('trygde_rate_cutoff_age_hi') or self.age < self.parameter(
                'trygde_rate_cutoff_age_lo'):
            rate = self.parameter('trygde_rate_extreme')

        income = self.salary + self.pension
        if income <= self.parameter('trygde_income_limit'):
            return 0
        overshooting_income = income - self.parameter('trygde_income_limit')
        # share_of_overshooting =
        raw_tax = rate * self.salary + \
            self.parameter('trygde_rate_pension') * self.pension
        if raw_tax >= self.parameter('trygde_max_share') * overshooting_income:
            ans = self.parameter('trygde_max_share') * overshooting_income
            if apply_rounding:
                return tut.tax_round(ans)
            return ans

        if apply_rounding:
            return tut.tax_round(raw_tax)
        return raw_tax

    def deduction(self):
        if self.pension > 0:
            max_ded = self.parameter(
                'max_pension_tax_deduction') * (self.pension_percent / 100) * (self.pension_months / 12)
            # pdb.set_trace()
            reduction_stage1 = self.parameter(
                'pension_deduction_stage_one_threshold') * (self.pension_percent / 100) * (self.pension_months / 12)
            red_rate1 = self.parameter(
                'stage_one_reduction_rate')
            reduction_stage2 = self.parameter(
                'pension_deduction_stage_two_threshold') * (self.pension_percent / 100) * (self.pension_months / 12)
            red_rate2 = self.parameter(
                'stage_two_reduction_rate')
            cutoff = min(np.round(max_ded -
                                  ((min(self.pension, reduction_stage2) -
                                    reduction_stage1) *
                                   red_rate1 +
                                   max((self.pension -
                                        reduction_stage2) *
                                       red_rate2, 0)), 0), max_ded)
            deductions = self.municipal_income_tax() + self.county_income_tax() + \
                self.common_income_tax() + self.bracket_tax + self.national_insurance()
            return max(min(cutoff, deductions), 0)

        return 0

    def tax(self, apply_rounding=True):
        if apply_rounding:
            return tut.tax_round(self.state_wealth_tax()) + tut.tax_round(self.municipal_wealth_tax()) + tut.tax_round(self.municipal_income_tax()) + tut.tax_round(
                self.county_income_tax()) + tut.tax_round(self.common_income_tax()) + tut.tax_round(self.bracket_tax) + tut.tax_round(self.national_insurance()) - tut.tax_round(self.deduction())
        return self.state_wealth_tax() + self.municipal_wealth_tax() + self.municipal_income_tax() + self.county_income_tax() + \
            self.common_income_tax() + self.bracket_tax + \
            self.national_insurance() - self.deduction()

    def tax_breakdown(self):

        out = [['Formueskatt stat', self.state_wealth_tax_basis, self.state_wealth_tax()], [
            'Formueskatt kommune', self.state_wealth_tax_basis, self.municipal_wealth_tax()]]

        out += [['Inntektsskatt til kommune', self.income_tax_basis, self.municipal_income_tax()], ['Inntektsskatt til fylkeskommune', self.income_tax_basis, self.county_income_tax()],
                ['Fellesskatt', self.income_tax_basis, self.common_income_tax()], ['Trinnskatt', self.salary + self.pension, self.bracket_tax], ['Trygdeavgift', self.salary + self.pension, self.national_insurance()]]

        out += [['Sum skattefradrag', 0, self.deduction()]]
        # if apply_rounding:
        out += [['Din Skatt', np.nan, self.tax()]]

        return pd.DataFrame(out, columns=['Skatt', 'Grunnlag', 'Beloep'])


    def display_online_breakdown(self, refresh=False, session=None):
        """
        this is the online ('true') figures
        """
        frame = self.parsed_official_response()

        orig_df = frame.copy()
        frame.tax = frame.tax.map(tut.big_fmt)
        frame.tax_basis = frame.tax_basis.map(tut.big_fmt)

        for col in ['tax_basis', 'tax']:
            frame.loc[1, col] = ''

        tut.display_df(frame)
        return orig_df

    def parsed_official_response(self, refresh=False, session=None):
        resp = self.query_web_for_tax_results(refresh=refresh, session=session)
        # pdb.set_trace()
        raw = resp.json()
        data = raw['hovedperson']['beregnetSkattV3']['skattOgAvgift']

        correct_tax = raw['hovedperson']['beregnetSkattV3']['informasjonTilSkattelister']['beregnetSkatt']

        # if we don't have any wealth, we won't have those wealth tax keys in
        # data, seems we don't have deduction keys either?
        items = [
            'inntektsskattTilKommune',
            'inntektsskattTilFylkeskommune',
            'fellesskatt',
            'trinnskatt',
            'sumTrygdeavgift',
            'formueskattTilStat',
            'formueskattTilKommune']

        missed_items = list(set(data.keys()) - set(items))

        deductions = raw['hovedperson']['beregnetSkattV3'].get(
            'sumSkattefradrag', {}).get('beloep', 0)

        if len(missed_items) > 0:
            print("Did not use these items: %s" % (','.join(missed_items)))
            # pdb.set_trace()

        not_in_res = list(set(items) - set(data.keys()))

        if len(not_in_res) > 0:
            print(
                "Did not find these items in response: %s" %
                (','.join(not_in_res)))
        out = [['Salary', self.salary, 0], ['', 0, 0]]
        for item in items:
            try:
                out.append(
                    [item, data[item]['grunnlag'], data[item]['beloep']])
            except Exception:
                # print(err.msg)
                out.append([item, 0, 0])

        if deductions != 0:
            out.append(['Sum skattefradrag', 0, -deductions])

        frame = pd.DataFrame(out, columns=['tax_type', 'tax_basis', 'tax'])
        assert abs(frame.tax.sum() - correct_tax) < 1e-4, "Estimated tax differs from the true tax! (%s vs %s)" % (
            tut.big_fmt(frame.tax.sum()), tut.big_fmt(correct_tax))
        frame = frame.append({'tax_type': 'total',
                              'tax_basis': 0,
                              'tax': frame.tax.sum()},
                             ignore_index=True)
        return frame

    def official_tax(self, session=None, refresh=False):
        frame = self.parsed_official_response(refresh=refresh, session=session)

        # pdb.set_trace()
        return frame.query("tax_type == 'total'").tax.sum()
        # return frame

    def payload(self):
        age = pd.to_datetime('today').year - self.birth_year

        base = {'skatteberegningsgrunnlagV6': {'skattegrunnlagsobjekt':
                                               [{'beloep': self.salary, 'brukIKalkulator': 'BrukesDirekte', 'id': 'vF4DxZz4O', 'ledetekst': 'Lønn, naturalytelser mv.',
                                                 'postnummer': '2.1.1', 'sorteringsNoekkel': '020101', 'tekniskNavn': 'loennsinntektNaturalytelseMv', 'temakategori': 'arbeidTrygdPensjon', 'temaunderkategori': 'loennsinntekter', 'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                {'beloep': self.pension, 'brukIKalkulator': 'BrukesDirekte', 'id': 'vF4DxZz4O', 'ledetekst': 'Lønn, naturalytelser mv.',
                                                 'postnummer': '2.2.1', 'sorteringsNoekkel': '020201', 'tekniskNavn': 'alderspensjonFraFolketrygden', 'temakategori': 'arbeidTrygdPensjon', 'temaunderkategori': 'pensjonTrygdInntekt', 'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml',
                                                 'antallMaanederMedPensjon': self.pension_months, 'gjennomsnittligVektetPensjonsgrad': self.pension_percent},
                                                   {
                                                   'beloep': self.bank_interest_income,
                                                   'brukIKalkulator': 'BrukesDirekte',
                                                   'id': 'RCc8osmg4y',
                                                   'ledetekst': 'Renter på bankinnskudd',
                                                   'postnummer': '3.1.1',
                                                   'sorteringsNoekkel': '030101',
                                                   'tekniskNavn': 'opptjenteRenter',
                                                   'temakategori': 'bankLaanForsikring',
                                                   'temaunderkategori': 'bankInntekt',
                                                   'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                   {'beloep': self.interest_expenses,
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': 'fLHS8kFE8m',
                                                    'ledetekst': 'Gjeldsrenter',
                                                    'postnummer': '3.3.1',
                                                    'sorteringsNoekkel': '030301',
                                                    'tekniskNavn': 'paaloepteRenter',
                                                    'temakategori': 'bankLaanForsikring',
                                                    'temaunderkategori': 'bankLaanForsikringFradrag',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},

                                                   {'beloep': self.property_taxable_value,
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': '4ZImlzCPBc',
                                                    'ledetekst': 'Formuesverdi primærbolig',
                                                    'postnummer': '4.3.2',
                                                    'sorteringsNoekkel': '040302',
                                                    'tekniskNavn': 'formuesverdiForPrimaerbolig',
                                                    'temakategori': 'boligOgEiendeler',
                                                    'temaunderkategori': 'boligEindelerFormue',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},

                                                   {"ledetekst": "Gevinst ved salg av eiendom",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "boligOgEiendeler",
                                                    "sorteringsNoekkel": "020804",
                                                    "beloep": self.property_sale_proceeds,
                                                    "autofokus": True,
                                                    "postnummer": "2.8.4",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvFastEiendomMv",
                                                    "temaunderkategori": "boligEindelerInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "Dstg2w_w1"},
                                                   {
                                                   "ledetekst": "Tap ved salg av fast eiendom",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "boligOgEiendeler",
                                                   "sorteringsNoekkel": "030306",
                                                   "beloep": self.property_sale_loss,
                                                   "autofokus": True,
                                                   "postnummer": "3.3.6",
                                                   "tekniskNavn": "fradragsberettigetTapVedRealisasjonAvFastEiendom",
                                                   "temaunderkategori": "boligEindelerFradrag",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "4Go51ns0D"},
                                                   {
                                                   "ledetekst": "Utleie av fast eiendom",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "boligOgEiendeler",
                                                   "sorteringsNoekkel": "020802",
                                                   "beloep": self.rental_income,
                                                   "autofokus": True,
                                                   "postnummer": "2.8.2",
                                                   "tekniskNavn": "nettoinntektVedUtleieAvFastEiendomMv",
                                                   "temaunderkategori": "boligEindelerInntekt",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "in6py-mIs"},
                                                   {'beloep': self.bank_deposits,
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': '3JUkH5xoKm',
                                                    'ledetekst': 'Bankinnskudd',
                                                    'postnummer': '4.1.1',
                                                    'sorteringsNoekkel': '040101',
                                                    'tekniskNavn': 'innskudd',
                                                    'temakategori': 'bankLaanForsikring',
                                                    'temaunderkategori': 'bankLaanForsikringFormue',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                   {'beloep': '',
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': '29Ppf_wkm5',
                                                    'ledetekst': 'Gjeld',
                                                    'postnummer': '4.8.1',
                                                    'sorteringsNoekkel': '040801',
                                                    'tekniskNavn': 'gjeld',
                                                    'temakategori': 'bankLaanForsikring',
                                                    'temaunderkategori': 'bankLaanForsikringGjeld',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},

                                                   # this seems to be the equivalent of "kapitalförsäkring" in
                                                   # Sweden?
                                                   {'autofokus': True,
                                                    'beloep': self.gains_from_sale_fondskonto_share_comp,
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': 'cMr5mI4QB',
                                                    'ledetekst': 'Gevinst ved salg av fondskonto aksjedel',
                                                    'postnummer': '3.1.4',
                                                    'sorteringsNoekkel': '030104',
                                                    'tekniskNavn': 'gevinstVedRealisasjonAvOgUttakFraAksjedelIFondskonto',
                                                    'temakategori': 'finans',
                                                    'temaunderkategori': 'aksjeInntekt',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                   {"ledetekst": "Gevinst ved salg av fondskonto rentedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030104",
                                                    "beloep": self.gains_from_sale_fondskonto_interest_comp,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.4",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvOgUttakFraRentedelIFondskonto",
                                                    "temaunderkategori": "finansAnnetInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "2HEy2XMhn"},
                                                   # the below must be an
                                                   # rarely used case? Leave it
                                                   # for now
                                                   {
                                                   'autofokus': True,
                                                   'beloep': self.gains_from_sale_of_shares,
                                                   'brukIKalkulator': 'BrukesDirekte',
                                                   'id': 'XJsESPp3E',
                                                   'ledetekst': 'Gevinst ved salg av aksjer fra Aksjeoppgaven/utenlandske aksjer i norske banker',
                                                   'postnummer': '3.1.8',
                                                   'sorteringsNoekkel': '030108',
                                                   'tekniskNavn': 'gevinstVedRealisasjonAvAksje',
                                                   'temakategori': 'finans',
                                                   'temaunderkategori': 'aksjeInntekt',
                                                   'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                   # this is ask I believe? Or is it any sale of shares? Presumably,
                                                   # because you punch in the net gains, so could already be taking
                                                   # the ask-rules into account (postnummer is important, that
                                                   # identifies the item and
                                                   # its explanation)
                                                   {
                                                   "ledetekst": "Gevinst salg fra aksjesparekonto",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "030108",
                                                   "beloep": self.gains_from_sale_of_shares_ask,
                                                   "autofokus": True,
                                                   "postnummer": "3.1.8",
                                                   "tekniskNavn": "gevinstVedRealisasjonAvAksjesparekonto",
                                                   "temaunderkategori": "aksjeInntekt",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "spyaYFHUh"},
                                                   {"ledetekst": "Tap fondskonto aksjedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030307",
                                                    "beloep": self.loss_fondskonto_shares,
                                                    "autofokus": True,
                                                    "postnummer": "3.3.7",
                                                    "tekniskNavn": "tapVedRealisajonAvOgUttakFraAksjedelIFondskonto",
                                                    "temaunderkategori": "aksjeFradrag",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "vt-OPCZkD"},
                                                   {
                                                   "ledetekst": "Tap salg aksjesparekonto",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "030308",
                                                   "beloep": self.loss_ask_sale,
                                                   "autofokus": True,
                                                   "postnummer": "3.3.8",
                                                   "tekniskNavn": "tapVedRealisasjonAvAksjesparekonto",
                                                   "temaunderkategori": "aksjeFradrag",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "E5WH7AuF-"},
                                                   {"ledetekst": "Tap ved salg av aksjer fra aksjeoppgaven/Tap utenlandske aksjer fra norske banker",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030308",
                                                    "beloep": self.loss_from_sale_of_shares,
                                                    "autofokus": True,
                                                    "postnummer": "3.3.8",
                                                    "tekniskNavn": "tapVedRealisasjonAvAksje",
                                                    "temaunderkategori": "aksjeFradrag",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "hGkhnFQoz"},
                                                   {
                                                   "ledetekst": "Tap salg verdipapirfond aksjedel",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "030309",
                                                   "beloep": self.loss_from_sale_mutual_fund_share_comp,
                                                   "autofokus": True,
                                                   "postnummer": "3.3.9",
                                                   "tekniskNavn": "tapVedRealisasjonAvVerdipapirfondsandelKnyttetTilAksjedel",
                                                   "temaunderkategori": "aksjeFradrag",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "yQRUlIE-X"},
                                                   {"ledetekst": "Tap salg verdipapirfond aksjedel kombifond",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030309",
                                                    "beloep": self.loss_from_sale_mutual_fund_share_comp_combi_fund,
                                                    "autofokus": True,
                                                    "postnummer": "3.3.9",
                                                    "tekniskNavn": "tapVedRealisasjonAvVerdipapirfondsandelIKombifondKnyttetTilAksjedel",
                                                    "temaunderkategori": "aksjeFradrag",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "XLZ4CAWOS"},
                                                   {"ledetekst": "Tap fondskonto rentedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030307",
                                                    "beloep": self.loss_fondskonto_interest,
                                                    "autofokus": True,
                                                    "postnummer": "3.3.7",
                                                    "tekniskNavn": "tapVedRealisasjonAvOgUttakFraRentedelIFondskonto",
                                                    "temaunderkategori": "finansAnnetFradrag",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "_RMwr8GX4"},
                                                   {"ledetekst": "Tap salg verdipapirfond rentedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030309",
                                                    "beloep": self.loss_from_sale_mutual_fund_interest_comp,
                                                    "autofokus": True,
                                                    "postnummer": "3.3.9",
                                                    "tekniskNavn": "tapVedRealisasjonAvVerdipapirfondsandelKnyttetTilRentedel",
                                                    "temaunderkategori": "finansAnnetFradrag",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "yt3gvatEk"},
                                                   {
                                                   "ledetekst": "Tap salg verdipapirfond rentedel kombifond",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "030309",
                                                   "beloep": self.loss_from_sale_mutual_fund_interest_comp_combi_fund,
                                                   "autofokus": True,
                                                   "postnummer": "3.3.9",
                                                   "tekniskNavn": "tapVedRealisasjonAvVerdipapirfondsandelIKombifondKnyttetTilRentedel",
                                                   "temaunderkategori": "finansAnnetFradrag",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "OGTFIxE8l"},
                                                   {
                                                   "ledetekst": "Formue andeler i verdipapirfond – aksjedel",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "040104",
                                                   "beloep": self.mutual_fund_wealth_share_comp,
                                                   "autofokus": True,
                                                   "postnummer": "4.1.4",
                                                   "tekniskNavn": "verdiFoerVerdsettingsrabattForVerdipapirfondsandelKnyttetTilAksjedel",
                                                   "temaunderkategori": "aksjeFormue",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "Y8VYl5ZIt"},
                                                   {
                                                   "ledetekst": "Formue andeler i verdipapirfond - rentedel",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "040105",
                                                   "beloep": self.mutual_fund_wealth_interest_comp,
                                                   "autofokus": True,
                                                   "postnummer": "4.1.5",
                                                   "tekniskNavn": "formuesverdiForVerdipapirfondsandelKnyttetTilRentedel",
                                                   "temaunderkategori": "finansAnnetFormue",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "_9Y7rjtnc"},
                                                   {
                                                   "ledetekst": "Formuesverdi av aksjer mv.",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "040107",
                                                   "beloep": self.wealth_in_shares,
                                                   "autofokus": True,
                                                   "postnummer": "4.1.7",
                                                   "tekniskNavn": "verdiFoerVerdsettingsrabattForAksjeIVPS",
                                                   "temaunderkategori": "aksjeFormue",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "oQsYwc3ug"},
                                                   {"ledetekst": "Formue norske aksjer/Formue utenlandske aksjer fra norske banker",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "040108",
                                                    "beloep": self.wealth_in_unlisted_shares,
                                                    "autofokus": True,
                                                    "postnummer": "4.1.8",
                                                    "tekniskNavn": "verdiFoerVerdsettingsrabattForAksje",
                                                    "temaunderkategori": "aksjeFormue",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "2iZ7mXh1g"},
                                                   {"ledetekst": "Formue aksjesparekonto - kontanter",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "040108",
                                                    "beloep": self.wealth_ask_cash,
                                                    "autofokus": True,
                                                    "postnummer": "4.1.8",
                                                    "tekniskNavn": "formuesverdiForKontanterIAksjesparekonto",
                                                    "temaunderkategori": "finansAnnetFormue",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "znfRNpWHa"},
                                                   {"ledetekst": "Formue fondskonto kontant/rentedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "040502",
                                                    "beloep": self.wealth_fondskonto_cash_interest,
                                                    "autofokus": True,
                                                    "postnummer": "4.5.2",
                                                    "tekniskNavn": "formuesverdiForKontanterMvIFondskonto",
                                                    "temaunderkategori": "finansAnnetFormue",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "G6DfOhyqx"},
                                                   {
                                                   "ledetekst": "Formue aksjesparekonto - aksjedel",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "040108",
                                                   "beloep": self.wealth_ask_shares,
                                                   "autofokus": True,
                                                   "postnummer": "4.1.8",
                                                   "tekniskNavn": "verdiFoerVerdsettingsrabattForAksjedelIAksjesparekonto",
                                                   "temaunderkategori": "aksjeFormue",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "zXZJsFeLo"},
                                                   {"ledetekst": "Formue fondskonto aksjedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "040502",
                                                    "beloep": self.wealth_fondskonto_shares,
                                                    "autofokus": True,
                                                    "postnummer": "4.5.2",
                                                    "tekniskNavn": "verdiFoerVerdsettingsrabattForAksjeOgAksjefondIFondskonto",
                                                    "temaunderkategori": "aksjeFormue",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "_XmJTs4k8"},
                                                   {"ledetekst": "Gevinst salg verdipapirfond rentedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030109",
                                                    "beloep": self.mutual_fund_interest_comp_profit,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.9",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvVerdipapirfondsandelKnyttetTilRentedel",
                                                    "temaunderkategori": "finansAnnetInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "3keEJTbpe"},
                                                   {"ledetekst": "Gevinst salg verdipapirfond rentedel kombifond",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030109",
                                                    "beloep": self.mutual_fund_interest_comp_profit_combi_fund,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.9",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvVerdipapirfondsandelIKombifondKnyttetTilRentedel",
                                                    "temaunderkategori": "finansAnnetInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "9MwMeA8Ck"},
                                                   {"ledetekst": "Gevinst ved salg av fondskonto aksjedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030104",
                                                    "beloep": 0,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.4",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvOgUttakFraAksjedelIFondskonto",
                                                    "temaunderkategori": "aksjeInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "8B1puNRK4"},
                                                   {
                                                   "ledetekst": "Skattepliktig utbytte fra Aksjeoppgaven/utenlandske aksjer fra norske banker",
                                                   "brukIKalkulator": "BrukesDirekte",
                                                   "temakategori": "finans",
                                                   "sorteringsNoekkel": "030105",
                                                   "beloep": self.dividends,
                                                   "autofokus": True,
                                                   "postnummer": "3.1.5",
                                                   "tekniskNavn": "utbytteFraAksje",
                                                   "temaunderkategori": "aksjeInntekt",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "AuHD5aILi"},
                                                   {"ledetekst": "Utbytte/utdeling verdipapirfond",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030106",
                                                    "beloep": self.mutual_fund_dividends,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.6",
                                                    "tekniskNavn": "skattepliktigUtbytteFraVerdipapirfondsandel",
                                                    "temaunderkategori": "aksjeInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "Gh76es4Y5"},
                                                   # { "ledetekst": "Gevinst ved salg av aksjer fra Aksjeoppgaven/utenlandske aksjer i norske banker", "brukIKalkulator": "BrukesDirekte", "temakategori": "finans", "sorteringsNoekkel": "030108", "beloep": 0, "autofokus": True, "postnummer": "3.1.8", "tekniskNavn": "gevinstVedRealisasjonAvAksje", "temaunderkategori": "aksjeInntekt", "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml", "id": "4S0kLvk1l"},
                                                   {"ledetekst": "Gevinst salg verdipapirfond aksjedel",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030109",
                                                    "beloep": self.mutual_fund_share_comp_profit,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.9",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvVerdipapirfondsandelKnyttetTilAksjedel",
                                                    "temaunderkategori": "aksjeInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "CixZRINes"},
                                                   {"ledetekst": "Gevinst salg verdipapirfond aksjedel kombifond",
                                                    "brukIKalkulator": "BrukesDirekte",
                                                    "temakategori": "finans",
                                                    "sorteringsNoekkel": "030109",
                                                    "beloep": self.mutual_fund_share_comp_profit_combi_fund,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.9",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvVerdipapirfondsandelIKombifondKnyttetTilAksjedel",
                                                    "temaunderkategori": "aksjeInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "ccob_mQEQ"},
                                                ]},
                'skattepliktV8': {'skattesubjekt': {'personligSkattesubjekt': {'alderIInntektsaar': '%d' % age, 'skattepliktTilNorge': 'GLOBAL', 'tolvdelVedArbeidsoppholdINorge': '12'}, 'skattested': self.municipality, 'skattestedITiltakssone': False}}}

        return base
