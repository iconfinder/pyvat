import requests
from .result import VatNumberCheckResult


class Registry(object):
    """Abstract base registry.

    Defines an explicit interface for accessing arbitary registries.
    """

    def check_vat_number(self, vat_number, country_code):
        """Check if a VAT number is valid according to the registry.

        :param vat_number: VAT number without country code prefix.
        :param country_code: ISO 3166-1-alpha-2 country code.
        :returns: a :class:`VatNumberCheckResult` instance.
        """

        raise NotImplementedError()


class ViesRegistry(Registry):
    """VIES registry.

    Uses the European Commision's VIES registry for validating VAT numbers.
    """

    CHECK_VAT_SERVICE_URL = 'http://ec.europa.eu/taxation_customs/vies/' \
        'services/checkVatService'
    """URL for the VAT checking service.
    """

    def check_vat_number(self, vat_number, country_code):
        # Request information about the VAT number.
        result = VatNumberCheckResult()

        request_data = (
            u'<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope'
            u' xmlns:ns0="urn:ec.europa.eu:taxud:vies:services:checkVa'
            u't:types" xmlns:ns1="http://schemas.xmlsoap.org/soap/enve'
            u'lope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-insta'
            u'nce" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/env'
            u'elope/"><SOAP-ENV:Header/><ns1:Body><ns0:checkVat><ns0:c'
            u'ountryCode>%s</ns0:countryCode><ns0:vatNumber>%s</ns0:va'
            u'tNumber></ns0:checkVat></ns1:Body></SOAP-ENV:Envelope>' %
            (country_code, vat_number)
        )

        result.log_lines += [
            u'> POST %s with payload of content type text/xml, charset UTF-8:',
            request_data,
        ]

        try:
            response = requests.post(
                self.CHECK_VAT_SERVICE_URL,
                data=request_data.encode('utf-8'),
                headers={
                    'Content-Type': 'text/xml; charset=utf-8',
                }
            )
        except Exception as exception:
            # Do not completely fail problematic requests.
            result.log_lines.append(u'< Request failed with exception: %r' %
                                    (exception))
            return result

        # Log response information.
        result.log_lines += [
            u'< Response with status %d of content type %s:' %
            (response.status_code, response.headers['Content-Type']),
            response.text,
        ]

        # Do not completely fail problematic requests.
        if response.status_code != 200 or \
                not response.headers['Content-Type'].startswith('text/xml'):
            result.log_lines.append(u'< Response is nondeterministic due to '
                                    'invalid response status code or MIME '
                                    'type')
            return result

        # This is very rudimentary but also very fast.
        result.is_valid = '<valid>true</valid>' in response.text
        return result


__all__ = ('Registry', 'ViesRegistry', )
