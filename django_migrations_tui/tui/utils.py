import enum
import sys
from dataclasses import dataclass

from django.core.management import ManagementUtility, handle_default_options
from django.db import connections


class Format(enum.StrEnum):
    LIST = "list"
    PLAN = "plan"


@dataclass
class MigrationsList:
    app_name: str
    applied_count: int
    migrations: list[str]

    def __str__(self):
        if self.migrations == [" (no migrations)"]:
            return f"{self.app_name} (0/0)"
        return f"{self.app_name} ({self.applied_count}/{len(self.migrations)})"


def migrations_command():
    utility = ManagementUtility(["migrationstui"])
    command = utility.fetch_command("migrationstui")

    # argv = ['manage.py', 'migrationstui']
    argv = sys.argv
    command._called_from_command_line = True
    parser = command.create_parser(argv[0], argv[1])

    options = parser.parse_args(argv[2:])
    cmd_options = vars(options)
    # Move positional args out of options to mimic legacy optparse
    handle_default_options(options)
    command.verbosity = cmd_options["verbosity"]

    # Get the database we're operating from
    return command, cmd_options


def get_migrations_list():
    command, cmd_options = migrations_command()
    db = cmd_options["database"]
    connection = connections[db]
    migrations = command.show_list(connection, cmd_options["app_label"])
    return migrations


def get_migrations_plan():
    command, cmd_options = migrations_command()
    db = cmd_options["database"]
    connection = connections[db]
    plan = command.show_plan(connection, cmd_options["app_label"])
    return plan
