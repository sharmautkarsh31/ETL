from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from productimporter.products.models import Product
from productimporter.products.serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins

from productimporter.utils.csrf_exempt import CsrfExemptSessionAuthentication
from productimporter.utils.helpers import PaginationClass, make_base_url


class ProductViewSet(ModelViewSet):
    """
           CRUD/search/filter Products
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['active',]
    search_fields = ['name', 'sku']
    pagination_class = PaginationClass
    lookup_field = 'id'

    def get_serializer_context(self):
        return make_base_url(self.request)


class DeleteProductsViewSet(GenericViewSet, mixins.ListModelMixin):
    """
        View for deleting products
    """
    http_method_names = ['post', 'options', 'get']
    serializer_class = None
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset.delete()
        return Response({"status":"deleted all products"})
