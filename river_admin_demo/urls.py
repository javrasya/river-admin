from django.conf.urls import url

from river_admin_demo.view import approve_issue, approve_shipping

urlpatterns = [
    url(r'^approve_issue/(?P<issue_id>\d+)/(?P<next_state_id>\d+)/$', approve_issue, name='approve_ticket'),
    url(r'^approve_shipping/(?P<shipping_id>\d+)/(?P<next_state_id>\d+)/$', approve_shipping, name='approve_shipping'),
]
