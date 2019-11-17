import logging

from django.apps import AppConfig

LOGGER = logging.getLogger(__name__)

INITIALIZED = "Initialized"
SHIPPED = "Shipped"
ARRIVED = "Arrived"
RETURN_INITIALIZED = "Return Initialized"
RETURNED = "Returned"
RE_INITIALIZED = "Re-Initialized"
REFUNDED = "Refunded"
CLOSED = "Closed"


class RiverAdminShippingExampleApp(AppConfig):
    name = 'river_admin_shipping_example'
    label = 'river_admin_shipping_example'

    def ready(self):
        from river.models import State, Workflow, TransitionMeta
        from django.contrib.contenttypes.models import ContentType

        shipping_class = self.get_model('Shipping')
        shipping_content_type = ContentType.objects.get_for_model(shipping_class)

        initialized_state, _ = State.objects.get_or_create(label=INITIALIZED)
        shipped_state, _ = State.objects.get_or_create(label=SHIPPED)
        arrived_state, _ = State.objects.get_or_create(label=ARRIVED)
        return_initialized_state, _ = State.objects.get_or_create(label=RETURN_INITIALIZED)
        returned_state, _ = State.objects.get_or_create(label=RETURNED)
        re_initialized_state, _ = State.objects.get_or_create(label=RE_INITIALIZED)
        refunded_state, _ = State.objects.get_or_create(label=REFUNDED)
        closed_state, _ = State.objects.get_or_create(label=CLOSED)

        workflow, _ = Workflow.objects.get_or_create(content_type=shipping_content_type, field_name="shipping_status", defaults={"initial_state": initialized_state})

        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=initialized_state, destination_state=shipped_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=shipped_state, destination_state=arrived_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=arrived_state, destination_state=closed_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=arrived_state, destination_state=return_initialized_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=return_initialized_state, destination_state=returned_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=returned_state, destination_state=re_initialized_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=returned_state, destination_state=refunded_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=refunded_state, destination_state=closed_state)
        TransitionMeta.objects.get_or_create(workflow=workflow, source_state=re_initialized_state, destination_state=shipped_state)
