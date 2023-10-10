from django.core.management.commands.showmigrations import (
    Command as ShowMigrationsCommand,
)
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder

from django_migrations_tui.tui.app import Format, MigrationsApp
from django_migrations_tui.tui.utils import MigrationsList


class Command(ShowMigrationsCommand):
    help = "Show all migrations and their status in a TUI."

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]
        self.options = options

        if options["format"] == "plan":
            format = Format.PLAN
        else:
            format = Format.LIST

        app = MigrationsApp(format=format)
        app.run()

    def show_list(self, connection, app_names=None):
        """
        Show a list of all migrations on the system, or only those of
        some named apps.
        """
        # Load migrations from disk/DB
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        recorder = MigrationRecorder(connection)
        recorded_migrations = recorder.applied_migrations()
        graph = loader.graph
        # If we were passed a list of apps, validate it
        if app_names:
            self._validate_app_names(loader, app_names)
        # Otherwise, show all apps in alphabetic order
        else:
            app_names = sorted(loader.migrated_apps)

        migrations = list()
        for app_name in app_names:
            app_migration = MigrationsList(app_name, 0, list())
            shown = set()
            for node in graph.leaf_nodes(app_name):
                for plan_node in graph.forwards_plan(node):
                    if plan_node not in shown and plan_node[0] == app_name:
                        # Give it a nice title if it's a squashed one
                        title = plan_node[1]
                        if graph.nodes[plan_node].replaces:
                            title += " (%s squashed migrations)" % len(
                                graph.nodes[plan_node].replaces
                            )
                        applied_migration = loader.applied_migrations.get(plan_node)
                        # Mark it as applied/unapplied
                        if applied_migration:
                            if plan_node in recorded_migrations:
                                output = " [X] %s" % title
                                app_migration.applied_count += 1
                            else:
                                title += " Run 'manage.py migrate' to finish recording."
                                output = " [-] %s" % title
                            if self.verbosity >= 2 and hasattr(
                                applied_migration, "applied"
                            ):
                                output += (
                                    " (applied at %s)"
                                    % applied_migration.applied.strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    )
                                )
                            app_migration.migrations.append(output)
                        else:
                            app_migration.migrations.append(" [ ] %s" % title)
                        shown.add(plan_node)
            # If we didn't print anything, then a small message
            if not shown:
                app_migration.migrations.append(" (no migrations)")

            migrations.append(app_migration)
        return migrations

    def show_plan(self, connection, app_names=None):
        """
        Show all known migrations (or only those of the specified app_names)
        in the order they will be applied.
        """
        # Load migrations from disk/DB
        loader = MigrationLoader(connection)
        graph = loader.graph
        if app_names:
            self._validate_app_names(loader, app_names)
            targets = [key for key in graph.leaf_nodes() if key[0] in app_names]
        else:
            targets = graph.leaf_nodes()
        plan = []
        seen = set()

        # Generate the plan
        for target in targets:
            for migration in graph.forwards_plan(target):
                if migration not in seen:
                    node = graph.node_map[migration]
                    plan.append(node)
                    seen.add(migration)

        # Output
        def print_deps(node):
            out = []
            for parent in sorted(node.parents):
                out.append("%s.%s" % parent.key)
            if out:
                return " ... (%s)" % ", ".join(out)
            return ""

        migrations_plan = []
        for node in plan:
            deps = ""
            if self.verbosity >= 2:
                deps = print_deps(node)
            if node.key in loader.applied_migrations:
                migrations_plan.append(
                    "[X]  %s.%s%s" % (node.key[0], node.key[1], deps)
                )
            else:
                migrations_plan.append(
                    "[ ]  %s.%s%s" % (node.key[0], node.key[1], deps)
                )
        if not plan:
            migrations_plan.append("(no migrations)")

        return migrations_plan
