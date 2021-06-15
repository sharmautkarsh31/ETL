from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from productimporter.files_manager.api import DownloadCsvViewSet
from productimporter.products.api import ProductViewSet, DeleteProductsViewSet
from productimporter.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename='user-details')
router.register("product", ProductViewSet, basename='product-view-set')
router.register("delete_products", DeleteProductsViewSet, basename='delete-product')
router.register("download_csv", DownloadCsvViewSet, basename='download-product')


app_name = "api"
urlpatterns = router.urls
