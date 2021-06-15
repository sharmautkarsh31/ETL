from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from productimporter.products.models import Product


def generate_lazy_objs(df):
    for i, row in df.iterrows():
        yield Product(
            name=row['name'],
            sku=row['sku'],
            description=row['description']
        )

def make_base_url(request):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    return protocol+request.get_host()



class PaginationClass(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
