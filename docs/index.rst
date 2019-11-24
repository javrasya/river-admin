.. |Timeline Img| image:: /_static/images/timeline-next.png

.. |Home Img| image:: /_static/images/home-left-panel-on.png

.. |Re-prio Img| image:: /_static/images/re-prioritization.png

.. |Workflow Edit Img| image:: /_static/images/workflow-edit.png

.. |Custom Admin| image:: /_static/images/custom-admin.png



River Admin
===========

River Admin is a very modern and shiny web application functioning
like an admin interface that provides administration for django-river_ .
It basically extends the ``django-river`` flexibility with some user
friendly and very easy to use admin interfaces.

It can either be deployed as a standalone application on top
or bundled in your application since it is yet another library
you can install via package manager.

The power of it comes from the libraries it uses on both backend and
frontend sides which are ``django-river``, ``django-rest-framework``
``Vue``, ``Vuetify``

.. rst-class:: image-slide

|Home Img|
|Workflow Edit Img|
|Re-prio Img|
|Timeline Img|
|Custom Admin|

Each will be documented in detail but here what you
can briefly have with ``River Admin`` are that;

* List your workflows
* Customize your workflow apperance like the icon, the name and list displays in the same way as Django admin
* Create your workflow
* Click some buttons to create your transitions and by doing so create your states as well, so easy huh.
* Create authorization rules for your transitions and drag and drop to re-prioritize them
* Write your python code with an editor that supports basic highlighting and update it anytime you like
* Hook your function to a specific transition
* Hook your function to a specific approval operatation
* List states and delete them
* See a specific workflow object timeline to what has happened and what will possibly happen
* Have your hooks run for a specific workflow object instead of running them for every object in the workflow.
* Your django authorizations will still be ruling here.

.. _django-river: https://github.com/javrasya/django-river/


Donations
=========

This is a fully open source project and it can be better with your donations.

If you are using ``River Admin`` to create a commercial product,
please consider becoming our `sponsor`_  , `patron`_ or donate over `PayPal`_

.. _`patron`: https://www.patreon.com/javrasya
.. _`PayPal`: https://paypal.me/ceahmetdal
.. _`sponsor`: https://github.com/sponsors/javrasya

Getting Started
===============

You can easily get started with ``django-river`` by
following :ref:`getting-started`.

Contents
========

.. toctree::
   :maxdepth: 2

   getting_started
   authentication
   workflow/index
   function/index
   custom_admin
   workflow_object/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
