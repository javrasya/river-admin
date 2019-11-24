from django.conf.urls import url
from django.db import IntegrityError
from django.db.models import ProtectedError
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import exception_handler as drf_exception_handler

from river_admin.views.error_code import CAN_NOT_DELETE_DUE_TO_PROTECTION, DUPLICATE_ITEM

urls = []


def _path(path, method, **options):
    def decorator(view):
        authentications = options.get("authentication_classes", [TokenAuthentication])
        renderers = options.get("renderer_classes", [JSONRenderer])
        new_view = api_view([method])(authentication_classes(authentications)(renderer_classes(renderers)(view)))
        urls.append(url(path, new_view))
        return new_view

    return decorator


def get(path, **options):
    return _path(path, "GET", **options)


def post(path, **options):
    return _path(path, "POST", **options)


def put(path, **options):
    return _path(path, "PUT", **options)


def delete(path, **options):
    return _path(path, "DELETE", **options)


def exception_handler(exc, context):
    handled_exception = drf_exception_handler(exc, context)
    if handled_exception:
        return handled_exception

    errors = []
    if isinstance(exc, ProtectedError):
        error_code = CAN_NOT_DELETE_DUE_TO_PROTECTION
        protected_errors = []
        for protected_object in exc.protected_objects:
            object_type = protected_object.__class__.__name__.lower()
            serializer_class = None
            if isinstance(protected_object, Workflow):
                serializer_class = WorkflowDto
            elif isinstance(protected_object, State):
                serializer_class = StateDto
            elif isinstance(protected_object, TransitionMeta):
                serializer_class = TransitionMetaDto
            elif isinstance(protected_object, TransitionApprovalMeta):
                serializer_class = TransitionApprovalMetaDto
            elif isinstance(protected_object, Transition):
                serializer_class = None
            elif isinstance(protected_object, TransitionApproval):
                serializer_class = None
            elif isinstance(protected_object, OnTransitHook):
                serializer_class = TransitionHookDto
            elif isinstance(protected_object, OnApprovedHook):
                serializer_class = ApprovalHookDto

            if serializer_class:
                protected_errors.append({"object_type": object_type, "object": serializer_class(protected_object).data})

        if protected_errors:
            errors.append({"error_code": error_code, "detail": {"protected_errors": protected_errors}})

    elif isinstance(exc, IntegrityError):
        errors.append({"error_code": DUPLICATE_ITEM, "detail": {"duplicates": exc.args}})

    if errors:
        return Response(ErrorResponse(errors, many=True).data, status=HTTP_400_BAD_REQUEST)
    else:
        return None


class ErrorResponse(serializers.Serializer):
    error_code = serializers.IntegerField()
    detail = serializers.DictField()


from .auth_view import *
from .state_view import *
from .workflow_view import *
from .transition_meta_view import *
from .transition_approval_meta_view import *
from .function_view import *
from .transition_hook_view import *
from .approval_hook_view import *
from .transition_view import *
from .transition_approval_view import *
from .workflow_object_view import *


@get(r'^river-admin/$', authentication_classes=[], renderer_classes=[TemplateHTMLRenderer])
def index(request):
    return Response({}, template_name="index.html")
