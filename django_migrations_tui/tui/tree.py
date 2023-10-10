import asyncio

from asgiref.sync import sync_to_async
from textual import work
from textual.message import Message
from textual.widgets import Tree
from textual.worker import Worker, WorkerState

from .utils import Format, get_migrations_list, get_migrations_plan

# TODO: Add a way to search for a migration and filter


class MigrationsTree(Tree):
    """A widget to display migrations."""

    class Status(Message):
        """A message to update the status of a migration."""

        def __init__(self, message: str):
            self.message = message
            super().__init__()

    def __init__(self, format: Format):
        self.format = format
        super().__init__("")

    def on_mount(self):
        self.styles.border = ("round", "#0178D4")

        if self.format == Format.PLAN:
            return self.update_migrations_plan()
        else:
            return self.update_migrations_list()

    async def toggle_format(self) -> None:
        if self.format == Format.LIST:
            self.format = Format.PLAN
            await self.update_migrations_plan()
        else:
            self.format = Format.LIST
            await self.update_migrations_list()

    async def update_migrations_list(self) -> None:
        migrations = await self.get_migrations_list()
        total_migrations = sum(
            [
                len(app.migrations)
                for app in migrations
                if app.migrations != [" (no migrations)"]
            ]
        )
        total_applied = sum([app.applied_count for app in migrations])

        self.reset("migrations (%s/%s)" % (total_applied, total_migrations))
        self.root.expand()
        for app in migrations:
            current_app = self.root.add(str(app))
            for migration_name in app.migrations:
                current_app.add_leaf(migration_name)

    async def reload_migrations_list(self) -> None:
        migrations = await self.get_migrations_list()
        total_migrations = sum(
            [
                len(app.migrations)
                for app in migrations
                if app.migrations != [" (no migrations)"]
            ]
        )
        total_applied = sum([app.applied_count for app in migrations])
        self.root.set_label("migrations (%s/%s)" % (total_applied, total_migrations))

        for child, app in zip(self.root.children, migrations):
            child.set_label(str(app))
            for child_child, migration_name in zip(child.children, app.migrations):
                child_child.set_label(migration_name)

    async def update_migrations_plan(self) -> None:
        migrations = await self.get_migrations_plan()
        total_migrations = len(migrations)
        total_applied = sum(
            [1 for migration in migrations if migration.startswith("[X]")]
        )

        self.reset("plan (%s/%s)" % (total_applied, total_migrations))
        self.root.expand()
        for item in migrations:
            self.root.add_leaf(item)

    @sync_to_async
    def get_migrations_list(self):
        return get_migrations_list()

    @sync_to_async
    def get_migrations_plan(self):
        return get_migrations_plan()

    def action_migrate(self) -> None:
        if self.format == Format.LIST:
            self.migrate_list()
        else:
            self.migrate_plan()

    def migrate_list(self) -> None:
        selected_item = self.cursor_node
        if selected_item.is_root:
            command = ["python", "manage.py", "migrate"]
        elif selected_item.allow_expand:
            app_name = str(selected_item.label).split(" (")[0]
            command = ["python", "manage.py", "migrate", app_name]
        elif (
            not selected_item.allow_expand
            and str(selected_item.label) == " (no migrations)"
        ):
            self.post_message(self.Status("No migrations to apply."))
            return
        else:
            app_name = str(selected_item.parent.label).split(" (")[0]
            migration_name = str(selected_item.label).split("] ")[1]
            command = ["python", "manage.py", "migrate", app_name, migration_name]

        self.run_command(command)

    def migrate_plan(self) -> None:
        selected_item = self.cursor_node
        if selected_item.is_root:
            command = ["python", "manage.py", "migrate"]
        else:
            # discard the [X] from the label
            migration = str(selected_item.label)[5:]
            command = ["python", "manage.py", "migrate", *migration.split(".")]

        self.run_command(command)

    @work(exclusive=True)
    async def run_command(self, command: list[str]):
        self.post_message(self.Status(f"\n[bold cyan]{' '.join(command)}"))

        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        while proc.returncode is None:
            line = await proc.stdout.readline()
            if not line:
                break
            self.post_message(self.Status(line.decode("utf-8").rstrip()))
        _, stderr = await proc.communicate()
        if stderr:
            self.post_message(self.Status(stderr.decode("utf-8")))

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state in [
            WorkerState.CANCELLED,
            WorkerState.ERROR,
            WorkerState.SUCCESS,
        ]:
            if self.format == Format.LIST:
                await self.reload_migrations_list()
            else:
                await self.update_migrations_plan()

    def fake_migration(self) -> None:
        if self.format == Format.LIST:
            self.fake_migration_list()
        else:
            self.fake_migration_plan()

    def fake_migration_list(self) -> None:
        selected_item = self.cursor_node
        if selected_item.is_root:
            command = ["python", "manage.py", "migrate", "--fake"]
        elif selected_item.allow_expand:
            app_name = str(selected_item.label).split(" (")[0]
            command = ["python", "manage.py", "migrate", "--fake", app_name]
        elif (
            not selected_item.allow_expand
            and str(selected_item.label) == " (no migrations)"
        ):
            self.post_message(self.Status("No migrations to fake."))
            return
        else:
            app_name = str(selected_item.parent.label).split(" (")[0]
            migration_name = str(selected_item.label).split("] ")[1]
            command = [
                "python",
                "manage.py",
                "migrate",
                "--fake",
                app_name,
                migration_name,
            ]

        self.run_command(command)

    def fake_migration_plan(self) -> None:
        selected_item = self.cursor_node
        if selected_item.is_root:
            command = ["python", "manage.py", "migrate", "--fake"]
        else:
            # discard the [X] from the label
            migration = str(selected_item.label)[5:]
            command = [
                "python",
                "manage.py",
                "migrate",
                "--fake",
                *migration.split("."),
            ]

        self.run_command(command)

    def revert_migrations(self) -> None:
        """Revert all migrations for an app."""
        if self.format == Format.LIST:
            selected_item = self.cursor_node
            if selected_item.allow_expand and not selected_item.is_root:
                app_name = str(selected_item.label).split(" (")[0]
                command = ["python", "manage.py", "migrate", app_name, "zero"]
                self.run_command(command)
            else:
                self.post_message(self.Status("Select an app to revert."))
        else:
            self.post_message(
                self.Status("Revertions are not supported in plan format.")
            )
