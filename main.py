from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar, Select, TextArea, Footer
from textual.containers import Container, Center, VerticalScroll
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.events import Key
from textual import on, work
import asyncio
from customUtils import cmd

class LoadingScreen(Screen):
    CSS_PATH = "load.tcss"

    progress = reactive(0)
    current_step = reactive("")

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.get_logo(), id="logo"))
        yield ProgressBar(show_eta=False, show_percentage=False)
        yield Static("", id="status")


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
        self.timer = self.app.set_interval(1.0, self.update_progress)

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
            return 

    def update_progress(self):
        if self.step_index >= len(self.loading_steps):
            return

        self.progress_bar.advance(advance = self.step_duration)
        self.step_index += 1

        
        self.set_step()

        # Functions to be called during loading steps
    def getConfig(self):
        from customUtils import loadConfig
        self.config = loadConfig("config.json")

    def startLLM(self):
        from ollamaUtils import model
        self.llm = model(self.config)
        self.llm.startOllama()
        self.llm.createModel()
        self.llm.loadHistory()

    def loadTTS(self):
        from ttsWrapper import voice
        self.tts = voice(self.config)
        self.tts.clearCache()

    def finalize_setup(self):
        self.loaded = True
        self.app.install_screen(Dashboard(self.config,self.tts,self.llm), "Dashboard")
        self.dismiss(1)



class Dashboard(Screen):
    CSS_PATH = "main.tcss"
    BINDINGS= [
        Binding("ctrl+q", "quit", "Quit Enzo"),
        Binding("ctrl+r", "run_ai_task", "Run AI Task"),
    ]

    def __init__(self, config, tts, llm):
        super().__init__()
        self.config = config
        self.tts = tts
        self.llm = llm

    def compose(self) -> ComposeResult:
        # Top-left: Menu container
        modelOptions = []
        for i in range(len(self.config["modelsAvailable"])):
            modelOptions.append((self.config["modelsAvailable"][i]["name"], self.config["modelsAvailable"][i]["id"])) #NOTE: corresponds to ["id"] for loading btw

        SelectModel = Select(
                options=modelOptions,
                prompt="Select Model",
                id="model-select",
            )
        
        voiceOptions = []
        for i in range(len(self.config["voicesAvailable"])):
            voiceOptions.append((self.config["voicesAvailable"][i]["name"], self.config["voicesAvailable"][i]["id"]))

        SelectVoice = Select(
            options=voiceOptions,
            prompt="Select TTS Voice:",
            id="voice-select"
            )
        
        menuContainer =  VerticalScroll(SelectModel,
                                        SelectVoice,
                                         id="menu")
        menuContainer.border_title = "Enzo version 1.0.1"
        yield menuContainer
        
        # Bottom-left: AI output area
        AIoutput = Static("AI output will appear here...", id="ai-output")
        AIoutput.border_title = "Enzo says:"
        AIoutput.expand = True
        yield AIoutput

        # Right: User input text area (spans both rows)
        userInput = TextArea("Type your AI prompt here...", id="user-input", name="Input")
        userInput.border_title = "User Input"
        yield userInput
        yield Footer()

    async def action_run_ai_task(self) -> None:
        """Action to run the AI task when the button is pressed."""
        #model_select = self.query_one("#model-select", Select)
        #tts_select = self.query_one("#tts-select", Select)
        self.user_input = self.query_one("#user-input", TextArea)
        self.ai_output = self.query_one("#ai-output", Static)

        #model = model_select.value
        #tts = tts_select.value
        self.llm.question = self.user_input.text
        asyncio.create_task(self.run_ai_task())

    async def run_ai_task(self) -> None:
        """Run the AI task and update the AI output area."""
        self.user_input.text = "Processing your query..."
        await self.llm.startQuery(self.ai_output, self.tts, cmd,)  # Pass the Static widget to update directly
        
        self.user_input.text = "Query sent to AI. Waiting for response..."
        #await self.llm.queryComplete()
        #self.ai_output.update(self.aiTotalMessage)
        #if True:
        asyncio.create_task(self.tts.speak(self.aiTotalMessage))
        asyncio.create_task(cmd.play(self.tts.fileName))

        self.user_input.text = ""  # Clear user input after processing


class mainApp(App):
    """Main application class for the loading screen."""
    CSS_PATH = "main.tcss"

    def on_mount(self) -> None:
        self.install_screen(LoadingScreen(), name="loading")
    
    @work
    async def on_ready(self) -> None:
        if await self.push_screen_wait(LoadingScreen()) == 1:
            self.push_screen("Dashboard")


    async def on_key(self, event: Key) -> None:
        if event.key == "q":
            await self.action_quit()

    async def action_quit(self) -> None:
        self.exit()
        super().exit()
        




if __name__ == "__main__":
    app = mainApp()
    app.run()
