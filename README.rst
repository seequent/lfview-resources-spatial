LFView Resources - Spatial
************************************************************************

.. image:: https://img.shields.io/pypi/v/lfview-resources-spatial.svg
    :target: https://pypi.org/project/lfview-resources-spatial
.. image:: https://readthedocs.org/projects/lfview-resources-spatial/badge/
    :target: http://lfview-resources-spatial.readthedocs.io/en/latest/
.. image:: https://travis-ci.com/seequent/lfview-resources-spatial.svg?branch=master
    :target: https://travis-ci.com/seequent/lfview-resources-spatial
.. image:: https://codecov.io/gh/seequent/lfview-resources-spatial/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/seequent/lfview-resources-spatial
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/seequent/lfview-resources-spatial/blob/master/LICENSE

.. warning::

    The LF View API and all associated Python client libraries are in
    **pre-release**. They are subject to change at any time, and
    backwards compatibility is not guaranteed.

What is lfview-resources-spatial?
-----------------------------------
This library defines 3D spatial resources in the `LF View <https://lfview.com>`_ API.
Resources include point sets, line sets, surfaces, and volumes as well
as data, textures, and basic display options.

Scope
-----
This library simply includes declarative definitions of spatial resources.
It is built on `properties <https://propertiespy.readthedocs.io/en/latest/>`_ to
provide type-checking, validation, documentation, and serialization.
Very likely, these spatial resources will be used in conjunction with
the `LF View API Python client <https://lfview.readthedocs.io/en/latest/>`_.

Installation
------------

You may install this library using
`pip <https://pip.pypa.io/en/stable/installing/>`_  with

.. code::

    pip install lfview-resources-spatial

or from `Github <https://github.com/seequent/lfview-resources-spatial>`_

.. code::

    git clone https://github.com/seequent/lfview-resources-spatial.git
    cd lfview-resources-spatial
    pip install -e .

You may also just install the LF View API Python client with

.. code::

    pip install lfview-api-client

Either way, after installing, you may access these resources with

.. code:: python

    from lfview.resources import spatial

    points = spatial.ElementPointSet(
        vertices=[[1., 2, 3], [4, 5, 6]],
        data=spatial.DataBasic(
            location='nodes',
            array=[10., 20],
        ),
    )
