from pyvat import (check_vat_number, is_vat_number_format_valid)
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


class CheckVatNumberTestCase(TestCase):
    """Test case for :func:`check_vat_number`.
    """

    def test_arbitrary__no_country_code(self):
        """check_vat_number(<arbitary>, country_code=None)
        """

        for vat_number, expected_result in [
            ('123456', False),
            ('NL043133502B02', True),
        ]:
            self.assertEqual(check_vat_number(vat_number).is_valid,
                             expected_result)

    def test_dk__no_country_code(self):
        """check_vat_number(<DK>, country_code=None)
        """

        for vat_number, expected_result in [
            ('DK33779437', True),
            ('DK99999O99', False),
            ('DK9999999', False),
            ('DK999999900', False),
        ]:
            self.assertEqual(check_vat_number(vat_number).is_valid,
                             expected_result)

    def test_dk__country_code(self):
        """check_vat_number(<DK>, country_code='DK')
        """

        for vat_number, expected_result in [
            ('33779437', True),
            ('99999O99', False),
            ('9999999', False),
            ('999999900', False),
        ]:
            self.assertEqual(check_vat_number(vat_number,
                                              country_code='DK').is_valid,
                             expected_result)
            self.assertEqual(check_vat_number('DK%s' % (vat_number),
                                              country_code='DK').is_valid,
                             expected_result)

__all__ = ('IsVatNumberFormatValidTestCase', 'CheckVatNumberTestCase', )
