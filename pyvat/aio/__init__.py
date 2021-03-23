from ..item_type import ItemType
from ..party import Party
from .registries import ViesRegistry
from ..result import VatNumberCheckResult
from ..vat_charge import VatCharge, VatChargeAction

from .. import __version__

VIES_REGISTRY = ViesRegistry()
"""VIES registry instance.
"""


VAT_REGISTRIES = {
    'AT': VIES_REGISTRY,
    'BE': VIES_REGISTRY,
    'BG': VIES_REGISTRY,
    'CY': VIES_REGISTRY,
    'CZ': VIES_REGISTRY,
    'DE': VIES_REGISTRY,
    'DK': VIES_REGISTRY,
    'EE': VIES_REGISTRY,
    'ES': VIES_REGISTRY,
    'FI': VIES_REGISTRY,
    'FR': VIES_REGISTRY,
    'GR': VIES_REGISTRY,
    'HU': VIES_REGISTRY,
    'HR': VIES_REGISTRY,
    'IE': VIES_REGISTRY,
    'IT': VIES_REGISTRY,
    'LT': VIES_REGISTRY,
    'LU': VIES_REGISTRY,
    'LV': VIES_REGISTRY,
    'MT': VIES_REGISTRY,
    'NL': VIES_REGISTRY,
    'PL': VIES_REGISTRY,
    'PT': VIES_REGISTRY,
    'RO': VIES_REGISTRY,
    'SE': VIES_REGISTRY,
    'SK': VIES_REGISTRY,
    'SI': VIES_REGISTRY,
}
"""VAT registries.

Mapping from ISO 3166-1-alpha-2 country codes to the VAT registry capable of
validating the VAT number.
"""

from .. import decompose_vat_number
from .. import is_vat_number_format_valid


def check_vat_number(vat_number, country_code=None):
    """Check if a VAT number is valid.

    If possible, the VAT number will be checked against available registries.

    :param vat_number: VAT number to validate.
    :param country_code:
        Optional country code. Should be supplied if known, as there is no
        guarantee that naively entered VAT numbers contain the correct alpha-2
        country code prefix for EU countries just as not all non-EU countries
        have a reliable country code prefix. Default ``None`` prompting
        detection.
    :returns:
        a :class:`VatNumberCheckResult` instance containing the result for
        the full VAT number check.
    """

    # Decompose the VAT number.
    vat_number, country_code = decompose_vat_number(vat_number, country_code)
    if not vat_number or not country_code:
        return VatNumberCheckResult(False, [
            '> Unable to decompose VAT number, resulted in %r and %r' %
            (vat_number, country_code)
        ])

    # Test the VAT number format.
    format_result = is_vat_number_format_valid(vat_number, country_code)
    if format_result is not True:
        return VatNumberCheckResult(format_result, [
            '> VAT number validation failed: %r' % (format_result)
        ])

    # Attempt to check the VAT number against a registry.
    if country_code not in VAT_REGISTRIES:
        return VatNumberCheckResult()

    return VAT_REGISTRIES[country_code].check_vat_number(vat_number,
                                                         country_code)

from .. import get_sale_vat_charge

__all__ = (
    'check_vat_number',
    'get_sale_vat_charge',
    'is_vat_number_format_valid',
    ItemType.__name__,
    Party.__name__,
    VatCharge.__name__,
    VatChargeAction.__name__,
)
