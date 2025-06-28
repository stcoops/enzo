
from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar
from textual.containers import Container, Center, Vertical
from textual.reactive import reactive
from textual.timer import Timer
from textual.events import Key

class LoadingScreenApp(App):
    CSS = """
    Screen {
        background: rgb(30,30,30);
        align: center middle;
    }

    #logo {
        color: rgb(210,210,210);
        text-align: center;
        margin: 1;
    }

    #status {
        color: white;
        text-align: center;
        padding: 0 0;
    }

    ProgressBar {
        align: center middle;
        padding: 0 0;
        width: 60;
        margin: 1;
    }
    
    Bar > .bar--indeterminate {
        color: rgb(120,120,120);
        background: rgb(60,60,60);
    }

    Bar > .bar--bar {
        color: rgb(180,180,180);
        background: rgb(90,90,90);
    }

    Bar > .bar--complete {
        color: rgb(210,210,210);
    }

    #content {
        align: center middle;
        height: auto;
        margin: 1;
    }

    #vert {
        align: center middle;
        height: auto;
        margin: 1;
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
        yield Container(
                        Static(self.get_logo(), id="logo"),
                        Center(ProgressBar(total=sum(t for _, t in self.loading_steps), show_eta = False, show_percentage=False)),
                        Static("", id="status"),
                        id="content"
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
        return r"""
     __   ___ _  
    |_ |\| _// \ 
    |__| |/__\_/ 
        """

    def set_step(self):
        if self.step_index < len(self.loading_steps):
            self.current_step, self.step_duration = self.loading_steps[self.step_index]
            self.time_in_step = 0
            self.status_widget.update(f"-> {self.current_step}")
        else:
            self.status_widget.update("All systems ready! Launching application...")
            self.timer.stop()
            self.set_timer(2.0, self.action_quit)  # Wait before quitting

    def update_progress(self):
        if self.step_index >= len(self.loading_steps):
            return

        self.elapsed += 1
        self.time_in_step += 1
        self.progress_bar.update(progress=self.elapsed)

        if self.time_in_step >= self.step_duration:
            self.step_index += 1
            self.set_step()

    async def on_key(self, event: Key) -> None:
        """Allow user to quit with 'q' or Ctrl+C."""
        if event.key == "q":
            await self.action_quit()

    async def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    try:
        LoadingScreenApp().run()
    except KeyboardInterrupt:
        print("\n[Interrupted] Exiting cleanly...")
