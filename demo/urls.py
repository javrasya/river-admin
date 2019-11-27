from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from demo.view import approve_issue, approve_shipping

urlpatterns = [
    url(r'^approve_issue/(?P<issue_id>\d+)/(?P<next_state_id>\d+)/$', approve_issue, name='approve_issue'),
    url(r'^approve_shipping/(?P<shipping_id>\d+)/(?P<next_state_id>\d+)/$', approve_shipping, name='approve_shipping'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include("river_admin.urls")),
    url(r'^api-auth/', include('rest_framework.urls')),
]
