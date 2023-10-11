from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmationScreen(ModalScreen[bool]):
    """Screen with a confirmation dialog"""

    def __init__(self, command: list[str]):
        super().__init__()
        self.command = f"[bold cyan]{' '.join(command)}"

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.command, id="question"),
            Button("Migrate", variant="primary", id="yes"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
