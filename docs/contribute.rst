.. _`Contribute`:

Contribute
==========

``River Admin`` consists of two parts that are backend and ui.
It is built with `Django Rest Framework`_ on the backend
side whereas Vue_ on the front end side.

Rive Admin Backend
------------------
``River Admin`` backend side is built with ``Django``
and `Django Rest Framework`_. So you need ``Django``
development environment to be set up.

1. Install the dependencies

   .. code:: bash

       pip install -r requirements.txt

2. Install Tox_ to run the tests for all environments.

   .. code:: bash

       pip install tox

3. Install Twine_ and other necessary packages to upload packages to ``PyPI``

   .. code:: bash

       pip install wheel setuptools twine

4. You are ready to develop the backend side now.

Development
~~~~~~~~~~~

   .. code:: bash

       python manage.py runserver

Tests
~~~~~

Tox_ is used on the backend side to automate ``Python`` & ``Django``
testing. Tests are under ``river-admin/tets/``. Simply run

   .. code:: bash

       tox

To run it for a specific environment;

   .. code:: bash

       tox -e py34-dj2.1

River Admin UI
--------------

``River Admin`` ui is built with Vue_. So you need ``Vue``
development environment to be set up.

1. Install ``node`` & ``npm``
2. Install ``yarn`` (`Install Yarn`_)
3. Install dependencies

   .. code:: bash

       yarn install


Development
~~~~~~~~~~~

While developing the front end ``Vue`` app of ``River Admin``,
you can run it without building it and the server will
auotmatically reload on any changes in the code. This is quite
useful thing for fast feedback and debugging. One thing you
should make sure before you run this, backend server is also
running since it needs to call the backend

   .. code:: bash

       python manage.py runserver

   .. code:: bash

       yarn serve


Tests
~~~~~

UI tests are written with Jest_ javascript testing
framework from Facebook. Tests are under ``ui/tets/``.
To run the tests simply;

   .. code:: bash

       yarn test:unit

To run a specific one;

   .. code:: bash

       yarn test:unit StateInput.spec.js

To run the tests with a fresh snapshot (to clean the snapshots);

   .. code:: bash

       yarn test:unit -u

Build
~~~~~

   .. code:: bash

       yarn build


The distribution folders of the ``Vue`` app are
``river_admin/templates`` and ``river_admin/static``.
The reason for that is because a ``Django`` app should
contains all the ``html`` and ``static`` files under
``templates`` and ``static`` folders.


.. _Vue: https://vuejs.org/
.. _`Install Yarn`: https://yarnpkg.com/en/docs/install
.. _`Django Rest Framework`: https://www.django-rest-framework.org/
.. _Jest: https://jestjs.io/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Twine: https://pypi.org/project/twine/