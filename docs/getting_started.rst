.. _getting-started:

.. |Issue Tracking Workflow Img| image:: /_static/images/issue-tracking-workflow.png
.. |Shipping Workflow Img| image:: /_static/images/shipping-workflow.png


Getting Started
===============

Installation
------------
.. note::
    Before you can set up your workflow, your app integration with ``django-river`` must be done. Don't worry it is with the easiest setup.  
    To see how to do it with ``django-river`` pleas have a look at `django-river`

.. _django-river: https://github.com/javrasya/django-river/

1. Install and enable it

   .. code:: bash

       pip install django-river-admin


   .. code:: python

       INSTALLED_APPS=[
           ...
           river,
           river-admin
           ...
       ]

2. (For production) collect static;

   .. code:: bash

       python manage.py collectstatic

3. Run your application;

   .. code:: bash

       python manage.py runserver 0.0.0.0:8000


4. Open it up on the browser and login with an admin user and enjoy the best way of flowing your work ever :-)

   .. code:: bash

       http://0.0.0.0:8000/river-admin/


Out of the Box Examples
-----------------------

``River Admin`` comes with few examples that you can fiddle with and find your way easier.


.. note::
    Enabling them will create their tables and also the necessary workflow components in the DB for you. 
    It might be good idea to try them out on a development database.

Shipping Flow
^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       INSTALLED_APPS=[
           ...
           river,
           river-admin,
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
           river,
           river-admin,
           'river_admin_issue_tracker_example',
           ...
       ]

|Issue Tracking Workflow Img|