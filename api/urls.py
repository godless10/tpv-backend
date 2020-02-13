from django.urls import path,include
from . import views
from rest_framework import routers
from .views import ProductoViewSet,CategoriaViewSet,ProveedorViewSet,DetalleFacturaViewSet,FacturaViewSet

router=routers.DefaultRouter()
router.register('productos',ProductoViewSet)
router.register('categorias',CategoriaViewSet)
router.register('proveedores',ProveedorViewSet)
router.register('det_factura',DetalleFacturaViewSet)
router.register('facturas',FacturaViewSet)
#router.register('ratings',RatingViewSet)
#router.register('users',UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test', views.test),
]