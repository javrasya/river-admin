from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
from river.models import State

from examples.issue_tracker_example.models import Issue
from examples.shipping_example.models import Shipping


def _approve(user, model_class, field_name, pk, return_page, next_state_id=None):
    item = get_object_or_404(model_class.objects.all(), pk=pk)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        getattr(item.river, field_name).approve(as_user=user, next_state=next_state)
        return redirect(reverse(return_page))
    except Exception as e:
        return HttpResponse(e.message)


@login_required()
def approve_issue(request, issue_id, next_state_id=None):
    return _approve(request.user, Issue, "issue_status", issue_id, 'admin:issue_tracker_example_issue_changelist', next_state_id=next_state_id)


@login_required()
def approve_shipping(request, shipping_id, next_state_id=None):
    return _approve(request.user, Shipping, "shipping_status", shipping_id, 'admin:shipping_example_shipping_changelist', next_state_id=next_state_id)
