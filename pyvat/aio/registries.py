# import requests
import aiohttp
from asyncio import TimeoutError

import xml.dom.minidom

from ..result import VatNumberCheckResult
from ..xml_utils import get_first_child_element, get_text, NodeNotFoundError
from ..exceptions import ServerError
from ..registries import BaseViesRegistry

class ViesRegistry(BaseViesRegistry):
    """VIES registry."""


    async def check_vat_number(self, vat_number, country_code):
        # Non-ISO code used for Greece.
        if country_code == 'GR':
            country_code = 'EL'

        # Request information about the VAT number.
        result = VatNumberCheckResult()

        request_data = self.generate_request_data(vat_number, country_code)

        result.log_lines += [
            u'> POST %s with payload of content type text/xml, charset UTF-8:',
            request_data,
        ]

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.DEFAULT_TIMEOUT)) as session:
                async with session.post(
                    self.CHECK_VAT_SERVICE_URL, 
                    data=request_data.encode('utf-8'), 
                    headers={
                        'Content-Type': 'text/xml; charset=utf-8',
                }) as request:
                    response_text = await request.text()
                    result.log_lines += [
                        u'< Response with status %d of content type %s:' %
                        (request.status, request.headers['Content-Type']),
                        response_text,
                    ]

                    # Do not completely fail problematic requests.
                    if request.status != 200 or \
                        not request.headers['Content-Type'].startswith('text/xml'):
                            result.log_lines.append(u'< Response is nondeterministic due to '
                                                    u'invalid response status code or MIME '
                                                    u'type')
                            return result
        except TimeoutError as e:
            result.log_lines.append(u'< Request to EU VIEW registry timed out:'
                                    u' {}'.format(e))
            return result

        return self.parse_response_to_result(response_text, result)


__all__ = ('Registry', 'ViesRegistry', )
