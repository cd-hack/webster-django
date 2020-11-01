from rest_framework import pagination
from rest_framework.response import Response


class ProductPagination(pagination.PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'

    def get_paginated_response(self, data):
        return Response({'next':self.get_next_link(),
                        'previous':self.get_previous_link(),
                        'count':self.page.paginator.count,
                        'limit':self.page_size,
                        'results':data})