.. _create-workflow:

.. |Select Workflow Img| image:: /_static/images/select-workflow.png

.. |Select Initial State Img| image:: /_static/images/select-initial-state.png

.. |Home Without Workflow Img| image:: /_static/images/home-without-workflow.png

.. |Initial State Is Created Img| image:: /_static/images/initial-state-is-created.png

.. |Searching Second State Img| image:: /_static/images/searching-second-state.png

.. |Scond Second Is Created Img| image:: /_static/images/second-state-is-created.png


Create a Workflow
=================

.. note::
    Before you can set up your workflow, your app integration
    with ``django-river`` must be done. Don't worry it
    is with the easiest setup.To see how to do it with
    ``django-river`` pleas have a look at `django-river`

Creating a workflow consist of defining its intiial state
and the state field along with the content type and later
on the transitons buy just clicking.


Initiale Worklfow
-----------------

* if you haven't had any worklow before, ``Home`` page will wellcome you with a button which will take yo to the workflow creation page. If you have had a workflow before then just click the plus button on the right bottom corner to navigate to the page.

|Home Without Workflow Img|


* Pick the workflow that you have had the integration with ``django-river``

|Select Workflow Img|

* Pick the initial state of your workflow and lastly hit the create button

|Select Initial State Img|


Create Transitions
------------------

This is the most fun part of ``River Admin``. Becuase
it provides a highly interactive one screen to create them all.

.. note::
    Every change you make on that screen is an online action. Meaning that it will also be applied on the DB.

.. note::
    Same screen can anytime be used to update the
    transitions in the workflow as well

* What you are going to run into after you have done the previous steps is something like this;

|Initial State Is Created Img|

* This interface expects you to click the rectangles which are representing the transition states to create next state out of them. Simply click them and that will change their color so that you can understand you managed to select

|Searching Second State Img|


|Scond Second Is Created Img|
