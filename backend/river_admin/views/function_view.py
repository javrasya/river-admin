from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from river.models import Function

from river_admin.views import get, post, put, delete
from river_admin.views.serializers import UpdateFunctionDto, CreateFunctionDto, FunctionDto


@get(r'^function/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    function = get_object_or_404(Function.objects.all(), pk=pk)
    return Response(FunctionDto(function).data, status=HTTP_200_OK)


@get(r'^function/list/$')
def list_it(request):
    return Response(FunctionDto(Function.objects.all(), many=True).data, status=HTTP_200_OK)


@post(r'^function/create/')
def create_it(request):
    create_function_request = CreateFunctionDto(data=request.data)
    if create_function_request.is_valid():
        function = create_function_request.save()
        return Response({"id": function.id}, status=HTTP_200_OK)
    else:
        return Response(create_function_request.errors, status=HTTP_400_BAD_REQUEST)


@put(r'^function/update/(?P<pk>\w+)/$')
def update_it(request, pk):
    function = get_object_or_404(Function.objects.all(), pk=pk)
    update_function_request = UpdateFunctionDto(data=request.data, instance=function)

    if update_function_request.is_valid():
        update_function_request.save()
        return Response({"message": "Function is updated"}, status=HTTP_200_OK)
    else:
        return Response(update_function_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^function/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    function = get_object_or_404(Function.objects.all(), pk=pk)
    function.delete()
    return Response(status=HTTP_200_OK)
