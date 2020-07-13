from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ParseError,
    ValidationError,
)

# logger
import logging
logger = logging.getLogger(__name__)


class ResourceConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Record already exists."

    def __init__(self, fields=None):
        if fields is not None:
            self.detail += " Duplicate Value for: %s" % (str(fields))


class NetworkException(APIException):
    pass


class ResourceNotFoundException(NotFound):
    pass


class ParseException(ParseError):
    def __init__(self, detail=None, code=None, errors=None):
        if errors:
            logger.info(errors)
        return super(ParseException, self).__init__(detail, code)


class BadRequestException(ValidationError):
    pass
