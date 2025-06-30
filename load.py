
from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar
from textual.containers import Container, Center
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
    """

    progress = reactive(0)
    current_step = reactive("")
    timer: Timer | None = None

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.get_logo(), id="logo"),
            Center(ProgressBar(show_eta=False, show_percentage=False)),
            Static("", id="status"),
            id="content"
        )

    def on_mount(self) -> None:
        # Now self is available — safe to assign functions
        self.loading_steps = [
            ("Loading Configuration Files", 10, self.getConfig),
            ("Establishing Model Connection", 10, self.startLLM),
            ("Starting Text-to-Speech Service", 10, self.loadTTS),
            ("Finalizing Setup", 5, self.finalize_setup)
        ]

        self.step_index = 0
        self.elapsed = 0
        self.total_duration = sum(t for _, t, _ in self.loading_steps)
        self.progress_bar = self.query_one(ProgressBar)
        self.progress_bar.total = self.total_duration
        self.status_widget = self.query_one("#status", Static)

        self.set_step()
        self.timer = self.set_interval(1.0, self.update_progress)

    def get_logo(self) -> str:
        return r"""
    ___   ___ _  
    |_ |\| _// \ 
    |__| |/__\_/ 
        """

    def set_step(self):
        if self.step_index < len(self.loading_steps):
            self.current_step, self.step_duration, self.step_instruction = self.loading_steps[self.step_index]
            self.status_widget.update(f"-> {self.current_step}")
            # Run the step instruction function
            if self.step_instruction:
                self.step_instruction()
        else:
            self.status_widget.update("All systems ready! Launching application...")
            self.set_timer(2.0, self.action_quit)

    def update_progress(self):
        if self.step_index >= len(self.loading_steps):
            return

        self.progress_bar.advance(advance = self.step_duration)
        self.step_index += 1

        
        self.set_step()

    async def on_key(self, event: Key) -> None:
        if event.key == "q":
            await self.action_quit()

    async def action_quit(self) -> None:
        super().exit()
        self.exit()

    # Example step functions you can replace with real logic

    def getConfig(self):
        from customUtils import loadConfig
        self.config = loadConfig("config.json")

    async def startLLM(self):
        from ollamaUtils import model
        self.llm = model(self.config)
        #self.llm.startOllama()
        self.llm.createModel()
        self.llm.loadHistory()

    def loadTTS(self):
        from ttsWrapper import voice
        self.tts = voice(self.config)
        self.tts.clearCache()

    def finalize_setup(self):
        self.loaded = True


class details:
    def __init__(self, tts, llm, config):
        self.tts = tts
        self.llm = llm
        self.config= config

def loadscreen():
    """Main function to run the loading screen app."""
    try:
        L = LoadingScreenApp()
        L.run()
        if L.loaded == True:
            
            L.exit()
            
            return details(L.tts, L.llm, L.config)
        else:
            print("Loading screen did not complete successfully.")
            L.exit()
            exit(1)
    except KeyboardInterrupt:
        print("\n[Interrupted] Exiting cleanly...")
        L.exit()
        return None
