from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, not_none, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from river.models import State, Workflow, TransitionMeta, Transition

from river_admin.views import ContentType


class WorkflowViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentWorkflowIsRequested(self):
        response = self.client.get('/workflow/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.get('/workflow/get/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(workflow.id)))
        assert_that(response.data, has_entry("field_name", equal_to(workflow.field_name)))
        assert_that(
            response.data,
            all_of(
                has_entry("id", workflow.id),
                has_entry("field_name", workflow.field_name),
                has_entry(
                    "initial_state",
                    all_of(
                        has_entry("id", equal_to(initial_state.id)),
                        has_entry("label", equal_to(initial_state.label)),
                        has_entry("slug", equal_to(initial_state.slug))
                    )
                ),
                has_entry(
                    "content_type",
                    all_of(
                        has_entry("id", equal_to(content_type.id)),
                        has_entry("app_label", equal_to(content_type.app_label)),
                        has_entry("model", equal_to(content_type.model)),
                    )
                )
            )
        )

    def test__shouldReturnEmptyListWhenThereIsNoWorkflows(self):
        response = self.client.get('/workflow/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfWorkflows(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow_1 = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field-1")
        workflow_2 = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field-2")

        response = self.client.get('/workflow/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", workflow_1.id),
                    has_entry("field_name", workflow_1.field_name),
                    has_entry(
                        "initial_state",
                        all_of(
                            has_entry("id", equal_to(initial_state.id)),
                            has_entry("label", equal_to(initial_state.label)),
                            has_entry("slug", equal_to(initial_state.slug))
                        )
                    ),
                    has_entry(
                        "content_type",
                        all_of(
                            has_entry("id", equal_to(content_type.id)),
                            has_entry("app_label", equal_to(content_type.app_label)),
                            has_entry("model", equal_to(content_type.model)),
                        )
                    )
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", workflow_2.id),
                    has_entry("field_name", workflow_2.field_name),
                    has_entry(
                        "initial_state",
                        all_of(
                            has_entry("id", equal_to(initial_state.id)),
                            has_entry("label", equal_to(initial_state.label)),
                            has_entry("slug", equal_to(initial_state.slug))
                        )
                    ),
                    has_entry(
                        "content_type",
                        all_of(
                            has_entry("id", equal_to(content_type.id)),
                            has_entry("app_label", equal_to(content_type.app_label)),
                            has_entry("model", equal_to(content_type.model)),
                        )
                    )
                )
            )
        )

    def test__shouldNotCreateWorkflowWhenFieldNameIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        response = self.client.post('/workflow/create/', data={"initial_state": initial_state.id, "content_type": content_type.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateWorkflowWhenFieldContentTypeIsMissing(self):
        initial_state = State.objects.create(label="state-1")
        response = self.client.post('/workflow/create/', data={"initial_state": initial_state.id, "field_name": "test-field"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateWorkflowWhenInitialStateIsMissing(self):
        content_type = ContentType.objects.first()
        response = self.client.post('/workflow/create/', data={"field_name": "test-field", "content_type": content_type.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateWorkflowWhenInitialStateIsInvalid(self):
        content_type = ContentType.objects.first()
        response = self.client.post('/workflow/create/', data={"initial_state": 1, "field_name": "test-field", "content_type": content_type.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateWorkflowWhenContentTypeIsInvalid(self):
        initial_state = State.objects.create(label="state-1")
        response = self.client.post('/workflow/create/', data={"initial_state": initial_state.id, "field_name": "test-field", "content_type": -1})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        response = self.client.post('/workflow/create/', data={"initial_state": initial_state.id, "field_name": "test-field", "content_type": content_type.id})
        created_workflow = Workflow.objects.first()
        assert_that(created_workflow, not_none())
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(created_workflow.pk)))

    def test__shouldNotCreateWorkflowWhenFieldNameAndContentTypeIsDuplicate(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.post('/workflow/create/', data={"initial_state": initial_state.id, "field_name": workflow.field_name, "content_type": workflow.content_type.id})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldReturnNotFoundWhenAnInexistentWorkflowIsRequestedToDelete(self):
        response = self.client.delete('/workflow/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.delete('/workflow/delete/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(Workflow.objects.filter(field_name=workflow.field_name).first(), is_(none()))

    def test__shouldReturnEmptyListOfStateFieldsWhenThereIsNoModelWithStateField(self):
        response = self.client.get('/workflow/state-field/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfStateFieldsWhenThereIsModelWithStateField(self):
        content_type = ContentType.objects.first()

        from river.core.workflowregistry import workflow_registry
        workflow_registry.add("test-field-1", content_type.model_class())
        workflow_registry.add("test-field-2", content_type.model_class())

        response = self.client.get('/workflow/state-field/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("field_name", equal_to("test-field-1")),
                    has_entry(
                        "content_type",
                        all_of(
                            has_entry("id", equal_to(content_type.id)),
                            has_entry("app_label", equal_to(content_type.app_label)),
                            has_entry("model", equal_to(content_type.model)),
                        )
                    )
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("field_name", equal_to("test-field-2")),
                    has_entry(
                        "content_type",
                        all_of(
                            has_entry("id", equal_to(content_type.id)),
                            has_entry("app_label", equal_to(content_type.app_label)),
                            has_entry("model", equal_to(content_type.model)),
                        )
                    )
                )
            )
        )

    def test__shouldReturnOnlyInitialStateWhenThereIsNoTransitionMetaInTheWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.get('/workflow/state/list/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(1))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(initial_state.id)),
                    has_entry("label", equal_to(initial_state.label)),
                    has_entry("slug", equal_to(initial_state.slug))
                )
            )
        )

    def test__shouldReturnStatesOfTransitionsInWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")
        state_3 = State.objects.create(label="state-3")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3)

        response = self.client.get('/workflow/state/list/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(3))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(initial_state.id)),
                    has_entry("label", equal_to(initial_state.label)),
                    has_entry("slug", equal_to(initial_state.slug))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(state_2.id)),
                    has_entry("label", equal_to(state_2.label)),
                    has_entry("slug", equal_to(state_2.slug))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(state_3.id)),
                    has_entry("label", equal_to(state_3.label)),
                    has_entry("slug", equal_to(state_3.slug))
                )
            )
        )

    def test__shouldReturnEmptyListOfTransitionMetaWhenThereIsNoTransitionMetaInTheWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.get('/workflow/transition-meta/list/%d/' % workflow.id)
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

        response = self.client.get('/workflow/transition-meta/list/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_meta_1.id)),
                    has_entry("source_state", equal_to(transition_meta_1.source_state.id)),
                    has_entry("destination_state", equal_to(transition_meta_1.destination_state.id))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_meta_2.id)),
                    has_entry("source_state", equal_to(transition_meta_2.source_state.id)),
                    has_entry("destination_state", equal_to(transition_meta_2.destination_state.id))
                )
            )
        )

    def test__shouldReturnEmptyListOfTransitionWhenThereIsNoTransitionInTheWorkflow(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.get('/workflow/transition/list/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfTransition(self):
        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")
        state_3 = State.objects.create(label="state-3")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta_1 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        transition_meta_2 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3)

        transition_1 = Transition.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2, meta=transition_meta_1, object_id=1, content_type=content_type, iteration=0)
        transition_2 = Transition.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3, meta=transition_meta_2, object_id=1, content_type=content_type, iteration=0)

        response = self.client.get('/workflow/transition/list/%d/' % workflow.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_1.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("source_state", equal_to(transition_1.source_state.id)),
                    has_entry("destination_state", equal_to(transition_1.destination_state.id)),
                    has_entry("meta", equal_to(transition_meta_1.id)),
                    has_entry("iteration", equal_to(transition_1.iteration)),
                    has_entry("object_id", equal_to("1")),
                    has_entry("is_done", equal_to(False)),
                    has_entry("is_cancelled", equal_to(False)),
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_2.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("source_state", equal_to(transition_2.source_state.id)),
                    has_entry("destination_state", equal_to(transition_2.destination_state.id)),
                    has_entry("meta", equal_to(transition_meta_2.id)),
                    has_entry("iteration", equal_to(transition_2.iteration)),
                    has_entry("object_id", equal_to("1")),
                    has_entry("is_done", equal_to(False)),
                    has_entry("is_cancelled", equal_to(False)),
                )
            )
        )

    def test__shouldReturnListOfDefaultWorkflowMetadataIfItIsNotCustomized(self):
        initial_state = State.objects.create(label="state-1")
        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")

        response = self.client.get('/workflow/metadata/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(1))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(str(workflow.id))),
                    has_entry("icon", "mdi-sitemap"),
                    has_entry("name", equal_to("%s (test-field)" % content_type.model_class().__name__)),
                )
            )
        )
