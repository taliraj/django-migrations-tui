import enum
import sys
from dataclasses import dataclass
from typing import List

from django.core.management import ManagementUtility, handle_default_options
from django.db import connections


class Format(enum.Enum):
    LIST = "list"
    PLAN = "plan"


@dataclass
class MigrationsList:
    app_name: str
    applied_count: int
    migrations: List[str]

    def __str__(self):
        if self.migrations == [" (no migrations)"]:
            return f"{self.app_name} (0/0)"
        return f"{self.app_name} ({self.applied_count}/{len(self.migrations)})"


def get_migrations(format: Format = Format.LIST, argv=None):
    utility = ManagementUtility(["migrationstui"])
    command = utility.fetch_command("migrationstui")

    if argv is None:
        argv = sys.argv
    if len(argv) < 2:
        argv = ["manage.py", "migrationstui"]

    command._called_from_command_line = True
    parser = command.create_parser(argv[0], argv[1])

    options = parser.parse_args(argv[2:])
    cmd_options = vars(options)
    # Move positional args out of options to mimic legacy optparse
    handle_default_options(options)
    command.verbosity = cmd_options["verbosity"]

    db = cmd_options["database"]
    connection = connections[db]

    if format == Format.LIST:
        migrations = command.show_list(connection, cmd_options["app_label"])
    else:
        migrations = command.show_plan(connection, cmd_options["app_label"])
    return migrations


def get_migrations_list(argv=None):
    return get_migrations(format=Format.LIST, argv=argv)


def get_migrations_plan(argv=None):
    return get_migrations(format=Format.PLAN, argv=argv)
