import os
import json
import pdb
import webbrowser
import re
import itertools
import configparser
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
import tax_utils as tut


def tax_url(tax_year):
    """
    what it looks like, this is the main endpoint
    """
    return "https://skatteberegning.app.skatteetaten.no/%d" % tax_year


def headers():
    """
    [NO]
    """
    return {'Content-Type': 'application/json'}


def payload(salary=0, birth_year=1978, municipality='0402', tax_year=None, gains_from_sale_fondskonto_share_comp=0, gains_from_sale_fondskonto_interest_comp=0, gains_from_sale_of_shares_ask=0, property_taxable_value=0, pension=0, pension_months=12, pension_percent=100, property_sale_proceeds=0, rental_income=0, property_sale_loss=0, bank_deposits=0,
            bank_interest_income=0, interest_expenses=0, dividends=0, mutual_fund_dividends=0, gains_from_sale_of_shares=0, mutual_fund_interest_comp_profit=0, mutual_fund_interest_comp_profit_combi_fund=0,
            mutual_fund_share_comp_profit=0, mutual_fund_share_comp_profit_combi_fund=0, loss_fondskonto_shares=0, loss_fondskonto_interest=0, loss_ask_sale=0, loss_from_sale_of_shares=0, loss_from_sale_mutual_fund_share_comp_combi_fund=0,
            loss_from_sale_mutual_fund_share_comp=0, loss_from_sale_mutual_fund_interest_comp=0, loss_from_sale_mutual_fund_interest_comp_combi_fund=0, mutual_fund_wealth_share_comp=0, mutual_fund_wealth_interest_comp=0, wealth_in_shares=0,
            wealth_in_unlisted_shares=0, wealth_ask_cash=0, wealth_ask_shares=0, wealth_fondskonto_cash_interest=0, wealth_fondskonto_shares=0):
    """



    For 2021:
    postnummer doesn't seem to matter (note there's a duplicated line in the boilerplate below)

    """
    if tax_year is None:
        tax_year = pd.to_datetime('today').year
    # age = int(np.floor((pd.to_datetime('today') - dob).days/365.2422))
    age = pd.to_datetime('today').year - birth_year
    if tax_year == 2021:
        # base = json.loads(lw.read_json_file('ntax.json'))

        base = {'skatteberegningsgrunnlagV6': {'skattegrunnlagsobjekt':
                                               [{'beloep': salary, 'brukIKalkulator': 'BrukesDirekte', 'id': 'vF4DxZz4O', 'ledetekst': 'Lønn, naturalytelser mv.',
                                                 'postnummer': '2.1.1', 'sorteringsNoekkel': '020101', 'tekniskNavn': 'loennsinntektNaturalytelseMv', 'temakategori': 'arbeidTrygdPensjon', 'temaunderkategori': 'loennsinntekter', 'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                {'beloep': pension, 'brukIKalkulator': 'BrukesDirekte', 'id': 'vF4DxZz4O', 'ledetekst': 'Lønn, naturalytelser mv.',
                                                 'postnummer': '2.2.1', 'sorteringsNoekkel': '020201', 'tekniskNavn': 'alderspensjonFraFolketrygden', 'temakategori': 'arbeidTrygdPensjon', 'temaunderkategori': 'pensjonTrygdInntekt', 'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml',
                                                 'antallMaanederMedPensjon': pension_months, 'gjennomsnittligVektetPensjonsgrad': pension_percent},
                                                   {
                                                   'beloep': bank_interest_income,
                                                   'brukIKalkulator': 'BrukesDirekte',
                                                   'id': 'RCc8osmg4y',
                                                   'ledetekst': 'Renter på bankinnskudd',
                                                   'postnummer': '3.1.1',
                                                   'sorteringsNoekkel': '030101',
                                                   'tekniskNavn': 'opptjenteRenter',
                                                   'temakategori': 'bankLaanForsikring',
                                                   'temaunderkategori': 'bankInntekt',
                                                   'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},
                                                   {'beloep': interest_expenses,
                                                    'brukIKalkulator': 'BrukesDirekte',
                                                    'id': 'fLHS8kFE8m',
                                                    'ledetekst': 'Gjeldsrenter',
                                                    'postnummer': '3.3.1',
                                                    'sorteringsNoekkel': '030301',
                                                    'tekniskNavn': 'paaloepteRenter',
                                                    'temakategori': 'bankLaanForsikring',
                                                    'temaunderkategori': 'bankLaanForsikringFradrag',
                                                    'type': 'ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml'},

                                                   {'beloep': property_taxable_value,
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
                                                    "beloep": property_sale_proceeds,
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
                                                   "beloep": property_sale_loss,
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
                                                   "beloep": rental_income,
                                                   "autofokus": True,
                                                   "postnummer": "2.8.2",
                                                   "tekniskNavn": "nettoinntektVedUtleieAvFastEiendomMv",
                                                   "temaunderkategori": "boligEindelerInntekt",
                                                   "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                   "id": "in6py-mIs"},
                                                   {'beloep': bank_deposits,
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
                                                    'beloep': gains_from_sale_fondskonto_share_comp,
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
                                                    "beloep": gains_from_sale_fondskonto_interest_comp,
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
                                                   'beloep': gains_from_sale_of_shares,
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
                                                   "beloep": gains_from_sale_of_shares_ask,
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
                                                    "beloep": loss_fondskonto_shares,
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
                                                   "beloep": loss_ask_sale,
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
                                                    "beloep": loss_from_sale_of_shares,
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
                                                   "beloep": loss_from_sale_mutual_fund_share_comp,
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
                                                    "beloep": loss_from_sale_mutual_fund_share_comp_combi_fund,
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
                                                    "beloep": loss_fondskonto_interest,
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
                                                    "beloep": loss_from_sale_mutual_fund_interest_comp,
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
                                                   "beloep": loss_from_sale_mutual_fund_interest_comp_combi_fund,
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
                                                   "beloep": mutual_fund_wealth_share_comp,
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
                                                   "beloep": mutual_fund_wealth_interest_comp,
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
                                                   "beloep": wealth_in_shares,
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
                                                    "beloep": wealth_in_unlisted_shares,
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
                                                    "beloep": wealth_ask_cash,
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
                                                    "beloep": wealth_fondskonto_cash_interest,
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
                                                   "beloep": wealth_ask_shares,
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
                                                    "beloep": wealth_fondskonto_shares,
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
                                                    "beloep": mutual_fund_interest_comp_profit,
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
                                                    "beloep": mutual_fund_interest_comp_profit_combi_fund,
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
                                                   "beloep": dividends,
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
                                                    "beloep": mutual_fund_dividends,
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
                                                    "beloep": mutual_fund_share_comp_profit,
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
                                                    "beloep": mutual_fund_share_comp_profit_combi_fund,
                                                    "autofokus": True,
                                                    "postnummer": "3.1.9",
                                                    "tekniskNavn": "gevinstVedRealisasjonAvVerdipapirfondsandelIKombifondKnyttetTilAksjedel",
                                                    "temaunderkategori": "aksjeInntekt",
                                                    "type": "ske.fastsetting.skatt.skattegrunnlag.v2_0.SkattegrunnlagsobjektXml",
                                                    "id": "ccob_mQEQ"},
                                                ]},
                'skattepliktV8': {'skattesubjekt': {'personligSkattesubjekt': {'alderIInntektsaar': '%d' % age, 'skattepliktTilNorge': 'GLOBAL', 'tolvdelVedArbeidsoppholdINorge': '12'}, 'skattested': municipality, 'skattestedITiltakssone': False}}}

    else:
        raise Exception("Only tax year == 2021 implemented and tested")

    return base


def tax_query(salary=0, municipality='0402', birth_year=1978, tax_year=None, refresh=False, gains_from_sale_fondskonto_share_comp=0, gains_from_sale_fondskonto_interest_comp=0, gains_from_sale_of_shares_ask=0, property_taxable_value=0, pension=0, pension_months=12, pension_percent=100, property_sale_proceeds=0, rental_income=0, property_sale_loss=0, bank_deposits=0,
              bank_interest_income=0, interest_expenses=0, dividends=0, mutual_fund_dividends=0, gains_from_sale_of_shares=0, mutual_fund_interest_comp_profit=0, mutual_fund_interest_comp_profit_combi_fund=0, mutual_fund_share_comp_profit=0, mutual_fund_share_comp_profit_combi_fund=0, loss_fondskonto_shares=0, loss_fondskonto_interest=0, loss_ask_sale=0,
              loss_from_sale_of_shares=0, loss_from_sale_mutual_fund_share_comp=0, loss_from_sale_mutual_fund_share_comp_combi_fund=0, loss_from_sale_mutual_fund_interest_comp=0,
              loss_from_sale_mutual_fund_interest_comp_combi_fund=0, mutual_fund_wealth_share_comp=0, mutual_fund_wealth_interest_comp=0, wealth_in_shares=0, wealth_in_unlisted_shares=0, wealth_ask_cash=0, wealth_ask_shares=0, wealth_fondskonto_cash_interest=0, wealth_fondskonto_shares=0, session=None):
    """

    return the raw data from server
    """

    if tax_year is None:
        tax_year = pd.to_datetime('today').year
    if session is None:
        res = tut.get_request(tax_url(tax_year), payload_=payload(birth_year=birth_year, salary=salary, municipality=municipality, tax_year=tax_year, gains_from_sale_fondskonto_share_comp=gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask=gains_from_sale_of_shares_ask, property_taxable_value=property_taxable_value, pension=pension, pension_months=pension_months, pension_percent=pension_percent, property_sale_proceeds=property_sale_proceeds, rental_income=rental_income, property_sale_loss=property_sale_loss, bank_deposits=bank_deposits,
                                                                  bank_interest_income=bank_interest_income, interest_expenses=interest_expenses, gains_from_sale_fondskonto_interest_comp=gains_from_sale_fondskonto_interest_comp, dividends=dividends, mutual_fund_dividends=mutual_fund_dividends, gains_from_sale_of_shares=gains_from_sale_of_shares,
                                                                  mutual_fund_interest_comp_profit=mutual_fund_interest_comp_profit, mutual_fund_interest_comp_profit_combi_fund=mutual_fund_interest_comp_profit_combi_fund, mutual_fund_share_comp_profit=mutual_fund_share_comp_profit, loss_fondskonto_shares=loss_fondskonto_shares, loss_fondskonto_interest=loss_fondskonto_interest, loss_ask_sale=loss_ask_sale,
                                                                  mutual_fund_share_comp_profit_combi_fund=mutual_fund_share_comp_profit_combi_fund, loss_from_sale_of_shares=loss_from_sale_of_shares, loss_from_sale_mutual_fund_share_comp=loss_from_sale_mutual_fund_share_comp, loss_from_sale_mutual_fund_share_comp_combi_fund=loss_from_sale_mutual_fund_share_comp_combi_fund, loss_from_sale_mutual_fund_interest_comp=loss_from_sale_mutual_fund_interest_comp,
                                                                  loss_from_sale_mutual_fund_interest_comp_combi_fund=loss_from_sale_mutual_fund_interest_comp_combi_fund, mutual_fund_wealth_share_comp=mutual_fund_wealth_share_comp, mutual_fund_wealth_interest_comp=mutual_fund_wealth_interest_comp, wealth_in_shares=wealth_in_shares, wealth_in_unlisted_shares=wealth_in_unlisted_shares, wealth_ask_cash=wealth_ask_cash, wealth_ask_shares=wealth_ask_shares, wealth_fondskonto_cash_interest=wealth_fondskonto_cash_interest,
                                                                  wealth_fondskonto_shares=wealth_fondskonto_shares), headers_=headers(), method='post', refresh=refresh)
    else:
        # print("doing request post")
        # try:
        payload_ = payload(salary=salary, birth_year=birth_year, municipality=municipality, tax_year=tax_year, gains_from_sale_fondskonto_share_comp=gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask=gains_from_sale_of_shares_ask, property_taxable_value=property_taxable_value, pension=pension, pension_months=pension_months, pension_percent=pension_percent, property_sale_proceeds=property_sale_proceeds, rental_income=rental_income, property_sale_loss=property_sale_loss, bank_deposits=bank_deposits,
                           bank_interest_income=bank_interest_income, interest_expenses=interest_expenses, gains_from_sale_fondskonto_interest_comp=gains_from_sale_fondskonto_interest_comp, dividends=dividends, mutual_fund_dividends=mutual_fund_dividends, gains_from_sale_of_shares=gains_from_sale_of_shares,
                           mutual_fund_interest_comp_profit=mutual_fund_interest_comp_profit, mutual_fund_interest_comp_profit_combi_fund=mutual_fund_interest_comp_profit_combi_fund, mutual_fund_share_comp_profit=mutual_fund_share_comp_profit, loss_fondskonto_shares=loss_fondskonto_shares, loss_fondskonto_interest=loss_fondskonto_interest, loss_ask_sale=loss_ask_sale,
                           mutual_fund_share_comp_profit_combi_fund=mutual_fund_share_comp_profit_combi_fund, loss_from_sale_of_shares=loss_from_sale_of_shares, loss_from_sale_mutual_fund_share_comp=loss_from_sale_mutual_fund_share_comp, loss_from_sale_mutual_fund_share_comp_combi_fund=loss_from_sale_mutual_fund_share_comp_combi_fund, loss_from_sale_mutual_fund_interest_comp=loss_from_sale_mutual_fund_interest_comp,
                           loss_from_sale_mutual_fund_interest_comp_combi_fund=loss_from_sale_mutual_fund_interest_comp_combi_fund, mutual_fund_wealth_share_comp=mutual_fund_wealth_share_comp, mutual_fund_wealth_interest_comp=mutual_fund_wealth_interest_comp, wealth_in_shares=wealth_in_shares, wealth_in_unlisted_shares=wealth_in_unlisted_shares, wealth_ask_cash=wealth_ask_cash, wealth_ask_shares=wealth_ask_shares, wealth_fondskonto_cash_interest=wealth_fondskonto_cash_interest,
                           wealth_fondskonto_shares=wealth_fondskonto_shares)

        data = json.dumps(payload_, cls=tut.NpEncoder)
        res = session.post(tax_url(tax_year), data=data, headers=headers())

    if res.status_code != 200:
        raise Exception('[%d] error: %s' % (res.status_code, res.reason))

    return res.json()


def tax_parameters(tax_year=None):
    """
    this reads in the parameters from the config and makes them easily usable from other functions
    """
    return tut.tax_parameters(jurisdiction='NO', tax_year=tax_year)


def produce_tax_results(salary=0, refresh=False, tax_year=None, birth_year=1978, gains_from_sale_fondskonto_share_comp=0, gains_from_sale_of_shares_ask=0, property_taxable_value=0, pension=0, pension_months=12, pension_percent=100, property_sale_proceeds=0, rental_income=0, property_sale_loss=0, bank_deposits=0,
                        bank_interest_income=0, interest_expenses=0, gains_from_sale_fondskonto_interest_comp=0, dividends=0, mutual_fund_dividends=0, gains_from_sale_of_shares=0, mutual_fund_interest_comp_profit=0, mutual_fund_interest_comp_profit_combi_fund=0, mutual_fund_share_comp_profit=0, mutual_fund_share_comp_profit_combi_fund=0, loss_fondskonto_shares=0, loss_fondskonto_interest=0, loss_ask_sale=0,
                        loss_from_sale_of_shares=0, loss_from_sale_mutual_fund_share_comp=0, loss_from_sale_mutual_fund_share_comp_combi_fund=0, loss_from_sale_mutual_fund_interest_comp=0, loss_from_sale_mutual_fund_interest_comp_combi_fund=0,
                        mutual_fund_wealth_share_comp=0, mutual_fund_wealth_interest_comp=0, wealth_in_shares=0, wealth_in_unlisted_shares=0, wealth_ask_cash=0, wealth_ask_shares=0, wealth_fondskonto_cash_interest=0, wealth_fondskonto_shares=0, session=None):
    """
    This gets the data from the official Norwegian tax server
    """
    raw = tax_query(salary=salary, birth_year=birth_year, refresh=refresh, tax_year=tax_year, gains_from_sale_fondskonto_share_comp=gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask=gains_from_sale_of_shares_ask, property_taxable_value=property_taxable_value, pension=pension, pension_months=pension_months, pension_percent=pension_percent, property_sale_proceeds=property_sale_proceeds, rental_income=rental_income, property_sale_loss=property_sale_loss, bank_deposits=bank_deposits,
                    bank_interest_income=bank_interest_income, interest_expenses=interest_expenses, gains_from_sale_fondskonto_interest_comp=gains_from_sale_fondskonto_interest_comp, dividends=dividends, mutual_fund_dividends=mutual_fund_dividends, gains_from_sale_of_shares=gains_from_sale_of_shares,
                    mutual_fund_interest_comp_profit=mutual_fund_interest_comp_profit, mutual_fund_interest_comp_profit_combi_fund=mutual_fund_interest_comp_profit_combi_fund, mutual_fund_share_comp_profit=mutual_fund_share_comp_profit, mutual_fund_share_comp_profit_combi_fund=mutual_fund_share_comp_profit_combi_fund, loss_fondskonto_shares=loss_fondskonto_shares, loss_fondskonto_interest=loss_fondskonto_interest, loss_ask_sale=loss_ask_sale, loss_from_sale_of_shares=loss_from_sale_of_shares,
                    loss_from_sale_mutual_fund_share_comp=loss_from_sale_mutual_fund_share_comp, loss_from_sale_mutual_fund_share_comp_combi_fund=loss_from_sale_mutual_fund_share_comp_combi_fund, loss_from_sale_mutual_fund_interest_comp=loss_from_sale_mutual_fund_interest_comp, loss_from_sale_mutual_fund_interest_comp_combi_fund=loss_from_sale_mutual_fund_interest_comp_combi_fund, mutual_fund_wealth_share_comp=mutual_fund_wealth_share_comp,
                    mutual_fund_wealth_interest_comp=mutual_fund_wealth_interest_comp, wealth_in_shares=wealth_in_shares, wealth_in_unlisted_shares=wealth_in_unlisted_shares, wealth_ask_cash=wealth_ask_cash, wealth_ask_shares=wealth_ask_shares, wealth_fondskonto_cash_interest=wealth_fondskonto_cash_interest, wealth_fondskonto_shares=wealth_fondskonto_shares, session=session)

    # pdb.set_trace()
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
    out = [['Salary', salary, 0], ['', 0, 0]]
    for item in items:
        try:
            out.append([item, data[item]['grunnlag'], data[item]['beloep']])
        except Exception:
            # print(err.msg)
            out.append([item, 0, 0])

    if deductions != 0:
        out.append(['Sum skattefradrag', 0, -deductions])

    frame = pd.DataFrame(out, columns=['tax_type', 'tax_basis', 'tax'])
    assert abs(frame.tax.sum() - correct_tax) < 1e-4, "Estimated tax differs from the true tax! (%s vs %s)" % (
        tut.big_fmt(frame.tax.sum()), tut.big_fmt(correct_tax))
    return frame


def explain_tax_item(item_no='3.1.8'):
    """
    just show the web-page for the item
    """

    text = item_no.replace('.', '/')
    url = "https://www.skatteetaten.no/person/skatt/skattemelding/finn-post/%s" % text
    return webbrowser.open(url)


def generate_test_cases(
        n_test_cases=20, test_payload_only=False, tax_year=None):
    """
    generate randomized test cases

    test_payload_only is for when we broke on writing numpy ints to json, no longer relevant
    """

    if tax_year is None:
        tax_year = pd.to_datetime('today').year
    incomes = range(0, 1000000, 1000)

    inc_random = np.random.choice(incomes, 2)

    gains_from_sale_fondskonto_share_comps = range(0, 1000000, 1000)
    gfsfsc = np.random.choice(gains_from_sale_fondskonto_share_comps, 2)
    net_gain_shares_sales = range(0, 1000000, 1000)
    ngss = np.random.choice(net_gain_shares_sales, 2)

    property_taxable_values = range(0, 1000000, 1000)
    ptv = np.random.choice(property_taxable_values, 2)
    pensions = range(0, 1000000, 1000)
    pension_random = np.random.choice(pensions, 2)

    pension_months = [12]
    pension_percents = [0, 50, 100]

    property_sale_proceeds = range(0, 1000000, 1000)
    rent_incomes = range(0, 1000000, 1000)
    property_sale_losses = range(0, 1000000, 1000)
    bank_deposits = range(0, 1000000, 1000)
    bank_interest_income = range(0, 1000000, 1000)
    interest_expenses = range(0, 1000000, 1000)
    # gains_from_sale_fondskonto_interest_comp = range(0, 1000000, 1000 )
    dividends = range(0, 1000000, 1000)
    gains_from_sale_of_shares = range(0, 1000000, 1000)
    # mutual_fund_interest_comp_profit = range(0, 1000000, 1000 )
    # mutual_fund_interest_comp_profit_combi_fund = range(0, 1000000, 1000 )
    # mutual_fund_share_comp_profit = range(0, 1000000, 1000 )
    # mutual_fund_share_comp_profit_combi_fund = range(0, 1000000, 1000 )
    loss_fondskonto_shares = range(0, 1000000, 1000)
    # loss_fondskonto_interest = range(0, 1000000, 1000 )
    loss_ask_sale = range(0, 1000000, 1000)

    loss_from_sale_mutual_fund_share_comp = range(0, 1000000, 1000)
    wealth_fondskonto_cash_interest = range(0, 1000000, 1000)
    loss_from_sale_of_shares = range(0, 1000000, 1000)
    # loss_from_sale_mutual_fund_share_comp_combi_fund = range(0, 1000000, 1000 )
    # loss_from_sale_mutual_fund_interest_comp = range(0, 1000000, 1000 )
    # loss_from_sale_mutual_fund_interest_comp_combi_fund = range(0, 1000000, 1000 )
    # mutual_fund_wealth_share_comp = range(0, 1000000, 1000 )
    # mutual_fund_wealth_interest_comp = range(0, 1000000, 1000 )
    wealth_in_shares = range(0, 1000000, 1000)
    # wealth_in_unlisted_shares = range(0, 1000000, 1000 )
    # wealth_ask_cash = range(0, 1000000, 1000 )
    wealth_ask_shares = range(0, 1000000, 1000)
    wealth_fondskonto_shares = range(0, 1000000, 1000)

    # pdb.set_trace()
    combos = itertools.product(inc_random, gfsfsc, ngss, ptv, pension_random, pension_months, pension_percents, np.random.choice(property_sale_proceeds, 2),
                               np.random.choice(
        rent_incomes, 2), np.random.choice(
        property_sale_losses, 2), np.random.choice(
            bank_deposits, 2),
        np.random.choice(
        bank_interest_income, 2), np.random.choice(
        interest_expenses, 2),
        np.random.choice(
        dividends, 2), np.random.choice(
        gains_from_sale_of_shares, 2),
        np.random.choice(
        loss_fondskonto_shares, 2), np.random.choice(
        loss_ask_sale, 2), np.random.choice(
            loss_from_sale_mutual_fund_share_comp, 2),
        np.random.choice(
        wealth_fondskonto_cash_interest, 2), np.random.choice(
        loss_from_sale_of_shares, 2),
        np.random.choice(
        wealth_in_shares, 2), np.random.choice(
        wealth_ask_shares, 2), np.random.choice(wealth_fondskonto_shares, 2)

    )
    arr = list(combos)
    # pdb.set_trace()
    sample_idx = np.random.choice(len(arr), n_test_cases)
    out = []
    # this converts the ints to np.int64 and therefore breaks the json
    # conversion...
    parameters = np.array(arr)[sample_idx]

    # pdb.set_trace()
    with requests.Session() as sesh:
        for (salary, gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask,
                property_taxable_value, pension, pension_months, pension_percent,
                property_sale_proceeds, rental_income, property_sale_loss, bank_deposit,
                bank_interest_income, interest_expenses, dividends, gains_from_sale_of_shares, loss_fondskonto_shares,
                loss_ask_sale, loss_from_sale_mutual_fund_share_comp, wealth_fondskonto_cash_interest, loss_from_sale_of_shares,
                wealth_in_shares, wealth_ask_shares, wealth_fondskonto_shares) in parameters:

            if test_payload_only:
                try:
                    pl_in = payload(tax_year=tax_year, salary=salary, gains_from_sale_fondskonto_share_comp=gains_from_sale_fondskonto_share_comp,
                                    gains_from_sale_of_shares_ask=gains_from_sale_of_shares_ask, property_taxable_value=property_taxable_value,
                                    pension=pension, pension_months=pension_months, pension_percent=pension_percent, property_sale_proceeds=property_sale_proceeds,
                                    rental_income=rental_income, property_sale_loss=property_sale_loss, bank_deposits=bank_deposit, bank_interest_income=bank_interest_income,
                                    interest_expenses=interest_expenses, dividends=dividends, gains_from_sale_of_shares=gains_from_sale_of_shares, loss_fondskonto_shares=loss_fondskonto_shares,
                                    loss_ask_sale=loss_ask_sale, loss_from_sale_mutual_fund_share_comp=loss_from_sale_mutual_fund_share_comp, wealth_fondskonto_cash_interest=wealth_fondskonto_cash_interest,
                                    loss_from_sale_of_shares=loss_from_sale_of_shares, wealth_in_shares=wealth_in_shares, wealth_ask_shares=wealth_ask_shares)
                    json.dumps(pl_in)
                except BaseException:
                    print("Failed to create payload")
                    pdb.set_trace()
            else:
                frame = produce_tax_results(salary=salary, gains_from_sale_fondskonto_share_comp=gains_from_sale_fondskonto_share_comp,
                                            gains_from_sale_of_shares_ask=gains_from_sale_of_shares_ask, property_taxable_value=property_taxable_value,
                                            pension=pension, pension_months=pension_months, pension_percent=pension_percent, property_sale_proceeds=property_sale_proceeds,
                                            rental_income=rental_income, property_sale_loss=property_sale_loss, bank_deposits=bank_deposit, bank_interest_income=bank_interest_income,
                                            interest_expenses=interest_expenses, dividends=dividends, gains_from_sale_of_shares=gains_from_sale_of_shares, loss_fondskonto_shares=loss_fondskonto_shares,
                                            loss_ask_sale=loss_ask_sale, loss_from_sale_mutual_fund_share_comp=loss_from_sale_mutual_fund_share_comp, wealth_fondskonto_cash_interest=wealth_fondskonto_cash_interest,
                                            loss_from_sale_of_shares=loss_from_sale_of_shares, wealth_in_shares=wealth_in_shares, wealth_ask_shares=wealth_ask_shares, session=sesh, tax_year=tax_year, wealth_fondskonto_shares=wealth_fondskonto_shares)
                # pdb.set_trace()
                out.append([salary, gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask,
                            property_taxable_value, pension, pension_months, pension_percent,
                            property_sale_proceeds, rental_income, property_sale_loss, bank_deposit,
                            bank_interest_income, interest_expenses, dividends, gains_from_sale_of_shares, loss_fondskonto_shares,
                            loss_ask_sale, loss_from_sale_mutual_fund_share_comp, wealth_fondskonto_cash_interest, loss_from_sale_of_shares,
                            wealth_in_shares, wealth_ask_shares, wealth_fondskonto_shares, frame.tax.sum()])

    if test_payload_only:
        return None
    return pd.DataFrame(out, columns=['salary', 'gains_from_sale_fondskonto_share_comp', 'gains_from_sale_of_shares_ask',
                                      'property_taxable_value', 'pension', 'pension_months', 'pension_percent',
                                      'property_sale_proceeds', 'rental_income', 'property_sale_loss', 'bank_deposits',
                                      'bank_interest_income', 'interest_expenses', 'dividends', 'gains_from_sale_of_shares', 'loss_fondskonto_shares',
                                      'loss_ask_sale', 'loss_from_sale_mutual_fund_share_comp', 'wealth_fondskonto_cash_interest', 'loss_from_sale_of_shares',
                                      'wealth_in_shares', 'wealth_ask_shares', 'wealth_fondskonto_shares', 'correct_tax'])


def print_test_cases(frame, start_case=9):
    """
    df is generated by generate_test_cases
    This is to make it easier to paste into the test file
    """

    # TODO: could be dispatched to utils module
    case = start_case
    for i in range(len(frame)):
        print('[%d]' % case)
        for k, value in frame.iloc[i].items():
            item = k
            if k == 'correct_tax':
                item = 'tax'

            print('%s=%d' % (item, value))
        case += 1


def add_test_cases(
        n_test_cases=15, file_name='no_test_cases.ini', test_df=None):
    """
    add random test cases
    set test_df if you've already generated test cases
    """

    # TODO: does it make sense to move to utils file?
    text = tut.read_file_as_string(file_name)
    # make sure we backup before overwriting
    i = 0
    name, ext = file_name.split('.')
    while os.path.exists('%s_bkup%s.%s' % (name, ('%d' % i).zfill(2), ext)):
        i += 1

    with open('%s_bkup%s.%s' % (name, ('%d' % i).zfill(2), ext), 'w') as file_ptr:
        file_ptr.write(text)
    cases = [m.group() for m in re.finditer(r'\[\d{2}\]', text)]
    if len(cases) == 0:
        cases = [m.group() for m in re.finditer(r'\[\d{1}\]', text)]
    last_case = int(cases[-1].replace('[', '').replace(']', ''))
    # append new cases ot the end
    if test_df is None:
        frame = generate_test_cases(n_test_cases=n_test_cases)
    else:
        frame = test_df.copy()
    case = last_case + 1
    text += '\n'
    for i in range(len(frame)):
        text += '[%d]\n' % case
        # print('[%d]'%case)
        for k, value in frame.iloc[i].items():
            item = k
            if k == 'correct_tax':
                item = 'tax'

            text += '%s=%d\n' % (item, value)
        case += 1

    with open(file_name, 'w') as file_ptr:
        file_ptr.write(text)


def add_birth_year_test_cases(file_name='no_test_cases.ini', birth_year=1950):
    """
    take the existing tests and add birth_year=1950 to them (that's one of the cutoff ages)

    this is a one-off.
    """
    text = tut.read_file_as_string(file_name)
    # make sure we backup before overwriting
    i = 0
    name, ext = file_name.split('.')
    while os.path.exists('%s_bkup%s.%s' % (name, ('%d' % i).zfill(2), ext)):
        i += 1

    with open('%s_bkup%s.%s' % (name, ('%d' % i).zfill(2), ext), 'w') as file_ptr:
        file_ptr.write(text)
    cases = [m.group() for m in re.finditer(r'\[\d{2}\]', text)]
    case_idxs = [m.start() for m in re.finditer(r'\[\d{2}\]', text)]

    if len(cases) == 0:
        cases = [m.group() for m in re.finditer(r'\[\d{1}\]', text)]
        case_idxs = [m.start() for m in re.finditer(r'\[\d{1}\]', text)]
    else:
        # add in the single_digit ones:
        last_case = int(cases[-1].replace('[', '').replace(']', ''))
        cases += [m.group() for m in re.finditer(r'\[\d{1}\]', text)]
        case_idxs += [m.start() for m in re.finditer(r'\[\d{1}\]', text)]
    case_idxs, cases = tut.syncsort(case_idxs, cases)

    # append new cases ot the end

    case = last_case + 1
    text += '\n'
    # new_text = text[0:case_idxs[0]]
    new_text = ''
    for i in range(len(case_idxs)):
        try:
            rel = text[case_idxs[i]:case_idxs[i + 1]]
        except BaseException:
            rel = text[case_idxs[i]:]

        if rel.find('birth_year') == -1:
            # pdb.set_trace()
            rel += 'birth_year=%d\n' % birth_year
            # rel
            new_text += rel.replace(cases[i], '[%d]' % (case))
            case += 1

    with open(file_name, 'w') as file_ptr:
        file_ptr.write(text + new_text)


def dump_test_cases_to_excel():
    """
    help speed up excel-translation
    """
    fields = ['birth_year', 'salary', 'pension', 'pension_months', 'pension_percent', 'rental_income', 'property_sale_proceeds', 'property_sale_loss', 'gains_from_sale_fondskonto_share_comp',
              'dividends', 'mutual_fund_dividends', 'gains_from_sale_of_shares', 'gains_from_sale_of_shares_ask', 'mutual_fund_share_comp_profit_combi_fund', 'mutual_fund_share_comp_profit', 'loss_from_sale_mutual_fund_share_comp_combi_fund', 'loss_fondskonto_shares', 'loss_ask_sale',
              'loss_from_sale_of_shares', 'loss_from_sale_mutual_fund_share_comp', 'gains_from_sale_fondskonto_interest_comp', 'mutual_fund_interest_comp_profit', 'mutual_fund_interest_comp_profit_combi_fund', 'loss_fondskonto_interest', 'loss_from_sale_mutual_fund_interest_comp', 'loss_from_sale_mutual_fund_interest_comp_combi_fund', 'mutual_fund_wealth_share_comp',
              'interest_expenses', 'wealth_in_shares', 'wealth_ask_shares', 'wealth_in_unlisted_shares', 'wealth_fondskonto_shares', 'mutual_fund_wealth_interest_comp', 'wealth_ask_cash',
              'wealth_fondskonto_cash_interest', 'bank_deposits', 'property_taxable_value', 'bank_interest_income']

    # params = tax_parameters(tax_year=tax_year)
    cases = configparser.ConfigParser()
    cases.read('no_test_cases.ini')
    case_numbers = sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))
    out = []
    for case_idx in case_numbers:
        input_struct = {}
        for k, value in cases['%d' % case_idx].items():
            if k != 'tax':
                input_struct[k] = value

            # try:
        for k, value in input_struct.items():
            if value.isdigit():
                input_struct[k] = float(value)
            elif value.replace('.', '').isdigit():
                input_struct[k] = float(value)
            elif value.replace('e', '').isdigit():
                input_struct[k] = eval(value)
            # except:
            #   pdb.set_trace()

        row = [case_idx]
        for field in fields:
            if field in ['birth_year']:
                val = input_struct.get(field, 1978)
            elif field in ['pension_percent']:
                val = input_struct.get(field, 100)
            elif field in ['pension_months']:
                val = input_struct.get(field, 12)
            else:
                val = input_struct.get(field, 0)
            row.append(val)
        out.append(row)

    return pd.DataFrame(out, columns=['case_idx'] + fields)


