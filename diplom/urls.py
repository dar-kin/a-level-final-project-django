from django.contrib import admin
from django.urls import path, include
from customuser.views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("customuser/", include("customuser.urls", namespace="customuser")),
    path("cinema/", include("cinema.urls", namespace="cinema")),
    path('', MainView.as_view(), name="main")
]
