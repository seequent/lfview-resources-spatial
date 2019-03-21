.. _resources_spatial:

.. include:: ../README.rst

{%- if graph %}
.. image:: {{ graph }}
{%- endif %}

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   {% for module in modules %}
   content/{{ '_'.join(module.split('.'))}}
   {%- endfor %}
   {%- for other_file in other_files %}
   content/{{ other_file.split('.')[0] }}
   {%- endfor %}

* :ref:`genindex`
