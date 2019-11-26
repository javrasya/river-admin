from django.contrib import admin

import river_admin
from examples.issue_tracker_example.models import Issue


class IssueRiverAdmin(river_admin.RiverAdmin):
    name = "Issue Tracking Flow"
    icon = "mdi-ticket-account"
    list_displays = ['pk', 'title', 'reporter', 'assignee', 'issue_status']


river_admin.site.register(Issue, "issue_status", IssueRiverAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'reporter', 'assignee', 'issue_status',)
    readonly_fields = ('issue_status',)


admin.site.register(Issue, IssueAdmin)
