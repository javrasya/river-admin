from django.core.management.base import BaseCommand
from django.db import transaction

from river_admin_issue_tracker_example.models import Issue

OPEN = "Open"
IN_PROGRESS = "In Progress"
RESOLVED = "Resolved"
RE_OPENED = "Re-Opened"
CLOSED = "Closed"


class Command(BaseCommand):
    help = 'Bootstrapping database with necessary items'

    @transaction.atomic()
    def handle(self, *args, **options):
        from river.models import State, Workflow, TransitionMeta
        from django.contrib.contenttypes.models import ContentType

        issue_content_type = ContentType.objects.get_for_model(Issue)

        open_state, _ = State.objects.get_or_create(label=OPEN)
        in_progress_state, _ = State.objects.get_or_create(label=IN_PROGRESS)
        resolved_state, _ = State.objects.get_or_create(label=RESOLVED)
        re_opened_state, _ = State.objects.get_or_create(label=RE_OPENED)
        closed_state, _ = State.objects.get_or_create(label=CLOSED)

        workflow, _ = Workflow.objects.get_or_create(content_type=issue_content_type, field_name="issue_status", defaults={"initial_state": open_state})

        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=open_state, destination_state=in_progress_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=in_progress_state, destination_state=resolved_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=resolved_state, destination_state=closed_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=resolved_state, destination_state=re_opened_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=re_opened_state, destination_state=in_progress_state)

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
