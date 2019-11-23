.. _authorizations:

.. |Edit Workflow Rules From Home| image:: /_static/images/go-to-workflow-authorization.png
    :width: 50%

.. |Edit Workflow Rules From Editing| image:: /_static/images/edit-workflow-page-button-on-editing.png

.. |Select Transition - Step 1| image:: /_static/images/left-click-on-transition.png

.. |Create Approval - Step 2| image:: /_static/images/create-approval-1.png
    :width: 80%

.. |Create Approval - Step 3| image:: /_static/images/user-group-not-selected-yet.png
    :width: 80%

.. |Create Approval - Step 4| image:: /_static/images/user-group-selected.png
    :width: 80%

.. |Approval Created| image:: /_static/images/an-approval-is-created.png

.. |Create Approval With Multiple Group| image:: /_static/images/create-authorization-rule-with-multiple-groups.png
    :width: 80%

.. |Delete Authorization Rule| image:: /_static/images/delete-authorization-rule.png
    :width: 80%

.. |Approval With Multiple Group Created| image:: /_static/images/authorization-rule-with-multiple-groups.png

.. |Chain of Authorization Rule| image:: /_static/images/chain-of-authorization-rule.png

.. |Start Reprioritization| image:: /_static/images/repritoritization-1.png
    :width: 80%

.. |Reprioritizating| image:: /_static/images/repritoritization-2.png
    :width: 80%


Authorizations
==============

Thanks to ``django-river`` because it supports flexibility to manage
workflow components on the fly meaning that the changes can be applied
without a code change or a deployment. ``River Admin`` is extending this
capability and providing a user friendly, easy to use screens to do that on top
of ``django-river``. One of these screens is managing the authorization
rules of the transitions.

.. _how to naivagate authorizations:

How to Navigate
---------------

.. note::
    In order to see this page, your user has to have ``river.view_workflow``
    together with ``river.change_workflow`` permissions.

In order to go to that screen you can either be navigated from the home screen
by clicking the "Edit Workflow Rules" button;

.. rst-class:: center

|Edit Workflow Rules From Home|


Or from the editing workflow page by clicking "Edit Workflow Rules"
button;

|Edit Workflow Rules From Editing|

Add Authorization Rule
----------------------

``River Admin`` provides a graphical interface that illustrates states
and transitions in the workflow which you have already seen while
creating the workflow. Same component exists here but with more capability.
That extra capability you have here is to be able to click transitions which
are illustrated with arrows between the states. Later you will see another
component on the right side of the screen where you can manage the
authorization rules for the transition.

Step 1:
|Select Transition - Step 1|


Step 2:

.. rst-class:: center

|Create Approval - Step 2|

Step 3:

.. rst-class:: center

|Create Approval - Step 3|

Step 4:

.. rst-class:: center

|Create Approval - Step 4|

After the authorization rule is created successfully;

|Approval Created|

The authorization rule we have just created means that
in order the transition to happen a user within
``Delivery Person`` user group should approve it.

Multiple Groups
~~~~~~~~~~~~~~~

Multiple user groups can also be selected in one authorization
rules as it is already supported by ``django-river`` and that
would mean that anyone who is in those groups can approve the
transition;

.. rst-class:: center

|Create Approval With Multiple Group|

|Approval With Multiple Group Created|

Delete Authorization Rule
-------------------------

.. rst-class:: center

|Delete Authorization Rule|



Chain of Authorization Rules
----------------------------

This is one of the cool feature of ``django-river`` already.
Multiple authorization rules can be chained togeter with a
prioritization mechanism. With this a first authorization rule
should be satisfied before the second one can kick in.

.. note::
    This should not be mixed up with having multiple groups
    in one authorization rule. Because with multiple groups
    anytime any user in any of the specified group is authorized
    to approve the transition.

|Chain of Authorization Rule|

What is created in the image above is a chain of authorization rules
for the transition. It means that a users within ``Delivery Person``
group should first approve it before it is on the user's approval who
are in the ``Delivery Manager`` group.


.. note::
    The prioritization order matters here.

Reprioritizition
~~~~~~~~~~~~~~~~

One of the most convinient improvement with ``River Admin`` on top of
``django-river`` is changing the order of the chain by just a drag
and drop.

.. rst-class:: center

|Start Reprioritization|
|Reprioritizating|
