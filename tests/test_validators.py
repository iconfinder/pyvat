from pyvat import (
    check_vat_number,
    is_vat_number_format_valid,
    VatNumberCheckResult,
)
from unittest import TestCase


class IsVatNumberFormatValidTestCase(TestCase):
    """Test case for :func:`is_vat_number_format_valid`.
    """

    def test_dk__no_country_code(self):
        """is_vat_number_format_valid(<DK>, country_code=None)
        """

        for vat_number, expected_result in [
            ('DK 12 34 56 78', True),
            ('DK12345678', True),
            ('dk12345678', True),
            ('DK00000000', True),
            ('DK99999999', True),
            ('DK99999O99', False),
            ('DK9999999', False),
            ('DK999999900', False),
        ]:
            self.assertEqual(is_vat_number_format_valid(vat_number),
                             expected_result)

    def test_nl__no_country_code(self):
        """is_vat_number_format_valid(<NL>, country_code=None)
        """

        for vat_number, expected_result in [
            ('NL043133502B02', True),
        ]:
            self.assertEqual(is_vat_number_format_valid(vat_number),
                             expected_result)

    def test_at__no_country_code(self):
        """is_vat_number_format_valid(<AT>, country_code=None)
        """

        for vat_number, expected_result in [
            ('ATU68103312', True),
        ]:
            self.assertEqual(is_vat_number_format_valid(vat_number),
                             expected_result)

    def test_dk__country_code(self):
        """is_vat_number_format_valid(<DK>, country_code='DK')
        """

        for vat_number, expected_result in [
            ('12 34 56 78', True),
            ('12345678', True),
            ('12345678', True),
            ('00000000', True),
            ('99999999', True),
            ('99999O99', False),
            ('9999999', False),
            ('999999900', False),
        ]:
            self.assertEqual(is_vat_number_format_valid(vat_number,
                                                        country_code='DK'),
                             expected_result)
            self.assertEqual(is_vat_number_format_valid('DK%s' % (vat_number),
                                                        country_code='DK'),
                             expected_result)

    def test_ie__country_code(self):
        """is_vat_number_format_valid(<IE>, country_code='IE')
        """

        for vat_number, expected_result in [
            ('1114174HH', True),
        ]:
            self.assertEqual(is_vat_number_format_valid(vat_number,
                                                        country_code='IE'),
                             expected_result)
            self.assertEqual(is_vat_number_format_valid('IE%s' % (vat_number),
                                                        country_code='IE'),
                             expected_result)


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
