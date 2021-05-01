from .API.resources import HallViewSet, SessionViewSet
from rest_framework import routers

app_name = "api"

router = routers.SimpleRouter()
router.register(r'halls', HallViewSet)
router.register(r'sessions', SessionViewSet)
urlpatterns = router.urls
