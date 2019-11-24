from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from river.models import Transition

from river_admin.views import get
from river_admin.views.serializers import TransitionDto, TransitionHookDto, TransitionApprovalDto


@get(r'^transition/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition = get_object_or_404(Transition.objects.all(), pk=pk)
    return Response(TransitionDto(transition).data, status=HTTP_200_OK)


@get(r'^transition/transition-approval/list/(?P<transition_id>\w+)/$')
def list_transition_approvals(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)

    return Response(TransitionApprovalDto(transition.transition_approvals.all().order_by("transition", "priority"), many=True).data, status=HTTP_200_OK)


@get(r'^transition/transition-hook/list/(?P<transition_id>\w+)/$')
def list_transition_hooks(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)
    return Response(
        TransitionHookDto(
            transition.meta.on_transit_hooks.filter(Q(object_id__isnull=True) | Q(object_id=transition.object_id)),
            many=True
        ).data,
        status=HTTP_200_OK
    )
