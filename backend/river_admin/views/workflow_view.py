from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.core.workflowregistry import workflow_registry
from river.models import Workflow, State

import river_admin
from river_admin.views import get, post, delete, StateDto
from river_admin.views.serializers import WorkflowStateFieldDto, CreateWorkflowDto, WorkflowDto, TransitionMetaDto, TransitionApprovalMetaDto, TransitionDto, TransitionApprovalDto, WorkflowMetadataDto


@get(r'^workflow/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    workflow = get_object_or_404(Workflow.objects.all(), pk=pk)
    return Response(WorkflowDto(workflow).data, status=HTTP_200_OK)


@get(r'^workflow/list/$')
def list_it(request):
    valid_workflows = [workflow for workflow in Workflow.objects.all() if workflow.content_type.model_class()]
    return Response(WorkflowDto(valid_workflows, many=True).data, status=HTTP_200_OK)


@post(r'^workflow/create/$')
def create_it(request):
    create_workflow_request = CreateWorkflowDto(data=request.data)
    if create_workflow_request.is_valid():
        workflow = create_workflow_request.save()
        return Response({"id": workflow.id}, status=HTTP_200_OK)
    else:
        return Response(create_workflow_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^workflow/delete/(?P<pk>\w+)/$')
def delete_it(request, pk):
    workflow = get_object_or_404(Workflow.objects.all(), pk=pk)
    workflow.delete()
    return Response(status=HTTP_200_OK)


@get(r'^workflow/state-field/list/$')
def list_available_state_fields(request):
    class_by_id = lambda cid: workflow_registry.class_index[cid]
    result = []
    for class_id, field_names in workflow_registry.workflows.items():
        cls = class_by_id(class_id)
        content_type = ContentType.objects.get_for_model(cls)
        for field_name in field_names:
            if not Workflow.objects.filter(content_type=content_type, field_name=field_name).exists():
                result.append(
                    {
                        "content_type": content_type,
                        "field_name": field_name
                    })

    return Response(WorkflowStateFieldDto(result, many=True).data, status=HTTP_200_OK)


@get(r'^workflow/state/list/(?P<workflow_id>\w+)/$')
def list_states(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    state_ids = set()
    state_ids.add(workflow.initial_state.pk)
    for source_state_id, destination_state_id in workflow.transition_metas.values_list("source_state__pk", "destination_state__pk"):
        state_ids.add(source_state_id)
        state_ids.add(destination_state_id)

    return Response(StateDto(State.objects.filter(pk__in=state_ids), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/transition-meta/list/(?P<workflow_id>\w+)/$')
def list_transition_meta(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)

    return Response(TransitionMetaDto(workflow.transition_metas.all(), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/transition/list/(?P<workflow_id>\w+)/$')
def list_transitions(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    return Response(TransitionDto(workflow.transitions.all(), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/object/list/(?P<workflow_pk>\w+)/$')
def list_workflow_objects(request, workflow_pk):
    def _get_objects(model_class, headers):
        for obj in model_class.objects.all():
            yield dict({key: str(getattr(obj, key, None)) for key in headers}, **{"id": obj.pk, "__str": str(obj)})

    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    registered_admin = river_admin.site.get(model_class, workflow.field_name)
    headers = registered_admin.list_displays if registered_admin else ["pk", workflow.field_name]

    return Response({"headers": headers, "workflow_objects": list(_get_objects(model_class, headers))}, status=HTTP_200_OK)


@get(r'^workflow/metadata/$')
def get_workflow_metadata(request):
    workflows = []
    for workflow in Workflow.objects.all():
        model_class = workflow.content_type.model_class()
        if model_class:
            registered_admin = river_admin.site.get(model_class, workflow.field_name)
            default_name = "%s (%s)" % (model_class.__name__, workflow.field_name)
            workflow_name = registered_admin.name or default_name if registered_admin else default_name
            workflow_icon = registered_admin.icon or "mdi-sitemap" if registered_admin else "mdi-sitemap"
            workflows.append({"id": workflow.id, "name": workflow_name, "icon": workflow_icon})

    return Response(WorkflowMetadataDto(workflows, many=True).data, status=HTTP_200_OK)
