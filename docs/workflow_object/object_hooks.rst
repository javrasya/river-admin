.. _`Object Hooks`:

.. |Workflow and Object Hooks Together| image:: /_static/images/workflow-and-object-hooks-together.png
    :width: 80%

.. |Create Object Transition Hook - Step 1| image:: /_static/images/create-object-transition-hook-1.png
    :width: 80%

.. |Create Object Transition Hook - Step 2| image:: /_static/images/create-object-transition-hook-2.png
    :width: 80%

.. |Create Object Transition Hook - Step 3| image:: /_static/images/create-object-transition-hook-3.png
    :width: 80%

.. |Object Transition Hook Created| image:: /_static/images/object-transition-hook-created.png
    :width: 80%

.. |Create Object Approval Hook - Step 1| image:: /_static/images/create-object-approval-hook-1.png
    :width: 80%

.. |Create Object Approval Hook - Step 2| image:: /_static/images/create-object-approval-hook-2.png
    :width: 80%

.. |Create Object Approval Hook - Step 3| image:: /_static/images/create-object-approval-hook-3.png
    :width: 80%

.. |Object Approval Hook Created| image:: /_static/images/object-approval-hook-created.png
    :width: 80%

Object Hooks
============

.. note::
    What hooking is described in workflow level :ref:`Hooks`. So please
    visit there to get the idea of the hooks.

Object level hooking is tied to a specific object unlike workflow
level hookings. It means the the hooks that you created for an object
won't be kicked in for the other objects that are same kind.

On the timeline page, those you created at the workflow level will
be shown with ``aliceblue`` color and without a delete button since it is
a general hook for all objects in the workflow. But you will see
object level hooks with white color and a delete button as shown below;

.. rst-class:: center

|Workflow and Object Hooks Together|

Create Transition Hooks
-----------------------

.. rst-class:: center

|Create Object Transition Hook - Step 1|
|Create Object Transition Hook - Step 2|
|Create Object Transition Hook - Step 3|

After you create, it should look like this;

.. rst-class:: center

|Object Transition Hook Created|


Create Approval Hooks
---------------------

.. rst-class:: center

|Create Object Approval Hook - Step 1|
|Create Object Approval Hook - Step 2|
|Create Object Approval Hook - Step 3|

After you create, it should look like this;

.. rst-class:: center

|Object Approval Hook Created|
