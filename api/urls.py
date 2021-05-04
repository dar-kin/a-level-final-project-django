from .API.resources import HallViewSet, SessionViewSet, UserViewSet, ClientSessionView, BookedSessionViewSet, \
    BookedSessionListViewSet
from rest_framework import routers
from django.urls import path

app_name = "api"

urlpatterns = [
    path("clients-session-list/<date:date>/<str:sort>/",
         ClientSessionView.as_view({"get": "list"}), name="clients-session-list"),
    path("clients-session-list/<date:date>/", ClientSessionView.as_view({"get": "list"}), name="clients-session-list"),
    path("create-booked-session/<session:s>/<date:date>/", BookedSessionViewSet.as_view({"post": "create"}),
         name="create-booked-session"),
    path("my-booked-sessions/", BookedSessionListViewSet.as_view({"get": "list"}), name="my-booked-sessions"),
    path("today-session-list/<time:start_range>/<time:end_range>/<hall:hall>/",
         ClientSessionView.as_view({"get": "get_sessions_in_time"}), name="today-session-list"),
    path("today-session-list/<time:start_range>/<time:end_range>/",
         ClientSessionView.as_view({"get": "get_sessions_in_time"}), name="today-session-list"),
    path("today-session-list/<hall:hall>/",
         ClientSessionView.as_view({"get": "get_sessions_in_time"}), name="today-session-list")
]
router = routers.SimpleRouter()
router.register(r'halls', HallViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'users', UserViewSet)
urlpatterns += router.urls
