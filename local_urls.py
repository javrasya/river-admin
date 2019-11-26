import os

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("river_admin.urls")),
    url(r'^api-auth/', include('rest_framework.urls')),
]

if os.environ.get("PRODUCTION", "false").lower() == "true":
    urlpatterns += [url(r'^demo/', include('demo.urls')), ]
