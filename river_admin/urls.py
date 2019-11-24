from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from river_admin.views import urls

urlpatterns = [
                  url(r'^api-token-auth/', obtain_auth_token),
              ] + urls
