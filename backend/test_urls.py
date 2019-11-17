from rest_framework.authtoken.views import obtain_auth_token

from river_admin.views import urls

from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^api-token-auth/', obtain_auth_token),
                  url(r'^api-auth/', include('rest_framework.urls')),
              ] + urls
