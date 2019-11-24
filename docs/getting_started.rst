.. _getting-started:

.. |Issue Tracking Workflow Img| image:: /_static/images/issue-tracking-workflow.png
.. |Shipping Workflow Img| image:: /_static/images/shipping-workflow.png


Getting Started
===============

Requirements
------------

* `django-river`_ >= 3.0.0
* Any ``Python`` version that is supported by `django-river`_
* Any ``Django`` version that is supported by `django-river`_
* Any browser that is supported by `Vuetify`_ (`Browser Support`_)

.. _`Browser Support`: https://vuetifyjs.com/en/getting-started/browser-support#browser-support
.. _`Vuetify`: https://vuetifyjs.com/en/
.. _`django-river`: https://github.com/javrasya/django-river

Installation
------------
.. note::
    Before you can set up your workflow, your app
    integration with ``django-river`` must be done.
    Don't worry it is with the easiest setup.To see
    how to do it with ``django-river`` pleas have a
    look at `django-river`

1. Install and enable it

   .. code:: bash

       pip install django-river-admin


   .. code:: python

       INSTALLED_APPS=[
           ...
           'river',
           'river-admin'
           ...
       ]

2. Register ``River Admin`` urls in your app ``urls.py``

   .. code:: python

        urlpatterns = [
            url(r'^', include("river_admin.urls")),
        ]

3. Collect statics **(For production)**;

   .. code:: bash

       python manage.py collectstatic

4. Run your application;

   .. code:: bash

       python manage.py runserver 0.0.0.0:8000


5. Open it up on the browser and login with an admin user and enjoy the best way of flowing your work ever :-)

   .. code:: bash

       http://0.0.0.0:8000/river-admin/


Out of the Box Examples
-----------------------

``River Admin`` comes with few examples that you can
fiddle with and find your way easier.


.. note::
    Enabling them will create their tables and
    also the necessary workflow components in
    the DB for you. It might be good idea to try
    them out on a development database.

Shipping Flow
^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       INSTALLED_APPS=[
           ...
           'river',
           'river-admin',
           'river_admin_shipping_example',
           ...
       ]

|Shipping Workflow Img|


Issue Tracking Flow
^^^^^^^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       INSTALLED_APPS=[
           ...
           'river',
           'river-admin',
           'river_admin_issue_tracker_example',
           ...
       ]

|Issue Tracking Workflow Img|


.. toctree::
   :maxdepth: 2
