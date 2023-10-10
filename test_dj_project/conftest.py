import pytest
from django.core.management import ManagementUtility, handle_default_options
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder


@pytest.fixture
def command():
    utility = ManagementUtility(["migrationstui"])
    command = utility.fetch_command("migrationstui")

    argv = ["manage.py", "migrationstui"]
    command._called_from_command_line = True
    parser = command.create_parser(argv[0], argv[1])

    options = parser.parse_args(argv[2:])
    cmd_options = vars(options)
    # Move positional args out of options to mimic legacy optparse
    handle_default_options(options)
    command.verbosity = cmd_options["verbosity"]

    # Get the database we're operating from
    db = cmd_options["database"]
    connection = connections[db]

    return command, connection, cmd_options


@pytest.fixture
def migrations_list(command):
    command, connection, cmd_options = command
    migrations = command.show_list(connection, cmd_options["app_label"])
    return migrations


@pytest.fixture
def migrations_plan(command):
    command, connection, cmd_options = command
    migrations = command.show_plan(connection, cmd_options["app_label"])
    return migrations


@pytest.fixture
def migrations_plan_verbosity_2(command):
    command, connection, cmd_options = command
    command.verbosity = 2
    migrations = command.show_plan(connection, cmd_options["app_label"])
    return migrations


@pytest.fixture
def recorded_migrations():
    recorder = MigrationRecorder(connections["default"])
    applied_migrations = recorder.applied_migrations().keys()
    return applied_migrations
