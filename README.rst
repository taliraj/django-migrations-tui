=====================
django-migrations-tui
=====================

Manage Django Migrations with a Text-Based UI

Installation
------------
``django-migrations-tui`` is available on PyPI and can be installed with ``pip``:

.. code-block:: console

    pip install django-migrations-tui

Quick start
-----------

#. Add ``django_migrations_tui`` to your ``INSTALLED_APPS``.
#. Run ``python manage.py migrationstui`` to start the UI.
#. Use the arrow keys to navigate and press the letter keys to perform actions. The available actions are:

   * ``v``: Change the format of the migration list: ``list`` or ``plan``
   * ``l``: Toggle the logs panel
   * ``m``: Run ``migrate`` on the selected migration or app
   * ``f``: Run ``migrate --fake`` on the selected migration or app
   * ``r``: Run ``migrate <app name> zero`` on the selected app
   * ``q``: Quit the UI
   * ``ctrl+\``: Search and select migrations by name
   * Some vim keybindings are also supported for navigation. Supported movements are ``j``, ``k``, ``ctrl+home``, ``G``, ``ctrl+b`` and ``ctrl+f``.

Screenshots
-----------

.. image:: https://user-images.githubusercontent.com/3104974/274433860-d6d5abf7-0c7f-4dc2-844e-96b3c1d7b404.png
    :alt: Screenshot of django-migrations-tui
    :width: 45%
    :target: https://user-images.githubusercontent.com/3104974/274433860-d6d5abf7-0c7f-4dc2-844e-96b3c1d7b404.png


.. image:: https://user-images.githubusercontent.com/3104974/274433862-58530910-291f-41e6-8c21-b445b5085229.png
    :alt: Screenshot of django-migrations-tui
    :width: 45%
    :target: https://user-images.githubusercontent.com/3104974/274433862-58530910-291f-41e6-8c21-b445b5085229.png
