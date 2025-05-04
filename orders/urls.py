from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = router.urls
