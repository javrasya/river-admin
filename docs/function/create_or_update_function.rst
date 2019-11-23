.. _create-or-update-function:

.. |Create Function| image:: /_static/images/create-function.png

Create & Update Function
========================

.. note::
    ``River Admin`` is not extending the APIs of ``django-river``.
    In order to see how your functions should look like please
    visit the `django river function documentation`_ itself

.. _django river function documentation: https://django-river.readthedocs.io/en/latest/hooking/function.html#context-parameter

|Create Function|

.. note::
    Changes on the functions are applied to your hooks right away.
    It means that, next time a hook is kicked in with this function
    will be executed with the up to date version of the function.
