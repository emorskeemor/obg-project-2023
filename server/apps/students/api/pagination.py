from rest_framework.pagination import PageNumberPagination

class StudentPaginator(PageNumberPagination):
    page_size = 5
    page_query_param: str = "page_size"
    