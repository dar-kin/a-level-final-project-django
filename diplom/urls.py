from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from customuser.views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("customuser/", include("customuser.urls", namespace="customuser")),
    path("cinema/", include("cinema.urls", namespace="cinema")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="js-catalog"),
    path('', MainView.as_view(), name="main")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
