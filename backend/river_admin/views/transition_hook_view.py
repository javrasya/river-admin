from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import OnTransitHook

from river_admin.views import post, delete
from river_admin.views.serializers import CreateTransitionHookDto


@post(r'^transition-hook/create/$')
def create_it(request):
    create_transition_hook_request = CreateTransitionHookDto(data=request.data)
    if create_transition_hook_request.is_valid():
        transition_hook = create_transition_hook_request.save()
        return Response({"id": transition_hook.pk}, status=HTTP_200_OK)
    else:
        return Response(create_transition_hook_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^transition-hook/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    hook = get_object_or_404(OnTransitHook.objects.all(), pk=pk)
    hook.delete()
    return Response(status=status.HTTP_200_OK)
