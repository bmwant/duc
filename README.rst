Duc
===
.. image:: https://travis-ci.org/bmwant21/duc.svg?branch=master
    :target: https://travis-ci.org/bmwant21/duc
.. image:: https://coveralls.io/repos/bmwant21/duc/badge.svg
    :target: https://coveralls.io/r/bmwant21/duc

Duc (trans\ *duc*\ er) is a data transformation tool for Python.

.. code-block:: pycon

    >>> d = Duc({'name': {'validator': {'type': 'string'}, 'transform': {'name': 'number_name', 'type': 'integer'}})
    >>> v.validate({'name': '518'})
    True
    >>> v.transform()
    True
    >>> v.result
    {'number_name': 518}

About
-----
Sometimes your application receives data from one place and then (after some
transformation) sends it to other place. Often you cannot change the format of
data you receive because source dictates its own requirements. But with Duc you
can validate input (using `Cerberus <https://github.com/nicolaiarocci/cerberus>`_)
and make transformations on it (using similar syntax).
Particular example is when you get data from a client and save it to database.
You want to validate it or leave it *as-is* (if you trust client) but select
specific fields or transform data to other format is required. Slightly like
forms in web-application.
It was tested under Python 3.4. Compatibility with other versions is not
guaranteed.

Documentation
-------------
Complete documentation is missed by you can check *examples.py* for code snippets
and usage illustration

Installation
------------
Duc is on PyPI so all you need is:

.. code-block:: console

    $ pip install duc

Also you can install it from Github directly (to use latest version)

.. code-block:: console

    $ pip install git+https://github.com/bmwant21/duc.git

Testing
-------
Just run (with `Pytest <http://pytest.org/latest/>`_):

.. code-block:: console

    $ py.test tests

Copyright
---------
Duc is an open source project by `Most Wanted
<http://bmwlog.pp.ua>`_.
