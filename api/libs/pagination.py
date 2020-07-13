from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
)


class ResultSetPagination(LimitOffsetPagination):
    """
    Base class for setting pagination of a list api respnose.
    """
    default_limit = 25
    max_limit = 100


class CursorSetPagination(CursorPagination):
    """
    Base class for setting Cursor Pagination for list api response.
    """
    page_size = 1
    max_page_size = 100
    page_size_query_param = 'page_size'
    ordering = '-created_at'


class RetrievalPagination(CursorSetPagination):
    """
    Retreival specific Cursor Pagination for list api response.
    """
    ordering = 'distance'
