from django.contrib import admin

import river_admin
from river_admin_issue_tracker_example.models import Issue


class IssueRiverAdmin(river_admin.RiverAdmin):
    name = "Issue Tracking Flow"
    icon = "mdi-ticket-account"
    list_displays = ['pk', 'title', 'reporter', 'assignee', 'issue_status']


river_admin.site.register(Issue, "issue_status", IssueRiverAdmin)


class IssueAdmin(admin.ModelAdmin):
    readonly_fields = ('issue_status',)


admin.site.register(Issue, IssueAdmin)
