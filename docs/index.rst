.. |Build Status| image:: https://travis-ci.org/javrasya/river-admin.svg?branch=master
    :target: https://travis-ci.org/javrasya/river-admin

.. |Doc Status| image:: https://readthedocs.org/projects/river-admin/badge/?version=latest
    :target: https://river-admin.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |Coverage Status| image:: https://coveralls.io/repos/github/javrasya/river-admin/badge.svg?branch=master
    :target: https://coveralls.io/github/javrasya/river-admin?branch=master

.. |Code Quality| image:: https://api.codacy.com/project/badge/Grade/3e7f03e8df5a488f90fb0ed93295c41b
    :target: https://www.codacy.com/manual/javrasya/river-admin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=javrasya/river-admin&amp;utm_campaign=Badge_Grade

.. |Timeline Img| image:: /_static/images/timeline-in-macbook.png

.. |Home Img| image:: /_static/images/home-left-panel-on-in-macbook.png

.. |Re-prio Img| image:: /_static/images/re-prioritization-in-macbook.png

.. |Workflow Edit Img| image:: /_static/images/edit-workflow-in-macbook.png

.. |Images| image:: /_static/images/readme-images.gif



River Admin
===========

.. rst-class:: center-without-bg

|Build Status| |Doc Status| |Coverage Status| |Code Quality|

``River Admin`` is a very modern and shiny web application functioning
like an admin interface that provides administration for django-river_ .
It basically extends the ``django-river`` flexibility with some user
friendly and very easy to use admin interfaces.

The power of it comes from the libraries it uses on both backend and
frontend sides which are ``django-river``, ``django-rest-framework``
``Vue``, ``Vuetify``

.. rst-class:: center-without-bg

|Images|

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
