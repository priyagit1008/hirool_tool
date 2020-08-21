import os

# django imports.
from api.settings import BASE_DIR


BAD_REQUEST = {
    "error_code": "ERR_4000",
    "detail": "Bad Request."
}

BAD_ACTION = {
    "error_code": "ERR_4005",
    "detail": "Bad Action."
}

OPERATION_NOT_ALLOWED = {
    "error_code": "ERR_4012",
    "code": "FT_4012",
    "detail": "Operation not allowed"
}
# down_file = os.path.join(BASE_DIR,"media/user_resumes")
# down_file = 'f7e32601-1169-4f54-bc9d-ee655cc97364'
# os.path.join(BASE_DIR, "media")
