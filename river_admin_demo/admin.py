from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from river_admin_issue_tracker_example.admin import IssueAdmin
from river_admin_issue_tracker_example.models import Issue
from river_admin_shipping_example.admin import ShippingAdmin
from river_admin_shipping_example.models import Shipping


def create_river_button(obj, transition_approval):
    approve_ticket_url = reverse('approve_ticket', kwargs={'ticket_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return f"""
        <input
            type="button"
            style="margin:2px;2px;2px;2px;"
            value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
            onclick="location.href=\'{approve_ticket_url}\'"
        />
    """


class CustomIssueAdmin(IssueAdmin):
    def get_list_display(self, request):
        self.user = request.user
        return super(CustomIssueAdmin, self).get_list_display(request) + ("river_actions",)

    def river_actions(self, obj):
        content = ""
        for transition_approval in obj.river.issue_status.get_available_approvals(as_user=self.user):
            content += create_river_button(obj, transition_approval)

        return mark_safe(content)


class CustomShippingAdmin(ShippingAdmin):
    def get_list_display(self, request):
        self.user = request.user
        return super(CustomShippingAdmin, self).get_list_display(request) + ("river_actions",)

    def river_actions(self, obj):
        content = ""
        for transition_approval in obj.river.shipping_status.get_available_approvals(as_user=self.user):
            content += create_river_button(obj, transition_approval)

        return mark_safe(content)


admin.site.unregister(Issue)
admin.site.unregister(Shipping)
admin.site.register(Issue, CustomIssueAdmin)
admin.site.register(Shipping, CustomShippingAdmin)
