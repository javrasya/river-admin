.. _authentication:

.. |Login Page Img| image:: /_static/images/login.png


Authentication
==============


``River Admin`` is working like an administration interface
and naturally it has an authentication mechanism.
Even though it is working with the users  who are created
via Django API, it doesn't use Django Admin logged in your
Django admin. So you will be asked to login with your user;


|Login Page Img|

.. note::
    In order to be able to login, your user has to be either an admin user or having ``river_workflow.view`` permissions. So to speak, ``river_workflow.view``
    is the minimum required permission to be able to user ``River Admin``


Once user is logged in, they won't be asked by their credentials
until they are logged out or their minimum required permission
described above is revoked.

.. toctree::
   :maxdepth: 2
