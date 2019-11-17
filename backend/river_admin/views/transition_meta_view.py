from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import TransitionMeta, Workflow

from river_admin.views import get, post
from river_admin.views.serializers import TransitionMetaDto, CreateTransitionMetaDto, TransitionHookDto, TransitionApprovalMetaDto


@get(r'^transition-meta/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition_meta = get_object_or_404(TransitionMeta.objects.all(), pk=pk)
    return Response(TransitionMetaDto(transition_meta).data, status=HTTP_200_OK)


@get(r'^transition-meta/list/$')
def list_it(request):
    return Response(TransitionMetaDto(TransitionMeta.objects.all(), many=True).data, status=HTTP_200_OK)


@post(r'^transition-meta/create/$')
def create_it(request):
    create_transition_meta_request = CreateTransitionMetaDto(data=request.data)
    if create_transition_meta_request.is_valid():
        transition_meta = create_transition_meta_request.save()
        return Response({"id": transition_meta.id}, status=HTTP_200_OK)
    else:
        return Response(create_transition_meta_request.errors, status=HTTP_400_BAD_REQUEST)


@get(r'^transition-meta/transition-approval-meta/list/(?P<transition_meta_id>\w+)/$')
def list_transition_approval_meta(request, transition_meta_id):
    transition_meta = get_object_or_404(TransitionMeta.objects.all(), pk=transition_meta_id)

    return Response(TransitionApprovalMetaDto(transition_meta.transition_approval_meta.all().order_by("transition_meta", "priority"), many=True).data, status=HTTP_200_OK)


@get(r'^transition-meta/transition-hook/list/(?P<transition_meta_id>\w+)/$')
def list_transition_hooks(request, transition_meta_id):
    transition_meta = get_object_or_404(TransitionMeta.objects.all(), pk=transition_meta_id)
    return Response(TransitionHookDto(transition_meta.on_transit_hooks.filter(transition__isnull=True, object_id__isnull=True), many=True).data, status=HTTP_200_OK)
