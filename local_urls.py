from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("river_admin.urls")),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^demo/', include('river_admin_demo.urls')),
]
