.. |Build Status| image:: https://travis-ci.org/javrasya/river-admin.svg?branch=master
    :target: https://travis-ci.org/javrasya/river-admin

.. |Doc Status| image:: https://readthedocs.org/projects/river-admin/badge/?version=latest
    :target: https://river-admin.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |Licence| image:: https://img.shields.io/github/license/javrasya/river-admin
    :alt: GitHub license
    :target: https://github.com/javrasya/river-admin/blob/master/LICENSE

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

|Build Status| |Doc Status| |Licence| |Coverage Status| |Code Quality|

``River Admin`` is a very modern and
a shiny customizable admin extension with user friendly and easy to use
interfaces for django-river_ . The power of it comes from the libraries
it uses on both backend and frontend sides which are ``django-river``,
``django-rest-framework`` ``Vue`` and ``Vuetify``.

.. rst-class:: center-without-bg

|Images|

.. _django-river: https://github.com/javrasya/django-river/

Donations
=========

This is a fully open source project and it can be better with your donations.

If you are using ``River Admin`` to create a commercial product,
please consider becoming our `sponsor`_  , `patron`_ or donate over `PayPal`_

.. _`patron`: https://www.patreon.com/javrasya
.. _`PayPal`: https://paypal.me/ceahmetdal
.. _`sponsor`: https://github.com/sponsors/javrasya

Live Demo
=========

https://river-admin-demo.herokuapp.com/river-admin/

- User: demo
- Password: demo

To run demo locally;

   .. code:: bash

        export LOCAL_DEMO=True
        pip install -r requirements.txt
        python manage.py migrate
        python manage.py bootstrap_shipping_example
        python manage.py bootstrap_issue_tracker_example
        python manage.py bootstrap_river_admin_demo
        python manage.py runserver

And then go to ``http://127.0.0.1:8000/river-admin/``

**Note:** Create an admin user for yourself if you would like more access.

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
   contribute


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
