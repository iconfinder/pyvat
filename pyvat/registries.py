import requests


class Registry(object):
    """Abstract base registry.

    Defines an explicit interface for accessing arbitary registries.
    """

    def is_vat_number_valid(self, vat_number, country_code):
        """Test if a VAT number is valid according to the registry.

        :param vat_number: VAT number without country code prefix.
        :param country_code: ISO 3166-1-alpha-2 country code.
        :returns: ``True`` if the country code is valid, otherwise ``False``.
        """

        raise NotImplementedError()


class ViesRegistry(Registry):
    """VIES registry.

    Uses the European Commision's VIES registry for validating VAT numbers.
    """

    def is_vat_number_valid(self, vat_number, country_code):
        # Request information about the VAT number.
        try:
            response = requests.post(
                'http://ec.europa.eu/taxation_customs/vies/services/'
                'checkVatService',
                data=(
                    u'<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope'
                    u' xmlns:ns0="urn:ec.europa.eu:taxud:vies:services:checkVa'
                    u't:types" xmlns:ns1="http://schemas.xmlsoap.org/soap/enve'
                    u'lope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-insta'
                    u'nce" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/env'
                    u'elope/"><SOAP-ENV:Header/><ns1:Body><ns0:checkVat><ns0:c'
                    u'ountryCode>%s</ns0:countryCode><ns0:vatNumber>%s</ns0:va'
                    u'tNumber></ns0:checkVat></ns1:Body></SOAP-ENV:Envelope>' %
                    (country_code,
                     vat_number)
                ).encode('utf-8'),
                headers={
                    'Content-Type': 'text/xml; charset=utf-8',
                }
            )
        except:
            # Do not completely fail problematic requests.
            return None

        # Do not completely fail problematic requests.
        if response.status_code != 200 or not response \
                .headers['Content-Type'].startswith('text/xml'):
            return None

        # This is very rudimentary but also very fast.
        return '<valid>true</valid>' in response.text


__all__ = ('Registry', 'ViesRegistry', )
