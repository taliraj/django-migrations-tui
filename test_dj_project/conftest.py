import pytest
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder

from django_migrations_tui.tui.utils import get_migrations_list, get_migrations_plan


@pytest.fixture
def migrations_list():
    return get_migrations_list(argv=["manage.py", "migrationstui"])


@pytest.fixture
def migrations_plan():
    return get_migrations_plan(argv=["manage.py", "migrationstui"])


@pytest.fixture
def migrations_plan_verbosity_2():
    return get_migrations_plan(argv=["manage.py", "migrationstui", "-v", "2"])


@pytest.fixture
def recorded_migrations():
    recorder = MigrationRecorder(connections["default"])
    applied_migrations = recorder.applied_migrations().keys()
    return applied_migrations
