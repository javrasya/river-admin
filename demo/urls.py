from django.conf.urls import url

from demo.view import approve_issue, approve_shipping

urlpatterns = [
    url(r'^approve_issue/(?P<issue_id>\d+)/(?P<next_state_id>\d+)/$', approve_issue, name='approve_issue'),
    url(r'^approve_shipping/(?P<shipping_id>\d+)/(?P<next_state_id>\d+)/$', approve_shipping, name='approve_shipping'),
]
