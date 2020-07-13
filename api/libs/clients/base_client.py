# python core library imports
import logging
from urllib.parse import urljoin

# django imports
from rest_framework.status import (
    is_success,
    is_client_error,
)

# third party imports
import requests

# project level imports
from libs.exceptions import (
    ParseException,
    NetworkException,
    BadRequestException,
    ResourceConflictException,
    ResourceNotFoundException,
)


logger = logging.getLogger(__name__)


class BaseClient(object):
    """
    BaseClient class is an abstract class which acts as a wrapper around
    python's requests library.
    """
    def __init__(self, host, do_log=False):
        """
        Initialize BaseClient objects
        """
        self.host = host
        self.do_log = do_log

    def parse_data_from_response(self, response, method):
        if method in ('HEAD', 'head'):
            return response

        if is_success(response.status_code):
            if response.status_code == requests.codes.no_content:
                return {}
            if self.do_log:
                logger.info("Success Response: {}".format(response.text))

            response_type = response.headers.get('Content-Type')
            if 'text' in response_type:
                return response.text

            return response.json()

        logger.error('Failure Response: {}'.format(response.text))

        logger_message = {
            'url': response.url,
            'response': response.text
        }

        # map response to corresponding exception, add exceptions here as required
        if response.status_code == requests.codes.bad_request:
            raise BadRequestException(logger_message)
        if response.status_code == requests.codes.not_found:
            raise ResourceNotFoundException(logger_message)
        if response.status_code == requests.codes.conflict:
            raise ResourceConflictException(logger_message)

        if is_client_error(response.status_code):  # 4XX except above
            raise ParseException(logger_message)

        # for everything else
        raise NetworkException(logger_message)

    def request(self, method, url_path, params=None,
                data=None, headers=None, auth=None, timeout=None):

        # build URL using host and
        url = urljoin(self.host, url_path)

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                auth=auth,
                timeout=timeout
            )
        except requests.RequestException as inst:
            raise NetworkException from inst
        return self.parse_data_from_response(response, method)

    def head(self, url_path, params=None, data=None, headers=None,
             auth=None, timeout=None):

        return self.request(
            method='HEAD',
            url_path=url_path,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout
        )

    def get(self, url_path, params=None, data=None, headers=None,
            auth=None, timeout=None):

        return self.request(
            method='GET',
            url_path=url_path,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout
        )

    def post(self, url_path, params=None, data=None, headers=None,
             auth=None, timeout=None):

        return self.request(
            method='POST',
            url_path=url_path,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout
        )

    def patch(self, url_path, params=None, data=None, headers=None,
              auth=None, timeout=None):

        return self.request(
            method='PATCH',
            url_path=url_path,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout
        )

    def delete(self, url_path, params=None, data=None, headers=None,
               auth=None, timeout=None):

        return self.request(
            method='DELETE',
            url_path=url_path,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout
        )
