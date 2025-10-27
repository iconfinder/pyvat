import os
import requests
import xml.dom.minidom

from requests import Timeout

from .result import VatNumberCheckResult
from .xml_utils import get_first_child_element, get_text, NodeNotFoundError
from .exceptions import ServerError
from .utils import first_child_by_localname


class Registry(object):
    """Abstract base registry.

    Defines an explicit interface for accessing arbitary registries.
    """

    def check_vat_number(self, vat_number, country_code, test):
        """Check if a VAT number is valid according to the registry.

        :param vat_number: VAT number without country code prefix.
        :param country_code: ISO 3166-1-alpha-2 country code.
        :param test: Boolean to identify if test or not.
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

    DEFAULT_TIMEOUT = 8
    """Timeout for the requests."""

    def check_vat_number_with_request_identifier(self, vat_number, requester_country_code, requester_vat_number, country_code):
        """
        Checks VAT number via checkVatApprox, complies with privacy logging (GDPR).
        """
        if country_code == 'GR':
            country_code = 'EL'

        result = VatNumberCheckResult()

        # --- build SOAP for checkVatApprox ---
        def _tag(name, val):
            # Omit empty optionals; VIES accepts missing optionals
            return f'<ns0:{name}>{val}</ns0:{name}>' if val not in (None, "") else ''

        request_data = (
            u'<?xml version="1.0" encoding="UTF-8"?>'
            u'<SOAP-ENV:Envelope '
            u'xmlns:ns0="urn:ec.europa.eu:taxud:vies:services:checkVat:types" '
            u'xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" '
            u'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">'
            u'<SOAP-ENV:Header/>'
            u'<ns1:Body>'
            u'  <ns0:checkVatApprox>'
            u'    <ns0:countryCode>%s</ns0:countryCode>'
            u'    <ns0:vatNumber>%s</ns0:vatNumber>'
            # all of these are optional; leave out unless you want to use them
            f'    {_tag("traderName", None)}'
            f'    {_tag("traderCompanyType", None)}'
            f'    {_tag("traderStreet", None)}'
            f'    {_tag("traderPostcode", None)}'
            f'    {_tag("traderCity", None)}'
            f'    {_tag("requesterCountryCode", requester_country_code)}'
            f'    {_tag("requesterVatNumber", requester_vat_number)}'
            u'  </ns0:checkVatApprox>'
            u'</ns1:Body>'
            u'</SOAP-ENV:Envelope>'
        ) % (country_code, vat_number)

        # GDPR/PII-aware logging
        DEBUG_VAT_LOGS = os.environ.get("DEBUG_VAT_LOGS", "0") == "1"
        if DEBUG_VAT_LOGS:
            # Redact PII in logs
            redacted_request = request_data
            redacted_request = redacted_request.replace(vat_number, "[REDACTED-VAT]")
            if requester_vat_number:
                redacted_request = redacted_request.replace(requester_vat_number, "[REDACTED-REQUESTER]")
            result.log_lines.append(u'> POST %s with payload of content type text/xml, charset UTF-8 (REDACTED).' % (self.CHECK_VAT_SERVICE_URL,))
            result.log_lines.append(redacted_request)
        else:
            result.log_lines.append(u'> VIES checkVatApprox API call issued (request payload redacted for privacy)')

        try:
            response = requests.post(
                self.CHECK_VAT_SERVICE_URL,
                data=request_data.encode('utf-8'),
                headers={'Content-Type': 'text/xml; charset=utf-8'},
                timeout=self.DEFAULT_TIMEOUT
            )
            # REMOVE: response.request_identifier (not a requests attr)
        except Timeout as e:
            result.log_lines.append(u'< Request to EU VIES registry timed out: {}'.format(e))
            return result
        except Exception as exception:
            result.log_lines.append(u'< Request failed with exception: %r' % (exception))
            return result

        content_type = response.headers.get('Content-Type', '')

        # Only log full response status if debug, else only status, not body
        if DEBUG_VAT_LOGS:
            log_response_text = response.text
            # Redact PII (replace VAT numbers, request identifiers)
            log_response_text = log_response_text.replace(vat_number, "[REDACTED-VAT]")
            if requester_vat_number:
                log_response_text = log_response_text.replace(requester_vat_number, "[REDACTED-REQUESTER]")
            result.log_lines.append(
                u'< Response with status %d of content type %s (REDACTED):' %
                (response.status_code, content_type)
            )
            result.log_lines.append(log_response_text)
        else:
            result.log_lines.append(
                u'< VIES response status: %d, content-type: %s (response content redacted for privacy)' %
                (response.status_code, content_type)
            )

        if response.status_code != 200 or not content_type.startswith('text/xml'):
            result.log_lines.append(u'< Response is nondeterministic due to invalid response status code or MIME type')
            return result

        # ---- Robust XML parsing (ignore prefixes) ----
        dom = xml.dom.minidom.parseString(response.text)

        envelope_node = dom.documentElement
        env_local = getattr(envelope_node, "localName", None) or envelope_node.tagName
        if not (env_local == "Envelope" or env_local.endswith(":Envelope")):
            raise ValueError('expected response XML root element to be a SOAP envelope')

        body_node = None
        try:
            body_node = get_first_child_element(envelope_node, 'env:Body')
        except Exception:
            body_node = first_child_by_localname(envelope_node, 'Body')

        # Fault handling (prefix-agnostic)
        try:
            error_node = get_first_child_element(body_node, 'env:Fault')
            fault_strings = error_node.getElementsByTagName('faultstring')
            fault_code = fault_strings[0].firstChild.nodeValue
            raise ServerError(fault_code)
        except NodeNotFoundError:
            try:
                fault_node = first_child_by_localname(body_node, 'Fault')
                fault_strings = fault_node.getElementsByTagName('faultstring')
                fault_code = fault_strings[0].firstChild.nodeValue
                raise ServerError(fault_code)
            except Exception:
                pass

        try:
            check_vat_response_node = get_first_child_element(body_node, 'ns2:checkVatApproxResponse')
        except Exception:
            check_vat_response_node = next(
                c for c in body_node.childNodes
                if getattr(c, "localName", "") == "checkVatApproxResponse"
            )

        # valid
        try:
            valid_node = get_first_child_element(check_vat_response_node, 'ns2:valid')
        except Exception:
            valid_node = first_child_by_localname(check_vat_response_node, 'valid')

        valid_text = get_text(valid_node)
        if valid_text in ('true', 'false'):
            result.is_valid = (valid_text == 'true')
        else:
            result.log_lines.append(u'< Response is nondeterministic due to invalid validity field: %r' % (valid_text))

        # traderName -> business_name
        try:
            try:
                name_node = get_first_child_element(check_vat_response_node, 'ns2:traderName')
            except Exception:
                name_node = first_child_by_localname(check_vat_response_node, 'traderName')
            result.business_name = (get_text(name_node) or '').strip() or None
        except Exception:
            pass

        # traderAddress -> business_address
        try:
            try:
                address_node = get_first_child_element(check_vat_response_node, 'ns2:traderAddress')
            except Exception:
                address_node = first_child_by_localname(check_vat_response_node, 'traderAddress')
            result.business_address = (get_text(address_node) or '').strip() or None
        except Exception:
            pass

        # countryCode
        try:
            try:
                cc_node = get_first_child_element(check_vat_response_node, 'ns2:countryCode')
            except Exception:
                cc_node = first_child_by_localname(check_vat_response_node, 'countryCode')
            result.business_country_code = (get_text(cc_node) or '').strip() or None
        except Exception:
            pass

        # requestIdentifier
        try:
            try:
                ri_node = get_first_child_element(check_vat_response_node, 'ns2:requestIdentifier')
            except Exception:
                ri_node = first_child_by_localname(check_vat_response_node, 'requestIdentifier')
            result.request_identifier = (get_text(ri_node) or '').strip() or None
        except Exception:
            result.request_identifier = None

        # Essential summary log (NO PII or full objects)
        summary = (
            u'< VIES checkVatApprox result: '
            u'validity=%r, '
            u'status_code=%s, '
            u'requestIdentifier=%r'
        ) % (
            result.is_valid,
            response.status_code,
            result.request_identifier
        )
        result.log_lines.append(summary)

        return result
    
    def check_vat_number(self, vat_number, country_code, test):
        # Non-ISO code used for Greece.
        if country_code == 'GR':
            country_code = 'EL'

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
                },
                timeout=self.DEFAULT_TIMEOUT
            )
        except Timeout as e:
            result.log_lines.append(u'< Request to EU VIEW registry timed out:'
                                    u' {}'.format(e))
            return result
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
                                    u'invalid response status code or MIME '
                                    u'type')
            return result

        # Parse the DOM and validate as much as we can.
        #
        # We basically expect the result structure to be as follows,
        # where the address and name nodes might be omitted.
        #
        # <env:Envelope
        #     xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
        #         <env:Header/>
        #         <env:Body>
        #         <ns2:checkVatResponse
        #              xmlns:ns2="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
        #              <ns2:countryCode>DE</ns2:countryCode>
        #              <ns2:vatNumber>812383453</ns2:vatNumber>
        #              <ns2:requestDate>2022-08-12+02:00</ns2:requestDate>
        #              <ns2:valid>true</ns2:valid>
        #              <ns2:name>---</ns2:name>
        #              <ns2:address>---</ns2:address>
        #         </ns2:checkVatResponse>
        #     </env:Body>
        # </env:Envelope>
        result_dom = xml.dom.minidom.parseString(response.text.encode('utf-8'))

        envelope_node = result_dom.documentElement
        if envelope_node.tagName != 'env:Envelope':
            raise ValueError(
                'expected response XML root element to be a SOAP envelope'
            )

        body_node = get_first_child_element(envelope_node, 'env:Body')

        # Check for server errors
        try:
            error_node = get_first_child_element(body_node, 'env:Fault')
            fault_strings = error_node.getElementsByTagName('faultstring')
            fault_code = fault_strings[0].firstChild.nodeValue
            raise ServerError(fault_code)
        except NodeNotFoundError:
            pass

        try:
            check_vat_response_node = get_first_child_element(
                body_node,
                'ns2:checkVatResponse'
            )
            valid_node = get_first_child_element(
                check_vat_response_node,
                'ns2:valid'
            )
        except Exception as e:
            result.log_lines.append(u'< Response is nondeterministic due to '
                                    u'invalid response body: %r' % (e))
            return result

        # Parse the validity of the business.
        valid_text = get_text(valid_node)

        if valid_text in frozenset(('true', 'false')):
            result.is_valid = valid_text == 'true'
        else:
            result.log_lines.append(u'< Response is nondeterministic due to '
                                    u'invalid validity field: %r' %
                                    (valid_text))

        # Parse the business name and address if possible.
        try:
            name_node = get_first_child_element(
                check_vat_response_node,
                'ns2:name'
            )
            result.business_name = get_text(name_node).strip() or None
        except Exception:
            pass

        try:
            address_node = get_first_child_element(
                check_vat_response_node,
                'ns2:address'
            )
            result.business_address = get_text(address_node).strip() or None
        except Exception:
            pass
        
        # Parse the country code if possible.
        try:
            country_code_node = get_first_child_element(
                check_vat_response_node,
                'ns2:countryCode'
            )
            result.business_country_code = get_text(country_code_node).strip() or None
        except Exception:
            pass

        return result


class HMRCRegistry(Registry):
    """HMRC registry.

    Uses the HMRC API for validating VAT numbers.
    """

    CHECK_VAT_SERVICE_URL = 'https://api.service.hmrc.gov.uk/organisations/' \
                            'vat/check-vat-number/lookup/'
    CHECK_VAT_SERVICE_TEST_URL = 'https://test-api.service.hmrc.gov.uk/organisations/' \
                                 'vat/check-vat-number/lookup/'
    """URL for the VAT checking service.
    """

    DEFAULT_TIMEOUT = 8
    """Timeout for the requests."""

    def check_vat_number(self, vat_number, country_code, test):
        # Request information about the VAT number.
        result = VatNumberCheckResult()
        result.is_valid = False
        try:
            url = self.CHECK_VAT_SERVICE_URL
            if test:
                url = self.CHECK_VAT_SERVICE_TEST_URL
            response = requests.get(
                url + vat_number,
                timeout=self.DEFAULT_TIMEOUT
            )
        except Timeout as e:
            result.log_lines.append(u'< Request to HMRC registry timed out:'
                                    u' {}'.format(e))
            return result
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
                not response.headers['Content-Type'].startswith('application/json'):
            result.log_lines.append(u'< Response is nondeterministic due to '
                                    u'invalid response status code or MIME '
                                    u'type')
            return result

        # Parse the DOM and validate as much as we can.
        #
        # We basically expect the result structure to be as follows,
        # where the address and name nodes might be omitted.
        #
        # {
        #     "target": {
        #         "name": "Credite Sberger Donal Inc.",
        #         "vatNumber": "553557881",
        #         "address": {
        #             "line1": "131B Barton Hamlet",
        #             "postcode": "SW97 5CK",
        #             "countryCode": "GB"
        #         }
        #     },
        #     "processingDate": "2022-09-29T12:08:48+01:00"
        # }

        json_response = response.json()
        target = json_response.get('target', None)
        if target:
            result.is_valid = True
            result.business_name = target.get('name', None)
            address = target.get('address', {})
            if address:
                business_address = ', '.join(list(address.values()))
                result.business_address = business_address
        return result


__all__ = ('Registry', 'ViesRegistry', 'HMRCRegistry', )
