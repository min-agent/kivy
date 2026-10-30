Kivy - Documentation
====================

You can access the latest documentation on the web:

* http://kivy.org/docs

Contributing
------------

If you intend on editing and contributing documentation, assure the kivy source
code is up to date before proceeding. If your documentation is outdated, it
could result in merge conflicts.

Install Sphinx
--------------

- With uv (https://docs.astral.sh/uv/):

  ``uv venv``

  ``uv pip install sphinx``

  ``source .venv/bin/activate``

- With apt-get:
    

  ``apt-get install python-sphinx``

- With MacPorts:
  

  ``port install py34-sphinx``

- On Windows:

  Install uv (https://docs.astral.sh/uv/), then run ``uv venv`` and:

  ``uv pip install sphinx``

  ``.venv\Scripts\activate``
  

Building the documentation
--------------------------

Generate documentation using make: ``make html``.

Documentation will be accessible in ``build/html/``.

