=====================
django-migrations-tui
=====================

Manage Django Migrations with a Text-Based UI

Installation
------------
To install, simply use ``pip``:

.. code-block:: console

    pip install django-migrations-tui

Quick start
-----------

#. Add ``django_migrations_tui`` to your Django project's ``INSTALLED_APPS``.
#. Run the following command to start the interactive UI.

    .. code-block:: console

        python manage.py migrationstui

#. Utilize the arrow keys for navigation and letter keys to perform actions:

   * ``v``: Change the format of the migration view between ``list`` and ``plan``
   * ``l``: Toggle the logs panel
   * ``m``: Run ``migrate`` on the selected migration or app
   * ``f``: Run ``migrate --fake`` on the selected migration or app
   * ``r``: Run ``migrate <app name> zero`` on the selected app
   * ``s``: Run ``sqlmigrate`` on the selected migration
   * ``q``: Quit the UI
   * ``ctrl+\``: Search and select migrations by name
   * Additionally, some vim keybindings are supported for navigation, including ``j``, ``k``, ``ctrl+home``, ``G``, ``ctrl+b`` and ``ctrl+f``.

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
