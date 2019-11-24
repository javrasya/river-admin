.. _Timeline:

.. |Workflow Object List Img| image:: /_static/images/list-workflow-objects.png

.. |Initialized| image:: /_static/images/initialized.png

.. |Shipped| image:: /_static/images/shipped.png

.. |Arrived 1| image:: /_static/images/arrived-1.png

.. |Arrived 2| image:: /_static/images/arrived-2.png

.. |Closed| image:: /_static/images/closed.png

.. |Blue State| image:: /_static/images/blue-state.png
    :width: 10%

.. |Green State| image:: /_static/images/green-state.png
    :width: 10%

.. |Grey State| image:: /_static/images/grey-state.png
    :width: 10%

.. |White State With Dashed Border| image:: /_static/images/white-state-with-dashed-border.png
    :width: 10%

Timeline
========

Each workflow object in ``django-river`` has a different
instance of the the same lifecycle. The transitions,
authorization rules and hooks are created out of the workflow
specification once and special to the workflow object itself.

``River Admin`` is showing the timeline of one workflow object
that is consist of states, transitions, authorizations and hooks
that scattered around in one useful user interface. On this page
you can see what has happened so far along with what will possibly
happen with the object. You can even add a transition and approval
hooks tied to a particular object that is not for whole workflow
object.


Here you can see an example of whole lifecycle of a workflow object;


Current State: Initialized
|Initialized|


Current State: Shipped
|Shipped|

Current State: Arrived Approved but still Shipped
|Arrived 1|

Current State: Arrived
|Arrived 2|

Current State: Closed
|Closed|

Colors
~~~~~~

There are different type of indicator colors for different
states like ``current state`` (Blue), ``approved state`` (Green),
``possible state`` (White with dashed border) or ``impossible state`` (Grey).

.. rst-class:: center

|Green State|
|Blue State|
|White State With Dashed Border|
|Grey State|

