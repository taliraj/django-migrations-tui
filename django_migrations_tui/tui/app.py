from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header

from .logs import Log
from .tree import MigrationsTree
from .utils import Format


class MigrationsApp(App):
    """A Textual app to manage django migrations."""

    TITLE = "Django Migrations TUI"

    BINDINGS = [
        ("v", "toggle_format", "View"),
        ("l", "toggle_logs", "Logs"),
        ("m", "migrate", "Migrate"),
        ("f", "fake_migration", "Fake"),
        ("r", "revert_migrations", "Revert App"),
    ]

    def __init__(self, *args, format: Format, **kwargs):
        self.format = format
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Vertical():
            yield Header()
            yield MigrationsTree(self.format)
            yield Log(markup=True, highlight=True, wrap=True)
            yield Footer()

    def action_migrate(self) -> None:
        tree = self.query_one(MigrationsTree)
        tree.action_migrate()

    def on_migrations_tree_status(self, message: MigrationsTree.Status) -> None:
        """Called when the status of a migration changes."""
        rich_log = self.query_one(Log)
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

    def action_fake_migration(self) -> None:
        """An action to fake a migration."""
        tree = self.query_one(MigrationsTree)
        tree.fake_migration()

    def action_revert_migrations(self) -> None:
        """An action to revert a migration."""
        tree = self.query_one(MigrationsTree)
        tree.revert_migrations()
