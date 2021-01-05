from pyvat import (
    check_vat_number,
    is_vat_number_format_valid,
    VatNumberCheckResult,
)
from unittest2 import TestCase


VAT_NUMBER_FORMAT_CASES = {
    '': [
        ('123456', False),
    ],
    'AT': [
        ('U68103312', True),
        ('U12345678', True),
    ],
    'BE': [
        ('123456789', True),
    ],
    'CY': [
        ('12345678X', True),
    ],
    'CZ': [
        ('12345678', True),
        ('123456789', True),
        ('1234567890', True),
    ],
    'DE': [
        ('123456789', True),
    ],
    'DK': [
        (' 12 34 56 78', True),
        ('12345678', True),
        ('00000000', True),
        ('99999999', True),
        ('99999O99', False),
        ('9999999', False),
        ('999999900', False),
    ],
    'EE': [
        ('123456789', True),
    ],
    'ES': [
        ('X12345678', True),
        ('12345678X', True),
        ('X1234567X', True),
    ],
    'FI': [
        ('12345678', True),
    ],
    'FR': [
        ('12345678901', True),
        ('X2345678901', True),
        ('1X345678901', True),
        ('XX345678901', True),
        ('O2345678901', False),
        ('1O345678901', False),
        ('OO345678901', False),
        ('I2345678901', False),
        ('1I345678901', False),
        ('II345678901', False),
    ],
    'GR': [
        ('012345678', True),
    ],
    'HR': [
        ('12345678901', True),
        ('1234567890', False),
        ('123456789012', False),
        ('1234567890A', False),
    ],
    'HU': [
        ('12345678', True),
    ],
    'IE': [
        ('1114174HH', True),
        ('1X34567X', True),
        ('1234567X', True),
    ],
    'IT': [
        ('12345678901', True),
    ],
    'LV': [
        ('12345678901', True),
    ],
    'LT': [
        ('123456789', True),
        ('123456789012', True),
    ],
    'LU': [
        ('12345678', True),
    ],
    'MT': [
        ('12345678', True),
    ],
    'NL': [
        ('043133502B02', True),
    ],
    'PL': [
        ('1234567890', True),
    ],
    'PT': [
        ('123456789', True),
    ],
    'SE': [
        ('123456789001', True),
    ],
    'SK': [
        ('1234567890', True),
    ],
    'SI': [
        ('12345678', True),
    ],
}
"""Cases for testing VAT number format validation.

Mapping of VAT number prefix to a list of tuples of:

::

   (<non-prefixed VAT number>, <valid>)
"""

VAT_NUMBER_CHECK_CASES = {
    '': [
        ('123456', VatNumberCheckResult(False)),
    ],
    'BE': [
        ('0438390312',
         VatNumberCheckResult(
             True,
             business_name=u'NV UNILEVER BELGIUM - UNILEVER BELGIQUE - '
             u'UNILEVER BELGIE',
             business_address=u'Industrielaan 9\n1070 Anderlecht'
         )),
    ],
    'DK': [
        ('54562519', VatNumberCheckResult(
            True,
            business_name=u'Lego A/S',
            business_address='Åstvej 1\n7190 Billund'
        )),
        ('99999O99', VatNumberCheckResult(False)),
        ('9999999', VatNumberCheckResult(False)),
        ('999999900', VatNumberCheckResult(False)),
    ],
    'IE': [
        ('1114174HH',
         VatNumberCheckResult(
             True,
             business_name=u'SPLAY CONSULTING LIMITED',
             business_address=u'22 ADMIRAL PARK, BALDOYLE, DUBLIN 13'
         )),
    ],
    'NL': [
        ('043133502B02', VatNumberCheckResult(False)),
    ],
}
"""Cases for fully testing VAT validity.

Mapping of VAT number prefix to a list of tuples of:

::

   (<non-prefixed VAT number>, <expected result>)
"""


class IsVatNumberFormatValidTestCase(TestCase):
    """Test case for :func:`is_vat_number_format_valid`.
    """

    def test_no_country_code(self):
        """is_vat_number_format_valid('..', country_code=None)
        """

        for country_code, cases in VAT_NUMBER_FORMAT_CASES.items():
            for vat_number, expected_result in cases:
                verbal_expected_result = \
                    'valid' if expected_result else 'invalid'

                self.assertEqual(
                    is_vat_number_format_valid('%s%s' % (country_code,
                                                         vat_number)),
                    expected_result,
                    'expected prefixed VAT number %s%s to be %s' %
                    (country_code,
                     vat_number,
                     verbal_expected_result)
                )

    def test_country_code(self):
        """is_vat_number_format_valid('..', country_code='..')
        """

        for country_code, cases in VAT_NUMBER_FORMAT_CASES.items():
            for vat_number, expected_result in cases:
                verbal_expected_result = \
                    'valid' if expected_result else 'invalid'

                self.assertEqual(is_vat_number_format_valid(vat_number,
                                                            country_code),
                                 expected_result,
                                 'expected non-prefixed VAT number %s (%s) '
                                 'to be %s' % (vat_number,
                                               country_code,
                                               verbal_expected_result))
                self.assertEqual(
                    is_vat_number_format_valid(
                        '%s%s' % (country_code, vat_number),
                        country_code
                    ),
                    expected_result,
                    'expected prefixed VAT number %s%s (%s) to be %s' %
                    (country_code,
                     vat_number,
                     country_code,
                     verbal_expected_result)
                )


class CheckVatNumberTestCase(TestCase):
    """Test case for :func:`check_vat_number`.
    """

    def assert_result_equals(self, expected, actual):
        self.assertIsInstance(actual, VatNumberCheckResult)
        self.assertEqual(expected.is_valid, actual.is_valid)
        self.assertEqual(expected.business_name, actual.business_name)
        expected_address = expected.business_address
        if expected_address:
            expected_address = expected_address.lower()
        actual_address = actual.business_address
        if actual_address:
            actual_address = actual_address.lower()
        self.assertEqual(expected_address, actual_address)

    def test_no_country_code(self):
        """check_vat_number('..', country_code=None)
        """

        for country_code, cases in VAT_NUMBER_CHECK_CASES.items():
            for vat_number, expected in cases:
                self.assert_result_equals(
                    expected,
                    check_vat_number('%s%s' % (country_code, vat_number))
                )

    def test_dk__country_code(self):
        """check_vat_number('..', country_code='..')
        """

        for country_code, cases in VAT_NUMBER_CHECK_CASES.items():
            for vat_number, expected in cases:
                self.assert_result_equals(
                    expected,
                    check_vat_number(vat_number, country_code)
                )
                self.assert_result_equals(
                    expected,
                    check_vat_number('%s%s' % (country_code, vat_number),
                                     country_code)
                )


__all__ = ('IsVatNumberFormatValidTestCase', 'CheckVatNumberTestCase', )
