from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, VisitanteViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'visitantes', VisitanteViewSet, basename='visitantes')

urlpatterns = router.urls
