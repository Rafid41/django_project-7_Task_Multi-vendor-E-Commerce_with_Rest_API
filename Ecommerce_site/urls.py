# Ecommerce_site\urls.py
from django.contrib import admin
from django.urls import path, include

# show media
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("account/", include("App_Login.urls")),
]


# media
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