def dump_config_answers_to_excel():
    """
    for excel file
    """
    cases = configparser.ConfigParser()
    cases.read('no_test_cases.ini')
    case_numbers = sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))
    out = []
    for case_idx in case_numbers:
        # input_struct = {}
        for k, value in cases['%d' % case_idx].items():
            if k == 'tax':
                out.append([case_idx, value])

    return pd.DataFrame(out, columns=['Case', 'Skatt'])


def generate_test_cases_using_all_parameters(
        n_test_cases=20, add_tax_values=False):
    """
    add_tax_values means we hit the server
    """

    fields = ['birth_year', 'salary', 'pension', 'pension_months', 'pension_percent', 'rental_income', 'property_sale_proceeds', 'property_sale_loss', 'gains_from_sale_fondskonto_share_comp',
              'dividends', 'mutual_fund_dividends', 'gains_from_sale_of_shares', 'gains_from_sale_of_shares_ask', 'mutual_fund_share_comp_profit_combi_fund', 'mutual_fund_share_comp_profit', 'loss_from_sale_mutual_fund_share_comp_combi_fund', 'loss_fondskonto_shares', 'loss_ask_sale',
              'loss_from_sale_of_shares', 'loss_from_sale_mutual_fund_share_comp', 'gains_from_sale_fondskonto_interest_comp', 'mutual_fund_interest_comp_profit', 'mutual_fund_interest_comp_profit_combi_fund', 'loss_fondskonto_interest', 'loss_from_sale_mutual_fund_interest_comp', 'loss_from_sale_mutual_fund_interest_comp_combi_fund', 'mutual_fund_wealth_share_comp',
              'interest_expenses', 'wealth_in_shares', 'wealth_ask_shares', 'wealth_in_unlisted_shares', 'wealth_fondskonto_shares', 'mutual_fund_wealth_interest_comp', 'wealth_ask_cash',
              'wealth_fondskonto_cash_interest', 'bank_deposits', 'property_taxable_value', 'bank_interest_income']

    # params = tax_parameters(tax_year=tax_year)
    # cases = configparser.ConfigParser()
    # cases.read('no_test_cases.ini')
    # case_numbers = sorted(map(int, list(set(cases.keys()) - set(['DEFAULT']))))
    out = []
    # big_rng =
    for i in range(n_test_cases):
        input_struct = {}

        for field in fields:
            if field in ['birth_year']:
                # val = input_struct.get(field, 1978)
                val = np.random.choice(range(1913, 1990), 1).item()
            elif field in ['pension_percent']:
                val = np.random.choice(range(1, 101), 1).item()
            elif field in ['pension_months']:
                val = np.random.choice(range(1, 13), 1).item()
            elif field in ['salary', 'pension']:
                val = np.random.randint(0, 100000)
            else:
                val = np.random.randint(0, 5000000)
            input_struct[field] = val

        if add_tax_values:
            tmp_df = produce_tax_results(**input_struct)
            input_struct['correct_tax'] = tmp_df.tax.sum()
        out.append(input_struct)

    return pd.DataFrame(out)


