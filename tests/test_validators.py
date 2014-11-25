from pyvat import (
    check_vat_number,
    is_vat_number_format_valid,
    VatNumberCheckResult,
)
from unittest2 import TestCase


VAT_NUMBER_CASES = {
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
    'EL': [
        ('012345678', True),
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
    'GB': [
        ('123456789', True),
        ('123456789001', True),
        ('999999999999999999999999999999999999', False),
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


class IsVatNumberFormatValidTestCase(TestCase):
    """Test case for :func:`is_vat_number_format_valid`.
    """

    def test_no_country_code(self):
        """is_vat_number_format_valid('..', country_code=None)
        """

        for country_code, cases in VAT_NUMBER_CASES.items():
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

        for country_code, cases in VAT_NUMBER_CASES.items():
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
        self.assertEqual(expected.business_address,
                         actual.business_address)

    def test_arbitrary__no_country_code(self):
        """check_vat_number(<arbitary>, country_code=None)
        """

        for vat_number, expected in [
            ('IE1114174HH',
             VatNumberCheckResult(
                 True,
                 business_name=u'SPLAY CONSULTING LIMITED',
                 business_address=u'22 ADMIRAL PARK ,BALDOYLE ,DUBLIN 13'
             )),
            ('123457', VatNumberCheckResult(False)),
            ('NL043133502B02', VatNumberCheckResult(False)),
            ('BE0438390312',
             VatNumberCheckResult(
                 True,
                 business_name=u'NV UNILEVER BELGIUM - UNILEVER BELGIQUE - '
                 u'UNILEVER BELGIE',
                 business_address=u'HUMANITEITSLAAN 292\n1190  VORST'
             )),
        ]:
            self.assert_result_equals(expected, check_vat_number(vat_number))

    def test_dk__no_country_code(self):
        """check_vat_number(<DK>, country_code=None)
        """

        for vat_number, expected in [
            ('DK33779437', VatNumberCheckResult(
                True,
                business_name=u'ICONFINDER ApS',
                business_address=u'Pilestr\xe6de 43 2\n1112 K\xf8benhavn K'
            )),
            ('DK99999O99', VatNumberCheckResult(False)),
            ('DK9999999', VatNumberCheckResult(False)),
            ('DK999999900', VatNumberCheckResult(False)),
        ]:
            self.assert_result_equals(expected, check_vat_number(vat_number))

    def test_dk__country_code(self):
        """check_vat_number(<DK>, country_code='DK')
        """

        for vat_number, expected in [
            ('33779437', VatNumberCheckResult(
                True,
                business_name=u'ICONFINDER ApS',
                business_address=u'Pilestr\xe6de 43 2\n1112 K\xf8benhavn K'
            )),
            ('99999O99', VatNumberCheckResult(False)),
            ('9999999', VatNumberCheckResult(False)),
            ('999999900', VatNumberCheckResult(False)),
        ]:
            self.assert_result_equals(expected,
                                      check_vat_number(vat_number,
                                                       country_code='DK'))
            self.assert_result_equals(expected,
                                      check_vat_number('DK%s' % (vat_number),
                                                       country_code='DK'))


__all__ = ('IsVatNumberFormatValidTestCase', 'CheckVatNumberTestCase', )
