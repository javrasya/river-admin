from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from river.models import TransitionApprovalMeta

from river_admin_shipping_example.models import Shipping

INITIALIZED = "Initialized"
SHIPPED = "Shipped"
ARRIVED = "Arrived"
RETURN_INITIALIZED = "Return Initialized"
RETURNED = "Returned"
RE_INITIALIZED = "Re-Initialized"
REFUNDED = "Refunded"
CLOSED = "Closed"


class Command(BaseCommand):
    help = 'Bootstrapping database with necessary items'

    @transaction.atomic()
    def handle(self, *args, **options):
        from river.models import State, Workflow, TransitionMeta
        from django.contrib.contenttypes.models import ContentType

        warehouse_attendant, _ = Group.objects.update_or_create(name="Warehouse Attendant")
        delivery_person, _ = Group.objects.update_or_create(name="Delivery Person")
        courier_company, _ = Group.objects.update_or_create(name="Courier Company")
        finance_manager, _ = Group.objects.update_or_create(name="Finance Person")

        shipping_content_type = ContentType.objects.get_for_model(Shipping)

        initialized_state, _ = State.objects.get_or_create(label=INITIALIZED)
        shipped_state, _ = State.objects.get_or_create(label=SHIPPED)
        arrived_state, _ = State.objects.get_or_create(label=ARRIVED)
        return_initialized_state, _ = State.objects.get_or_create(label=RETURN_INITIALIZED)
        returned_state, _ = State.objects.get_or_create(label=RETURNED)
        re_initialized_state, _ = State.objects.get_or_create(label=RE_INITIALIZED)
        refunded_state, _ = State.objects.get_or_create(label=REFUNDED)
        closed_state, _ = State.objects.get_or_create(label=CLOSED)

        workflow, _ = Workflow.objects.get_or_create(content_type=shipping_content_type, field_name="shipping_status", defaults={"initial_state": initialized_state})

        initialized_to_shipped, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=initialized_state, destination_state=shipped_state)
        shipped_to_arrived, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=shipped_state, destination_state=arrived_state)
        arrived_to_closed, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=arrived_state, destination_state=closed_state)
        arrived_to_return_initialized, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=arrived_state, destination_state=return_initialized_state)
        return_initialized_to_returned, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=return_initialized_state, destination_state=returned_state)
        returned_to_re_initialized, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=returned_state, destination_state=re_initialized_state)
        returned_to_refunded, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=returned_state, destination_state=refunded_state)
        refunded_to_closed, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=refunded_state, destination_state=closed_state)
        re_initialized_to_shipped, _ = TransitionMeta.objects.get_or_create(workflow=workflow, source_state=re_initialized_state, destination_state=shipped_state)

        initialized_to_shipped_rule_1, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=initialized_to_shipped, priority=0)
        initialized_to_shipped_rule_1.groups.set([warehouse_attendant])

        initialized_to_shipped_rule_2, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=initialized_to_shipped, priority=1)
        initialized_to_shipped_rule_2.groups.set([courier_company])

        shipped_to_arrived_rule_1, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=shipped_to_arrived, priority=0)
        shipped_to_arrived_rule_1.groups.set([delivery_person])

        shipped_to_arrived_rule_2, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=shipped_to_arrived, priority=1)
        shipped_to_arrived_rule_2.groups.set([courier_company])

        arrived_to_closed_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=arrived_to_closed, priority=0)
        arrived_to_closed_rule.groups.set([finance_manager])

        arrived_to_return_initialized_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=arrived_to_return_initialized, priority=0)
        arrived_to_return_initialized_rule.groups.set([courier_company])

        return_initialized_to_returned_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=return_initialized_to_returned, priority=0)
        return_initialized_to_returned_rule.groups.set([warehouse_attendant])

        returned_to_re_initialized_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=returned_to_re_initialized, priority=0)
        returned_to_re_initialized_rule.groups.set([warehouse_attendant])

        re_initialized_to_shipped_rule_1, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=re_initialized_to_shipped, priority=0)
        re_initialized_to_shipped_rule_1.groups.set([warehouse_attendant])

        re_initialized_to_shipped_rule_2, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=re_initialized_to_shipped, priority=1)
        re_initialized_to_shipped_rule_2.groups.set([courier_company])

        returned_to_refunded_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=returned_to_refunded, priority=0)
        returned_to_refunded_rule.groups.set([finance_manager])

        refunded_to_closed_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=refunded_to_closed, priority=0)
        refunded_to_closed_rule.groups.set([finance_manager])

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
