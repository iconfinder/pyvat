import datetime
import pycountry
from decimal import Decimal
from pyvat import (
    get_sale_vat_charge,
    ItemType,
    Party,
    VatChargeAction,
)
from pyvat.countries import EU_COUNTRY_CODES
from unittest2 import TestCase


EXPECTED_VAT_RATES = {
    'AT': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(10),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(20),
    },
    'BE': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(21),
    },
    'BG': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
    'CY': {
        ItemType.generic_physical_good: Decimal(19),
        ItemType.generic_electronic_service: Decimal(19),
        ItemType.generic_telecommunications_service: Decimal(19),
        ItemType.generic_broadcasting_service: Decimal(19),
        ItemType.prepaid_broadcasting_service: Decimal(19),
        ItemType.ebook: Decimal(19),
        ItemType.enewspaper: Decimal(19),
    },
    'CZ': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(21),
    },
    'DE': {
        ItemType.generic_physical_good: Decimal(19),
        ItemType.generic_electronic_service: Decimal(19),
        ItemType.generic_telecommunications_service: Decimal(19),
        ItemType.generic_broadcasting_service: Decimal(19),
        ItemType.prepaid_broadcasting_service: Decimal(19),
        ItemType.ebook: Decimal(7),
        ItemType.enewspaper: Decimal(19),
    },
    'DK': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(25),
        ItemType.enewspaper: Decimal(25),
    },
    'EE': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
    'ES': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(4),
        ItemType.enewspaper: Decimal(21),
    },
    'FI': {
        ItemType.generic_physical_good: Decimal(24),
        ItemType.generic_electronic_service: Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service: Decimal(24),
        ItemType.prepaid_broadcasting_service: Decimal(24),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(24),
    },
    'FR': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(10),
        ItemType.prepaid_broadcasting_service: Decimal(10),
        ItemType.ebook: Decimal('5.5'),
        ItemType.enewspaper: Decimal('2.1'),
    },
    'EL': {
        ItemType.generic_physical_good: Decimal(24),
        ItemType.generic_electronic_service: Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service: Decimal(24),
        ItemType.prepaid_broadcasting_service: Decimal(24),
        ItemType.ebook: Decimal(24),
        ItemType.enewspaper: Decimal(24),
    },
    'GR': {  # Synonymous for "EL" -- Greece
        ItemType.generic_physical_good:              Decimal(24),
        ItemType.generic_electronic_service:         Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service:       Decimal(24),
        ItemType.prepaid_broadcasting_service:       Decimal(24),
        ItemType.ebook:                              Decimal(24),
        ItemType.enewspaper:                         Decimal(24),
    },
    'HR': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(25),
    },
    'HU': {
        ItemType.generic_physical_good: Decimal(27),
        ItemType.generic_electronic_service: Decimal(27),
        ItemType.generic_telecommunications_service: Decimal(27),
        ItemType.generic_broadcasting_service: Decimal(27),
        ItemType.prepaid_broadcasting_service: Decimal(27),
        ItemType.ebook: Decimal(27),
        ItemType.enewspaper: Decimal(27),
    },
    'IE': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(9),
        ItemType.enewspaper: Decimal(21),
    },
    'IT': {
        ItemType.generic_physical_good: Decimal(22),
        ItemType.generic_electronic_service: Decimal(22),
        ItemType.generic_telecommunications_service: Decimal(22),
        ItemType.generic_broadcasting_service: Decimal(22),
        ItemType.prepaid_broadcasting_service: Decimal(22),
        ItemType.ebook: Decimal(22),
        ItemType.enewspaper: Decimal(22),
    },
    'LT': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(21),
        ItemType.enewspaper: Decimal(21),
    },
    'LU': {
        ItemType.generic_physical_good: Decimal(17),
        ItemType.generic_electronic_service: Decimal(17),
        ItemType.generic_telecommunications_service: Decimal(17),
        ItemType.generic_broadcasting_service: Decimal(3),
        ItemType.prepaid_broadcasting_service: Decimal(3),
        ItemType.ebook: Decimal(3),
        ItemType.enewspaper: Decimal(17),
    },
    'LV': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(21),
        ItemType.enewspaper: Decimal(21),
    },
    'MT': {
        ItemType.generic_physical_good: Decimal(18),
        ItemType.generic_electronic_service: Decimal(18),
        ItemType.generic_telecommunications_service: Decimal(18),
        ItemType.generic_broadcasting_service: Decimal(18),
        ItemType.prepaid_broadcasting_service: Decimal(18),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(18),
    },
    'NL': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(9),
        ItemType.enewspaper: Decimal(21),
    },
    'PL': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(8),
        ItemType.prepaid_broadcasting_service: Decimal(8),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(23),
    },
    'PT': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(23),
        ItemType.prepaid_broadcasting_service: Decimal(23),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(23),
    },
    'RO': {
        ItemType.generic_physical_good: Decimal(19),
        ItemType.generic_electronic_service: Decimal(19),
        ItemType.generic_telecommunications_service: Decimal(19),
        ItemType.generic_broadcasting_service: Decimal(19),
        ItemType.prepaid_broadcasting_service: Decimal(19),
        ItemType.ebook: Decimal(19),
        ItemType.enewspaper: Decimal(19),
    },
    'SE': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(25),
    },
    'SI': {
        ItemType.generic_physical_good: Decimal(22),
        ItemType.generic_electronic_service: Decimal(22),
        ItemType.generic_telecommunications_service: Decimal(22),
        ItemType.generic_broadcasting_service: Decimal(22),
        ItemType.prepaid_broadcasting_service: Decimal(22),
        ItemType.ebook: Decimal(22),
        ItemType.enewspaper: Decimal(22),
    },
    'SK': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
}
SUPPORTED_ITEM_TYPES = [
    ItemType.generic_electronic_service,
    ItemType.generic_telecommunications_service,
    ItemType.generic_broadcasting_service,
    ItemType.prepaid_broadcasting_service,
    ItemType.ebook,
    ItemType.enewspaper,
]


