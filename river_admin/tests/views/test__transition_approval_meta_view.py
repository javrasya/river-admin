import json

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, has_property, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import State, Workflow, TransitionMeta, TransitionApprovalMeta, OnApprovedHook, Function


class TransitionApprovalMetaViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentTransitionApprovalMetaIsRequested(self):
        response = self.client.get('/transition-approval-meta/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnTransitionApprovalMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        response = self.client.get('/transition-approval-meta/get/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(transition_approval_meta.id)))
        assert_that(response.data, has_entry("workflow", equal_to(workflow.id)))
        assert_that(response.data, has_entry("transition_meta", equal_to(transition_meta.id)))
        assert_that(response.data, has_entry("priority", equal_to(transition_approval_meta.priority)))
        assert_that(response.data, has_entry("permissions", has_length(0)))
        assert_that(response.data, has_entry("groups", has_length(0)))

    def test__shouldReturnEmptyListWhenThereIsNoTransitionApprovalMeta(self):
        response = self.client.get('/transition-approval-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfTransitionApprovalMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")
        state_3 = State.objects.create(label="state-3")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta_1 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        transition_meta_2 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3)

        transition_approval_meta_1 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta_1, priority=0)
        transition_approval_meta_2 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta_2, priority=0)

        response = self.client.get('/transition-approval-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_approval_meta_1.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("transition_meta", equal_to(transition_meta_1.id)),
                    has_entry("priority", equal_to(transition_approval_meta_1.priority)),
                    has_entry("permissions", has_length(0)),
                    has_entry("groups", has_length(0))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_approval_meta_2.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("transition_meta", equal_to(transition_meta_2.id)),
                    has_entry("priority", equal_to(transition_approval_meta_2.priority)),
                    has_entry("permissions", has_length(0)),
                    has_entry("groups", has_length(0))
                )
            )
        )

    def test__shouldNotCreateTransitionApprovalMetaWhenWorkflowIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        response = self.client.post('/transition-approval-meta/create/', data={"transition_meta": transition_meta.id, "permissions": [], "groups": [], "priority": 0})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateTransitionApprovalMetaWhenTransitionMetaIsMissing(self):
        initial_state = State.objects.create(label="state-1")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "permissions": [], "groups": [], "priority": 0})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateTransitionApprovalMetaEvenPriorityIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "transition_meta": transition_meta.id, "permissions": [], "groups": []})
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_transition_approval_meta = TransitionApprovalMeta.objects.first()
        assert_that(response.data, has_entry("id", equal_to(created_transition_approval_meta.pk)))
        assert_that(created_transition_approval_meta, has_property("priority", equal_to(0)))

    def test__shouldCreateTransitionApprovalMetaWithGivenPriority(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "transition_meta": transition_meta.id, "permissions": [], "groups": [], "priority": 5})
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_transition_approval_meta = TransitionApprovalMeta.objects.first()
        assert_that(response.data, has_entry("id", equal_to(created_transition_approval_meta.pk)))
        assert_that(created_transition_approval_meta, has_property("priority", equal_to(5)))

    def test__shouldReturnNotFoundWhenAnInexistentTransitionApprovalMetaIsRequestedToDelete(self):
        response = self.client.delete('/transition-approval-meta/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteTransitionApprovalMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        response = self.client.delete('/transition-approval-meta/delete/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(TransitionApprovalMeta.objects.filter(id=transition_approval_meta.id).first(), is_(none()))

    def test__shouldRePrioritizeTransitionApprovalMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta_1 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        transition_approval_meta_2 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=2)
        response = self.client.post('/transition-approval-meta/re-prioritize/', json.dumps([
            {"transition_approval_meta_id": transition_approval_meta_1.id, "priority": 50},
            {"transition_approval_meta_id": transition_approval_meta_2.id, "priority": 40}
        ]), content_type='application/json')

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_1.pk), has_property("priority", equal_to(50)))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_2.pk), has_property("priority", equal_to(40)))

    def test__shouldReturnEmptyListWhenThereIsNoApprovalHooks(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)

        response = self.client.get('/transition-approval-meta/approval-hook/list/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfApprovalHooks(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function_1 = Function.objects.create(name="test-function-1", body="function-body")
        function_2 = Function.objects.create(name="test-function-2", body="function-body")

        approval_hook_1 = OnApprovedHook.objects.create(workflow=workflow, callback_function=function_1, transition_approval_meta=transition_approval_meta)
        approval_hook_2 = OnApprovedHook.objects.create(workflow=workflow, callback_function=function_2, transition_approval_meta=transition_approval_meta)

        response = self.client.get('/transition-approval-meta/approval-hook/list/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(approval_hook_1.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_1.id)),
                        has_entry("name", equal_to(function_1.name)),
                        has_entry("body", equal_to(function_1.body))
                    )),
                    has_entry("transition_approval_meta", equal_to(transition_approval_meta.id)),
                    has_entry("transition_approval", none()),
                    has_entry("object_id", none()),
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(approval_hook_2.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_2.id)),
                        has_entry("name", equal_to(function_2.name)),
                        has_entry("body", equal_to(function_2.body))
                    )),
                    has_entry("transition_approval_meta", equal_to(transition_approval_meta.id)),
                    has_entry("transition_approval", none()),
                    has_entry("object_id", none()),
                )
            )
        )
