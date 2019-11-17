from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import OnApprovedHook, TransitionApprovalMeta, TransitionApproval

from river_admin.views import post, delete, get
from river_admin.views.serializers import ApprovalHookDto, CreateApprovalHookDto


@post(r'^approval-hook/create/$')
def create_it(request):
    create_approval_hook_request = CreateApprovalHookDto(data=request.data)
    if create_approval_hook_request.is_valid():
        approval_hook = create_approval_hook_request.save()
        return Response({"id": approval_hook.pk}, status=HTTP_200_OK)
    else:
        return Response(create_approval_hook_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^approval-hook/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    hook = get_object_or_404(OnApprovedHook.objects.all(), pk=pk)
    hook.delete()
    return Response(status=status.HTTP_200_OK)
