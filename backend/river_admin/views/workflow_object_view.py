from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from river.models import Workflow, DONE

from river_admin.views import get, delete
from river_admin.views.serializers import StateDto, WorkflowObjectStateDto, TransitionDto, TransitionApprovalDto


@get(r'^workflow-object/identify/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_identifier(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)
    return Response(str(workflow_object), status=status.HTTP_200_OK)


@get(r'^workflow-object/current-state/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_current_state(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    current_state = getattr(workflow_object, workflow.field_name)
    return Response(StateDto(current_state).data, status=status.HTTP_200_OK)


@get(r'^workflow-object/current-iteration/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_current_iteration(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    current_state = getattr(workflow_object, workflow.field_name)
    iterations = workflow.transitions.filter(workflow=workflow, object_id=workflow_object.pk, destination_state=current_state, status=DONE).values_list("iteration", flat=True)
    last_iteration = max(iterations) + 1 if iterations else 0
    return Response(last_iteration, status=status.HTTP_200_OK)


@delete(r'^workflow-object/delete/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_identifier(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)
    workflow_object.delete()
    return Response(status=status.HTTP_200_OK)


@get(r'^workflow-object/state/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_states(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    states = []
    processed_states = []
    for transition in workflow.transitions.filter(object_id=workflow_object.pk):
        source_iteration = transition.iteration - 1
        destination_iteration = transition.iteration

        source_state_key = str(source_iteration) + str(transition.source_state.pk)
        if source_state_key not in processed_states:
            states.append({"iteration": source_iteration, "state": transition.source_state})
            processed_states.append(source_state_key)

        destination_state_key = str(destination_iteration) + str(transition.destination_state.pk)
        if destination_state_key not in processed_states:
            states.append({"iteration": destination_iteration, "state": transition.destination_state})
            processed_states.append(destination_state_key)

    return Response(WorkflowObjectStateDto(states, many=True).data, status=HTTP_200_OK)


@get(r'^workflow-object/transition/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_transitions(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    return Response(TransitionDto(workflow.transitions.filter(object_id=workflow_object.pk), many=True).data, status=HTTP_200_OK)


@get(r'^workflow-object/transition-approval/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_transition_approvals(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    return Response(TransitionApprovalDto(workflow.transition_approvals.filter(object_id=workflow_object.pk), many=True).data, status=HTTP_200_OK)
