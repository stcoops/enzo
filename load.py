from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar
from textual.containers import Vertical
from textual.reactive import reactive
from textual.timer import Timer
from rich.text import Text


class LoadingScreenApp(App):

    CSS = """
    Screen {
        align: center middle;
        background: black;
    }

    #logo {
        color: cyan;
        text-align: center;
        height: auto;
    }

    #status {
        color: white;
        text-align: center;
        padding: 1 0;
    }

    ProgressBar {
        width: 60;
        margin: 1 0;
    }
    """

    progress = reactive(0)
    current_step = reactive("")
    timer: Timer | None = None

    loading_steps = [
        ("Initializing Modules", 2),
        ("Loading Configuration Files", 3),
        ("Establishing Database Connection", 4),
        ("Starting Application Services", 2),
        ("Finalizing Setup", 1)
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(self.get_logo(), id="logo"),
            ProgressBar(total=sum(t for _, t in self.loading_steps)),
            Static("", id="status"),
        )

    def on_mount(self) -> None:
        self.step_index = 0
        self.elapsed = 0
        self.total_duration = sum(t for _, t in self.loading_steps)
        self.progress_bar = self.query_one(ProgressBar)
        self.status_widget = self.query_one("#status", Static)

        self.set_step()
        self.timer = self.set_interval(1.0, self.update_progress)

    def get_logo(self) -> str:
        return """
 █████╗ ██████╗ ██████╗      ██╗      █████╗  ██████╗ 
██╔══██╗██╔══██╗██╔══██╗     ██║     ██╔══██╗██╔════╝ 
███████║██████╔╝██████╔╝     ██║     ███████║██║  ███╗
██╔══██║██╔═══╝ ██╔═══╝ ██   ██║     ██╔══██║██║   ██║
██║  ██║██║     ██║      ╚█████╔╝     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚═╝     ╚═╝       ╚════╝      ╚═╝  ╚═╝ ╚═════╝ 
        """

    def set_step(self):
        if self.step_index < len(self.loading_steps):
            self.current_step, self.step_duration = self.loading_steps[self.step_index]
            self.time_in_step = 0
            self.status_widget.update(Text(f"[cyan]{self.current_step}[/]"))
        else:
            self.status_widget.update(Text("[green]✅ All systems ready! Launching application...[/]"))
            self.timer.stop()

    def update_progress(self):
        if self.step_index >= len(self.loading_steps):
            return

        self.elapsed += 1
        self.time_in_step += 1
        self.progress_bar.update(progress=self.elapsed)

        if self.time_in_step >= self.step_duration:
            self.step_index += 1
            self.set_step()


if __name__ == "__main__":
    LoadingScreenApp().run()
