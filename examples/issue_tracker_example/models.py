
#Custom user model support replacement
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import models
from django.db.models import SET_NULL
from river.models.fields.state import StateField


class Issue(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField(max_length=200, null=True, blank=True)
    reporter = models.ForeignKey(User, related_name="reported_issues", null=True, blank=True, on_delete=SET_NULL)
    assignee = models.ForeignKey(User, related_name="assigned_issues", null=True, blank=True, on_delete=SET_NULL)
    issue_status = StateField()

    def __str__(self):
        return self.title
