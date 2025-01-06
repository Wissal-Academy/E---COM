from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet

router = DefaultRouter()
router.register('carts', CartViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls))
]
