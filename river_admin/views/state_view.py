from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import State

from river_admin.views import get, post, delete
from river_admin.views.serializers import StateDto, CreateStateDto


@get(r'^state/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    state = get_object_or_404(State.objects.all(), pk=pk)
    return Response(StateDto(state).data, status=HTTP_200_OK)


@get(r'^state/list/$')
def list_it(request):
    return Response(StateDto(State.objects.all(), many=True).data, status=HTTP_200_OK)


@post(r'^state/create/$')
def create_it(request):
    create_state_request = CreateStateDto(data=request.data)
    if create_state_request.is_valid():
        state = create_state_request.save()
        return Response({"id": state.id}, status=HTTP_200_OK)
    else:
        return Response(create_state_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^state/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    state = get_object_or_404(State.objects.all(), pk=pk)
    state.delete()
    return Response(status=HTTP_200_OK)
