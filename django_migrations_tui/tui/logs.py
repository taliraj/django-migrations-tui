from textual.widgets import RichLog


class Log(RichLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.display = False

    def on_mount(self):
        self.styles.border = ("round", "#0178D4")
        self.border_title = "Logs"
