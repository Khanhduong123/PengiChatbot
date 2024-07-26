from apps.documents.constants import ErrorCode
from apps.exceptions import BadRequest


class ErrorFormat(BadRequest):
    DETAIL = ErrorCode.ERROR_FORMAT


class ErrorUpload(BadRequest):
    DETAIL = ErrorCode.ERROR_UPLOAD


class ErrorDelete(BadRequest):
    DETAIL = ErrorCode.ERROR_DELETE