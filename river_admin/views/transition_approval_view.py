from rest_framework.generics import get_object_or_404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from river.models import TransitionApproval, Transition

from river_admin.views import get, ApprovalHookDto, Q
from river_admin.views.serializers import TransitionApprovalDto


@get(r'^transition-approval/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition_approval = get_object_or_404(TransitionApproval.objects.all(), pk=pk)
    return Response(TransitionApprovalDto(transition_approval).data, status=HTTP_200_OK)


@get(r'^transition-approval/get-by-transition/(?P<transition_id>\w+)/$')
def get_by_transition(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)
    return Response(TransitionApprovalDto(transition.transition_approval.all()).data, status=HTTP_200_OK)


@get(r'^transition-approval/approval-hook/list/(?P<transition_approval_id>\w+)/$')
def list_approval_hooks(request, transition_approval_id):
    transition_approval = get_object_or_404(TransitionApproval.objects.all(), pk=transition_approval_id)
    return Response(ApprovalHookDto(transition_approval.meta.on_approved_hooks.filter(Q(object_id__isnull=True) | Q(object_id=transition_approval.object_id)), many=True).data, status=HTTP_200_OK)
