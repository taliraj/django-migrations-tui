from functools import partial

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.command import Hit, Hits, Provider
from textual.containers import Vertical
from textual.widgets import Footer, Header

from .confirmation import ConfirmationScreen
from .logs import Log
from .tree import MigrationsTree
from .utils import Format, get_migrations_plan


class SelectMigrationCommands(Provider):
    """A command provider to search for migrations."""

    async def startup(self) -> None:
        """Called once when the command palette is opened, prior to searching."""
        worker = self.app.run_worker(get_migrations_plan, thread=True)
        self.migrations = await worker.wait()

    async def search(self, query: str) -> Hits:
        """Search for migrations."""
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, MigrationsApp)

        for migration in self.migrations:
            command = f"Select {str(migration)}"
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),
                    partial(app.select_migration, migration),
                )


class MigrationsApp(App):
    """A Textual app to manage django migrations."""

    COMMANDS = App.COMMANDS | {SelectMigrationCommands}
    CSS_PATH = "static/app.tcss"
    TITLE = "Django Migrations TUI"

    BINDINGS = [
        ("v", "toggle_format", "View"),
        ("l", "toggle_logs", "Logs"),
        ("m", "migrate", "Migrate"),
        ("f", "fake_migration", "Fake"),
        ("r", "revert_migrations", "Revert"),
        ("s", "sqlmigrate", "SQL"),
        Binding("q", "quit", "Quit", show=False),
    ]

    def __init__(self, *args, format: Format, **kwargs):
        self.format = format
        super().__init__(*args, **kwargs)
        self.sql_code = ""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header()
            yield MigrationsTree(self.format)
            yield Log(markup=True, highlight=True, wrap=True)
            yield Footer()

    def on_migrations_tree_status(self, message: MigrationsTree.Status) -> None:
        """Called when the status of a migration changes."""
        rich_log = self.query_one(Log)
        if message.sql:
            if message.message == "BEGIN;":
                self.sql_code = message.message # reset
            elif message.message != "COMMIT;":
                self.sql_code = f"{self.sql_code}\n{message.message}"
            else:
                self.sql_code = f"{self.sql_code}\n{message.message}"
                rich_log.write(Syntax(self.sql_code, "sql", word_wrap=True, line_numbers=True))
        else:
            rich_log.write(message.message)
        rich_log.display = True

    def action_toggle_logs(self) -> None:
        """An action to toggle logs."""
        rich_log = self.query_one(Log)
        rich_log.display = not rich_log.display

    async def action_toggle_format(self) -> None:
        """An action to toggle the format of the migrations tree."""
        tree = self.query_one(MigrationsTree)
        await tree.toggle_format()

    def action_migrate(self) -> None:
        tree = self.query_one(MigrationsTree)
        command = tree.action_migrate()

        def check_confirmation(apply) -> None:
            if apply:
                tree.run_command(command)

        if command:
            self.push_screen(ConfirmationScreen(command), check_confirmation)

    def action_fake_migration(self) -> None:
        """An action to fake a migration."""
        tree = self.query_one(MigrationsTree)
        command = tree.fake_migration()

        def check_confirmation(apply) -> None:
            if apply:
                tree.run_command(command)

        if command:
            self.push_screen(ConfirmationScreen(command), check_confirmation)

    def action_revert_migrations(self) -> None:
        """An action to revert a migration."""
        tree = self.query_one(MigrationsTree)
        command = tree.revert_migrations()

        def check_confirmation(apply) -> None:
            if apply:
                tree.run_command(command)

        if command:
            self.push_screen(ConfirmationScreen(command), check_confirmation)

    def action_sqlmigrate(self) -> None:
        tree = self.query_one(MigrationsTree)
        command = tree.sqlmigrate()

        def check_confirmation(apply) -> None:
            if apply:
                tree.run_command(command, sql=True)

        if command:
            self.push_screen(ConfirmationScreen(command, "Print SQL"), check_confirmation)

    def select_migration(self, migration: str) -> None:
        tree = self.query_one(MigrationsTree)
        tree.select_migration(migration)
