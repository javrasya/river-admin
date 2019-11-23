.. _hooks:

.. |Create Transition Hook - Step 1| image:: /_static/images/create-transition-hook-1.png
    :width: 80%

.. |Create Transition Hook - Step 2| image:: /_static/images/create-transition-hook-2.png
    :width: 80%

.. |Create Transition Hook - Step 3| image:: /_static/images/create-transition-hook-3.png
    :width: 80%

.. |Transition Hook Created| image:: /_static/images/transition-hook-created.png
    :width: 80%

.. |Create Approval Hook - Step 1| image:: /_static/images/create-approval-hook-1.png
    :width: 80%

.. |Create Approval Hook - Step 2| image:: /_static/images/create-approval-hook-2.png
    :width: 80%

.. |Create Approval Hook - Step 3| image:: /_static/images/create-approval-hook-3.png
    :width: 80%

.. |Approval Hook Created| image:: /_static/images/approval-hook-created.png
    :width: 80%

Hooks
=====

``Hooks`` are the workflow component for you to
subscribe certain events in your workflow like
a transition happens, an auhorization rule is approved
or the workflow is completed. It can be either a rule
in general for whole workflow or for a specific workflow
object too. In this section, we will be looking into the
first one

After ``django-river`` version ``3.0.0``, hooks
are supported on the fly and this is another
feature of ``django-river`` which ``River Admin``
has some interfaces for.

Hooks are managed on the same page with authorizations
for a workflow. So, to know how to navigate to the page,
please take a look at :ref:`how to naivagate authorizations`

.. note::
    To register a hook to a certain event, you need the required
    function to be defined preliminary. To see how to create a
    function please look at :ref:`Create or Update Function`

.. note::
    Even though ``django-river`` supports transition, approvals
    and workflow completing events to hook up, ``River Admin``
    currently supports only transitions and approval hooks.

    Apart from that even tough ``django-river`` gives you the capability of
    defining your hooks before the event happens or after the
    event happens, ``River Admin`` simplifies this by just
    allowing ``before transition happens`` and
    ``after an authorization rule is approved`` for the sake of
    convinience. By this it is very smooth to create your workflow
    along with your hooks all together.

Create Transition Hooks
-----------------------

Transition hooks can be defined for whole transition. It means that
the hook will be executed right before the transition happens.

.. rst-class:: center

|Create Transition Hook - Step 1|
|Create Transition Hook - Step 2|
|Create Transition Hook - Step 3|

After you create, it should look like this;

.. rst-class:: center

|Transition Hook Created|

Create Approval Hooks
---------------------

Approval hooks can be defined for a specific authorization rule
not for whole transition. After the authorization rule is approved
your hook will be invoked.


.. rst-class:: center

|Create Approval Hook - Step 1|
|Create Approval Hook - Step 2|
|Create Approval Hook - Step 3|

After you create, it should look like this;

.. rst-class:: center

|Approval Hook Created|
