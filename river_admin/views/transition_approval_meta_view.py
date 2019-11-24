from django.db import transaction
from django.db.models import F
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import TransitionApprovalMeta

from river_admin.views import get, post, delete
from river_admin.views.serializers import RePrioritizeTransitionApprovalMetaDto, TransitionApprovalMetaDto, CreateTransitionApprovalMetaDto, ApprovalHookDto


@get(r'^transition-approval-meta/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=pk)
    return Response(TransitionApprovalMetaDto(transition_approval_meta).data, status=HTTP_200_OK)


@get(r'^transition-approval-meta/list/$')
def list_it(request):
    return Response(TransitionApprovalMetaDto(TransitionApprovalMeta.objects.all(), many=True).data, status=HTTP_200_OK)


@delete(r'^transition-approval-meta/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=pk)
    transition_approval_meta.delete()
    return Response(status=HTTP_200_OK)


@post(r'^transition-approval-meta/create/$')
def create_it(request):
    create_transition_approval_meta_request = CreateTransitionApprovalMetaDto(data=request.data)
    if create_transition_approval_meta_request.is_valid():
        transition_approval_meta = create_transition_approval_meta_request.save()
        return Response({"id": transition_approval_meta.id}, status=HTTP_200_OK)
    else:
        return Response(create_transition_approval_meta_request.errors, status=HTTP_400_BAD_REQUEST)


@transaction.atomic
@post(r'^transition-approval-meta/re-prioritize/')
def re_prioritize_it(request):
    re_prioritize_transition_approval_meta_request = RePrioritizeTransitionApprovalMetaDto(data=request.data, many=True)
    if re_prioritize_transition_approval_meta_request.is_valid():

        request_map = {
            reprioritize_request["transition_approval_meta_id"]: reprioritize_request["priority"]
            for reprioritize_request in re_prioritize_transition_approval_meta_request.validated_data
        }

        TransitionApprovalMeta.objects.filter(pk__in=request_map.keys()).update(priority=F('priority') + len(request_map.keys()) * 10)
        for transition_approval_meta_id, priority in request_map.items():
            transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=transition_approval_meta_id)
            transition_approval_meta.priority = priority
            transition_approval_meta.save()

        return Response(status=HTTP_200_OK)
    else:
        return Response(re_prioritize_transition_approval_meta_request.errors, status=HTTP_400_BAD_REQUEST)


@get(r'^transition-approval-meta/approval-hook/list/(?P<transition_approval_meta_id>\w+)/$')
def list_approval_hooks(request, transition_approval_meta_id):
    transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=transition_approval_meta_id)
    return Response(
        ApprovalHookDto(
            transition_approval_meta.on_approved_hooks.filter(transition_approval__isnull=True, object_id__isnull=True),
            many=True
        ).data,
        status=HTTP_200_OK
    )
