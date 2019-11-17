import logging

from django.apps import AppConfig

LOGGER = logging.getLogger(__name__)

OPEN = "Initialized"
IN_PROGRESS = "Shipped"
RESOLVED = "Arrived"
RE_OPENED = "Return Initialized"
CLOSED = "Closed"


class RiverAdminIssueTrackerExampleApp(AppConfig):
    name = 'river_admin_issue_tracker_example'
    label = 'river_admin_issue_tracker_example'

    def ready(self):
        from river.models import State, Workflow, TransitionMeta
        from django.contrib.contenttypes.models import ContentType

        issue_class = self.get_model('Issue')
        issue_content_type = ContentType.objects.get_for_model(issue_class)

        open_state, _ = State.objects.get_or_create(label=OPEN)
        in_progress_state, _ = State.objects.get_or_create(label=IN_PROGRESS)
        resolved_state, _ = State.objects.get_or_create(label=RESOLVED)
        re_opened_state, _ = State.objects.get_or_create(label=RE_OPENED)
        closed_state, _ = State.objects.get_or_create(label=CLOSED)

        workflow, _ = Workflow.objects.get_or_create(content_type=issue_content_type, initial_state=open_state, field_name="issue_status")

        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=open_state, destination_state=in_progress_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=in_progress_state, destination_state=resolved_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=resolved_state, destination_state=closed_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=resolved_state, destination_state=re_opened_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=re_opened_state, destination_state=in_progress_state)
