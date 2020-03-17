.. _getting-started:

.. |Issue Tracking Workflow Img| image:: /_static/images/issue-tracking-workflow.png
.. |Shipping Workflow Img| image:: /_static/images/shipping-workflow.png


Getting Started
===============

Requirements
------------

* `django-river`_ >= 3.2.0
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

       pip install river-admin


   .. code:: python

       # settings.py

       INSTALLED_APPS=[
           ...
           'river',
           'rest_framework.authtoken',
           'river_admin'
           ...
       ]

       REST_FRAMEWORK = {
           'DEFAULT_AUTHENTICATION_CLASSES': [
               'rest_framework.authentication.BasicAuthentication',
               'rest_framework.authentication.TokenAuthentication',
           ],
           'EXCEPTION_HANDLER': 'river_admin.views.exception_handler'
       }

2. Do migration;

   .. code:: bash

        python manage.py migrate

3. Register ``River Admin`` urls in your app ``urls.py``

   .. code:: python

        urlpatterns = [
            url(r'^', include("river_admin.urls")),
        ]

4. Collect statics and make sure ``STATIC_URL`` is ``/static/`` **(FOR PRODUCTION WHERE DEBUG=False)**;

   .. code:: bash

       python manage.py collectstatic --no-input --no-post-process

5. Run your application;

   .. code:: bash

       python manage.py runserver 0.0.0.0:8000


6. Open it up on the browser and login with an admin user and enjoy the best way of flowing your work ever :-)

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

       # settings.py

       INSTALLED_APPS=[
           ...
           'river',
           'rest_framework.authtoken',
           'river_admin',
           'examples.shipping_example',
           ...
       ]

   .. code:: bash

        python manage.py migrate
        python manage.py bootstrap_shipping_example

|Shipping Workflow Img|

Issue Tracking Flow
^^^^^^^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       # settings.py

       INSTALLED_APPS=[
           ...
           'river',
           'rest_framework.authtoken',
           'river_admin',
           'examples.issue_tracker_example',
           ...
       ]

   .. code:: bash

        python manage.py migrate
        python manage.py bootstrap_issue_tracker_example

|Issue Tracking Workflow Img|


.. toctree::
   :maxdepth: 2
