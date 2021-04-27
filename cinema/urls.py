from django.urls import path, register_converter
from . import views
from .misc import DateConverter, SessionConverter


app_name = "cinema"


register_converter(DateConverter, "date")
register_converter(SessionConverter, "session")

urlpatterns = [
    path("createhall/", views.CreateHallView.as_view(), name="createhall"),
    path("updatehall/<int:pk>/", views.UpdateHallView.as_view(), name="updatehall"),
    path("createsession/", views.CreateSessionView.as_view(), name="createsession"),
    path("updatesession/<int:pk>/", views.UpdateSessionView.as_view(), name="updatesession"),
    path("booksession/<session:s>/<date:date>/", views.CreateBookedSessionView.as_view(), name="booksession"),
]