from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from productimporter.products.serializers import DownloadProductsSerializer
from productimporter.utils.csrf_exempt import CsrfExemptSessionAuthentication


class DownloadCsvViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
        View for downloading csv and processing it.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    http_method_names = ['post', 'options', 'get']
    serializer_class = DownloadProductsSerializer
    queryset = None


