from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header

from .confirmation import ConfirmationScreen
from .logs import Log
from .tree import MigrationsTree
from .utils import Format


class MigrationsApp(App):
    """A Textual app to manage django migrations."""

    CSS_PATH = "static/app.tcss"
    TITLE = "Django Migrations TUI"

    BINDINGS = [
        ("v", "toggle_format", "View"),
        ("l", "toggle_logs", "Logs"),
        ("m", "migrate", "Migrate"),
        ("f", "fake_migration", "Fake"),
        ("r", "revert_migrations", "Revert"),
        Binding("q", "quit", "Quit", show=False),
    ]

    def __init__(self, *args, format: Format, **kwargs):
        self.format = format
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header()
            yield MigrationsTree(self.format)
            yield Log(markup=True, highlight=True, wrap=True)
            yield Footer()

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