class GetSaleVatChargeTestCase(TestCase):
    """Test case for :func:`get_sale_vat_charge`.
    """

    def test_get_sale_vat_charge(self):
        """get_sale_vat_charge(..)
        """

        # EU businesses selling to any type of customer in their own country
        # charge VAT.
        for seller_cc in EU_COUNTRY_CODES:
            for it in SUPPORTED_ITEM_TYPES:
                for d in [datetime.date(2014, 12, 15),
                          datetime.date(2015, 1, 1)]:
                    for buyer_is_business in [True, False]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=seller_cc,
                                  is_business=buyer_is_business),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.charge)

                        self.assertEqual(vat_charge.rate,
                                         EXPECTED_VAT_RATES[seller_cc][it])
                        self.assertEqual(vat_charge.country_code,
                                         seller_cc)

        # EU businesses selling to businesses in other EU countries apply the
        # reverse-charge mechanism.
        for seller_cc in EU_COUNTRY_CODES:
            for buyer_cc in EU_COUNTRY_CODES:
                if seller_cc == buyer_cc:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=buyer_cc, is_business=True),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.reverse_charge)
                        self.assertEqual(vat_charge.rate,
                                         Decimal(0))
                        self.assertEqual(vat_charge.country_code,
                                         buyer_cc)

        # EU businesses selling to consumers in other EU countries charge VAT
        # in the country in which the consumer resides after January 1st, 2015.
        for seller_cc in EU_COUNTRY_CODES:
            for buyer_cc in EU_COUNTRY_CODES:
                if seller_cc == buyer_cc:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=buyer_cc, is_business=False),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.charge)
                        self.assertEqual(
                            vat_charge.rate,
                            EXPECTED_VAT_RATES[buyer_cc][it]
                            if d >= datetime.date(2015, 1, 1) else
                            EXPECTED_VAT_RATES[seller_cc][it]
                        )
                        self.assertEqual(
                            vat_charge.country_code,
                            buyer_cc
                            if d >= datetime.date(2015, 1, 1) else
                            seller_cc
                        )

        # EU businesses selling to customers outside the EU do not charge VAT.
        for seller_cc in EU_COUNTRY_CODES:
            for buyer_country in pycountry.countries:
                buyer_cc = buyer_country.alpha_2
                if buyer_cc in EU_COUNTRY_CODES:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        for buyer_is_business in [True, False]:
                            vat_charge = get_sale_vat_charge(
                                d,
                                it,
                                Party(country_code=buyer_cc,
                                      is_business=buyer_is_business),
                                Party(country_code=seller_cc, is_business=True)
                            )
                            self.assertEqual(vat_charge.action,
                                             VatChargeAction.no_charge)
                            self.assertEqual(vat_charge.rate, Decimal(0))
