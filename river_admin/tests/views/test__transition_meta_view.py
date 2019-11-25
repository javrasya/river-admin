import json

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, has_property, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from river.models import State, Workflow, TransitionMeta, TransitionApprovalMeta, OnApprovedHook, Function, OnTransitHook


class TransitionMetaViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentTransitionMetaIsRequested(self):
        response = self.client.get('/transition-meta/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnTransitionMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        response = self.client.get('/transition-meta/get/%d/' % transition_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(transition_meta.id)))
        assert_that(response.data, has_entry("workflow", equal_to(workflow.id)))
        assert_that(response.data, has_entry("source_state", equal_to(transition_meta.source_state.id)))
        assert_that(response.data, has_entry("destination_state", equal_to(transition_meta.destination_state.id)))

    def test__shouldReturnEmptyListWhenThereIsNoTransitionMeta(self):
        response = self.client.get('/transition-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfTransitionMeta(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")
        state_3 = State.objects.create(label="state-3")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta_1 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        transition_meta_2 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3)

        response = self.client.get('/transition-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_meta_1.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("source_state", equal_to(transition_meta_1.source_state.id)),
                    has_entry("destination_state", equal_to(transition_meta_1.destination_state.id)),
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_meta_2.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("source_state", equal_to(transition_meta_2.source_state.id)),
                    has_entry("destination_state", equal_to(transition_meta_2.destination_state.id)),
                )
            )
        )

    def test__shouldNotCreateTransitionMetaWhenWorkflowIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        response = self.client.post('/transition-meta/create/', data={"source_state": initial_state.id, "destination_state": state_2.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateTransitionMetaWhenSourceStateIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.post('/transition-meta/create/', data={"workflow": workflow.id, "destination_state": state_2.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateTransitionMetaWhenDestinationStateIsMissing(self):
        initial_state = State.objects.create(label="state-1")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.post('/transition-meta/create/', data={"workflow": workflow.id, "source_state": initial_state.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateTransitionMetaWithGivenPriority(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.post('/transition-meta/create/', data={"workflow": workflow.id, "source_state": initial_state.id, "destination_state": state_2.id})
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_transition_meta = TransitionMeta.objects.first()
        assert_that(response.data, has_entry("id", equal_to(created_transition_meta.pk)))
        assert_that(created_transition_meta, has_property("source_state", equal_to(initial_state)))
        assert_that(created_transition_meta, has_property("destination_state", equal_to(state_2)))

    def test__shouldReturnEmptyListWhenThereIsNoTransitionHooks(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        response = self.client.get('/transition-meta/transition-hook/list/%d/' % transition_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfApprovalHooks(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        function_1 = Function.objects.create(name="test-function-1", body="function-body")
        function_2 = Function.objects.create(name="test-function-2", body="function-body")

        transition_hook_1 = OnTransitHook.objects.create(workflow=workflow, callback_function=function_1, transition_meta=transition_meta)
        transition_hook_2 = OnTransitHook.objects.create(workflow=workflow, callback_function=function_2, transition_meta=transition_meta)

        response = self.client.get('/transition-meta/transition-hook/list/%d/' % transition_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_hook_1.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_1.id)),
                        has_entry("name", equal_to(function_1.name)),
                        has_entry("body", equal_to(function_1.body))
                    )),
                    has_entry("transition_meta", equal_to(transition_meta.id)),
                    has_entry("transition", none()),
                    has_entry("object_id", none()),
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_hook_2.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_2.id)),
                        has_entry("name", equal_to(function_2.name)),
                        has_entry("body", equal_to(function_2.body))
                    )),
                    has_entry("transition_meta", equal_to(transition_meta.id)),
                    has_entry("transition", none()),
                    has_entry("object_id", none()),
                )
            )
        )
