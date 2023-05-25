from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from teste_brmed.users.api.views import UserViewSet
from core.viewsets import CotacaoViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(r'cotacoes', CotacaoViewSet)

app_name = "api"
urlpatterns = router.urls
