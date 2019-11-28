from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from river.models import TransitionApprovalMeta

from examples.shipping_example.models import Shipping

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
        courier_company_attendant, _ = Group.objects.update_or_create(name="Courier Company Attendant")
        finance_manager, _ = Group.objects.update_or_create(name="Finance Person")

        shipping_content_type = ContentType.objects.get_for_model(Shipping)

        initialized_state, _ = State.objects.update_or_create(label=INITIALIZED, defaults={"description": "First step of the workflow"})
        shipped_state, _ = State.objects.update_or_create(label=SHIPPED, defaults={"description": "When the goods are physically shipped and it is confirmed by the courier company"})
        arrived_state, _ = State.objects.update_or_create(label=ARRIVED, defaults={"description": "The goods are arrived on the customer end"})
        return_initialized_state, _ = State.objects.update_or_create(label=RETURN_INITIALIZED, defaults={"description": "The customer wanted to return the goods and initialized the return at the courier company office"})
        returned_state, _ = State.objects.update_or_create(label=RETURNED, defaults={"description": "The returned goods have been arrived on the warehouse"})
        re_initialized_state, _ = State.objects.update_or_create(label=RE_INITIALIZED, defaults={"description": "There was a mistake with the shipment and the it corrected and re-initialized"})
        refunded_state, _ = State.objects.update_or_create(label=REFUNDED, defaults={"description": "The purchase has been refunded"})
        closed_state, _ = State.objects.update_or_create(label=CLOSED, defaults={"description": "The final step of the workflow"})

        workflow = Shipping.river.shipping_status.workflow \
                   or Workflow.objects.create(content_type=shipping_content_type, field_name="shipping_status", initial_state=initialized_state)

        workflow.transition_approvals.all().delete()
        workflow.transitions.all().delete()
        workflow.transition_approval_metas.all().delete()
        workflow.transition_metas.all().delete()

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
        initialized_to_shipped_rule_2.groups.set([courier_company_attendant])

        shipped_to_arrived_rule_1, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=shipped_to_arrived, priority=0)
        shipped_to_arrived_rule_1.groups.set([delivery_person])

        shipped_to_arrived_rule_2, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=shipped_to_arrived, priority=1)
        shipped_to_arrived_rule_2.groups.set([courier_company_attendant])

        arrived_to_closed_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=arrived_to_closed, priority=0)
        arrived_to_closed_rule.groups.set([finance_manager])

        arrived_to_return_initialized_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=arrived_to_return_initialized, priority=0)
        arrived_to_return_initialized_rule.groups.set([courier_company_attendant])

        return_initialized_to_returned_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=return_initialized_to_returned, priority=0)
        return_initialized_to_returned_rule.groups.set([warehouse_attendant])

        returned_to_re_initialized_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=returned_to_re_initialized, priority=0)
        returned_to_re_initialized_rule.groups.set([warehouse_attendant])

        re_initialized_to_shipped_rule_1, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=re_initialized_to_shipped, priority=0)
        re_initialized_to_shipped_rule_1.groups.set([warehouse_attendant])

        re_initialized_to_shipped_rule_2, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=re_initialized_to_shipped, priority=1)
        re_initialized_to_shipped_rule_2.groups.set([courier_company_attendant])

        returned_to_refunded_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=returned_to_refunded, priority=0)
        returned_to_refunded_rule.groups.set([finance_manager])

        refunded_to_closed_rule, _ = TransitionApprovalMeta.objects.get_or_create(workflow=workflow, transition_meta=refunded_to_closed, priority=0)
        refunded_to_closed_rule.groups.set([finance_manager])

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