def compare_calculated_tax_vs_correct_tax(
        case_idx=0, atol=1e-8, rtol=1e-6, check_basis=False):
    """
    compares the config vs our calculations
    It gives a more detailed breakdown so you can compare the components such as different basis etc.
    """

    tmp = NorwegianTax(case_idx=case_idx)
    df_calc = tmp.tax_breakdown()

    df_true = tmp.true_tax_data_frame()

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
    total_calculated_tax = df_calc.query("Skatt == 'Din Skatt'").Beloep.item()
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


class NorwegianTax:
    """
    to facilitate easy input
    """

    def __init__(self, salary=0, birth_year=1978, tax_year=None, gains_from_sale_fondskonto_share_comp=0, gains_from_sale_fondskonto_interest_comp=0, gains_from_sale_of_shares_ask=0, property_taxable_value=0, pension=0, pension_months=12, pension_percent=100, property_sale_proceeds=0, rental_income=0, property_sale_loss=0, bank_deposits=0,
                 bank_interest_income=0, interest_expenses=0, dividends=0, mutual_fund_dividends=0, gains_from_sale_of_shares=0, mutual_fund_interest_comp_profit=0, mutual_fund_interest_comp_profit_combi_fund=0, mutual_fund_share_comp_profit=0, mutual_fund_share_comp_profit_combi_fund=0, loss_fondskonto_shares=0, loss_fondskonto_interest=0, loss_ask_sale=0,
                 loss_from_sale_of_shares=0, loss_from_sale_mutual_fund_share_comp=0, loss_from_sale_mutual_fund_share_comp_combi_fund=0, loss_from_sale_mutual_fund_interest_comp=0,
                 loss_from_sale_mutual_fund_interest_comp_combi_fund=0, mutual_fund_wealth_share_comp=0, mutual_fund_wealth_interest_comp=0, wealth_in_shares=0, wealth_in_unlisted_shares=0, wealth_ask_cash=0, wealth_ask_shares=0, wealth_fondskonto_cash_interest=0, wealth_fondskonto_shares=0, case_idx=None):

        self._salary = salary
        self._birth_year = birth_year
        self._tax_year = tax_year
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
        self._case_file = 'no_test_cases.ini'
        self._session = requests.Session()

        if case_idx is not None:
            self._case_idx = case_idx
            inputs = tut.inputs_for_case_number(
                case_idx, case_file='no_test_cases.ini', include_correct_tax=False)

            for field, val in inputs.items():
                if hasattr(self, field):
                    # print('%s: %s'%(field, str(val)))
                    setattr(self, field, val)

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
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        self._birth_year = value

    @property
    def session(self):
        return self._session

    @property
    def tax_year(self):
        if self._tax_year is None:
            return pd.to_datetime('today').year
        return self._tax_year

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
    def case_file(self):
        return self._case_file

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
    def case_idx(self):
        return self._case_idx

    @case_idx.setter
    def case_idx(self, value):
        print("Trying to set case_idx to %s" % value)
        if value is not None:
            self._case_idx = value
            self.__init__()
            inputs = tut.inputs_for_case_number(
                value, case_file=self.case_file, include_correct_tax=False)

            for field, val in inputs.items():
                if hasattr(self, field):
                    # print('%s: %s'%(field, str(val)))
                    setattr(self, field, val)
        # self._case_idx = value

    @property
    def tax_parameters(self):
        return tut.tax_parameters(jurisdiction='NO', tax_year=self.tax_year)

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
    def pension_and_income_minimum_deduction(self):
        """
        does what it says
        """

        if (abs(self.pension) < 1e-4) or (abs(self.salary) < 1e-4):
            return 0

        income_deduction = max(
            min(
                self.salary *
                self.parameter('deduction_multiplier'),
                self.parameter('max_deduction_limit')),
            self.parameter('min_deduction_limit'))
        # you can't deduct more than what you earn:
        income_deduction = min(income_deduction, self.salary)
        pension_deduction = max(min(self.pension * self.parameter('pension_deduction_multiplier'),
                                    self.parameter('max_pension_deduction')), self.parameter('min_pension_deduction'))
        combo_deduction = pension_deduction + \
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
        return int(
            np.round(min(max(min(self.parameter('deduction_multiplier') * self.salary, self.parameter('max_deduction_limit')), self.parameter('min_deduction_limit')), self.salary)))

    @property
    def pension_only_minimum_deduction(self):
        """
        does what it says
        """
        return min(max(min(self.parameter('pension_deduction_multiplier') * self.pension,
                           self.parameter('max_pension_deduction')), self.parameter('min_pension_deduction')), self.pension)

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

    def parameter(self, pname=''):
        return self.tax_parameters.getfloat(pname)

    def state_wealth_tax(self):
        return self.tax_payable(basis=self.state_wealth_tax_basis, rate=self.parameter(
            'state_wealth_tax_rate'), limit=self.parameter('wealth_tax_lower_limit'))

    def municipal_wealth_tax(self):
        return self.tax_payable(basis=self.state_wealth_tax_basis, rate=self.parameter(
            'municipal_wealth_tax_rate'), limit=self.parameter('wealth_tax_lower_limit'))

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

    def true_tax_data_frame(self, refresh=False, session=None):
        frame = produce_tax_results(salary=self.salary, birth_year=self.birth_year, refresh=refresh, tax_year=self.tax_year, gains_from_sale_fondskonto_share_comp=self.gains_from_sale_fondskonto_share_comp, gains_from_sale_of_shares_ask=self.gains_from_sale_of_shares_ask, property_taxable_value=self.property_taxable_value, pension=self.pension, pension_months=self.pension_months, pension_percent=self.pension_percent, property_sale_proceeds=self.property_sale_proceeds, rental_income=self.rental_income, property_sale_loss=self.property_sale_loss,
                                    bank_deposits=self.bank_deposits, bank_interest_income=self.bank_interest_income, interest_expenses=self.interest_expenses, gains_from_sale_fondskonto_interest_comp=self.gains_from_sale_fondskonto_interest_comp, dividends=self.dividends, gains_from_sale_of_shares=self.gains_from_sale_of_shares, mutual_fund_interest_comp_profit=self.mutual_fund_interest_comp_profit,
                                    mutual_fund_interest_comp_profit_combi_fund=self.mutual_fund_interest_comp_profit_combi_fund, mutual_fund_share_comp_profit=self.mutual_fund_share_comp_profit, mutual_fund_share_comp_profit_combi_fund=self.mutual_fund_share_comp_profit_combi_fund, loss_fondskonto_shares=self.loss_fondskonto_shares, loss_fondskonto_interest=self.loss_fondskonto_interest, loss_ask_sale=self.loss_ask_sale,
                                    loss_from_sale_mutual_fund_share_comp=self.loss_from_sale_mutual_fund_share_comp, wealth_fondskonto_cash_interest=self.wealth_fondskonto_cash_interest,
                                    loss_from_sale_of_shares=self.loss_from_sale_of_shares, loss_from_sale_mutual_fund_share_comp_combi_fund=self.loss_from_sale_mutual_fund_share_comp_combi_fund, loss_from_sale_mutual_fund_interest_comp=self.loss_from_sale_mutual_fund_interest_comp, loss_from_sale_mutual_fund_interest_comp_combi_fund=self.loss_from_sale_mutual_fund_interest_comp_combi_fund,
                                    mutual_fund_wealth_share_comp=self.mutual_fund_wealth_share_comp, mutual_fund_wealth_interest_comp=self.mutual_fund_wealth_interest_comp, wealth_in_shares=self.wealth_in_shares, wealth_in_unlisted_shares=self.wealth_in_unlisted_shares, wealth_ask_cash=self.wealth_ask_cash, wealth_ask_shares=self.wealth_ask_shares, wealth_fondskonto_shares=self.wealth_fondskonto_shares, mutual_fund_dividends=self.mutual_fund_dividends, session=session)
        frame = frame.append({'tax_type': 'total',
                              'tax_basis': 0,
                              'tax': frame.tax.sum()},
                             ignore_index=True)

        return frame

    def display_online_breakdown(self, refresh=False, session=None):
        """
        this is the online ('true') figures
        """
        frame = self.true_tax_data_frame(refresh=refresh, session=session)

        orig_df = frame.copy()
        frame.tax = frame.tax.map(tut.big_fmt)
        frame.tax_basis = frame.tax_basis.map(tut.big_fmt)

        for col in ['tax_basis', 'tax']:
            frame.loc[1, col] = ''

        tut.display_df(frame)
        return orig_df

    def tax_ties_with_config(self, do_all=False, atol=1e-8, rtol=1e-5):
        if not do_all:
            return np.allclose(tut.config_tax(
                self.case_idx, case_file=self.case_file), self.tax())

        case_numbers = tut.all_case_numbers(case_file=self.case_file)
        observed = []
        expected = []
        for case_idx in tqdm(case_numbers):
            print("working on case number %d" % case_idx)
            setattr(self, 'case_idx', case_idx)
            # self.case_idx =
            # pdb.set_trace()
            observed.append(self.tax())
            expected.append(
                tut.config_tax(
                    self.case_idx,
                    case_file=self.case_file))

        if not np.allclose(observed, expected, atol=atol, rtol=rtol):
            exp = np.array(expected)
            obs = np.array(observed)

            good_idx = np.abs(exp - obs) <= (atol + rtol * np.abs(obs))
            bad_idx = np.where(~good_idx)[0]

            print("Some checks failed!")
            return bad_idx
        print("All tests passed!")
        return True

    def tax_ties_with_web(self, do_all=False, atol=1e-8,
                          rtol=1e-5, refresh=False):
        """
        this will (obviously hit the tax authority web server)
        """
        if not do_all:
            return np.allclose(self.true_tax_data_frame().query(
                "tax_type == 'total'").tax.sum(), self.tax())

        case_numbers = tut.all_case_numbers(case_file=self.case_file)
        observed = []
        expected = []
        with requests.Session() as sesh:
            for case_idx in tqdm(case_numbers):
                setattr(self, 'case_idx', case_idx)
                observed.append(self.tax())
                expected.append(
                    self.true_tax_data_frame(
                        refresh=refresh,
                        session=sesh).query("tax_type == 'total'").tax.sum())

        if not np.allclose(observed, expected, atol=atol, rtol=rtol):
            exp = np.array(expected)
            obs = np.array(observed)

            good_idx = np.abs(exp - obs) <= (atol + rtol * np.abs(obs))
            bad_idx = np.where(~good_idx)[0]

            print("Some checks failed!")
            return bad_idx
        print("All tests passed!")
        return True
