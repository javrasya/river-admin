from django.contrib.auth.models import Permission, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from river_admin.views import get
from river_admin.views.serializers import PermissionDto, GroupDto, UserDto


@get(r'^permission/get/(?P<pk>\w+)/$')
def get_permission(request, pk):
    permission = get_object_or_404(Permission.objects.all(), pk=pk)
    return Response(PermissionDto(permission).data, status=HTTP_200_OK)


@get(r'^permission/list/$')
def list_permissions(request):
    return Response(PermissionDto(Permission.objects.all(), many=True).data, status=HTTP_200_OK)


@get(r'^group/get/(?P<pk>\w+)/$')
def get_group(request, pk):
    group = get_object_or_404(Group.objects.all(), pk=pk)
    return Response(GroupDto(group).data, status=HTTP_200_OK)


@get(r'^group/list/$')
def list_group(request):
    return Response(GroupDto(Group.objects.all(), many=True).data, status=HTTP_200_OK)


@get(r'^user/get/$')
def get_user_profile(request):
    return Response(UserDto(request.user).data, status=HTTP_200_OK)


@get(r'^user/has_river_permission/(?P<operation>\w+)/(?P<object_type>\w+)/$')
def has_river_permission(request, operation, object_type):
    available_operations = ["add", "change", "delete", "view"]
    if operation in available_operations:
        return Response(request.user.has_perm("river.%s_%s" % (operation, object_type)), status=HTTP_200_OK)
    else:
        return Response({"message": "Invalid operation '%s'. Available operations are '%s'" % (operation, available_operations)}, status=HTTP_400_BAD_REQUEST)
