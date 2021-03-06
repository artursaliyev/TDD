from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list_views.home_page, name='index'),
    path('lists/', include(list_urls))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




