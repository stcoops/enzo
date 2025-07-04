from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar, Select, TextArea, Footer
from textual.containers import Container, Center, VerticalScroll
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.events import Key
from textual import on, work
import asyncio, json



class LoadingScreen(Screen):
    CSS_PATH = "load.tcss"

    progress = reactive(0)
    current_step = reactive("")

    def compose(self) -> ComposeResult:
        """Interesting workarounds for a broken progress bar on screens?"""
        self.logo_static = (Static(self.get_logo(), id="logo"))
        self.progress_bar = (ProgressBar(show_eta=False, show_percentage=False))
        self.status_widget = (Static("", id="status"))
        self.center_container = Container(self.logo_static, Center(self.progress_bar), self.status_widget, id="content")
    
        yield self.center_container


    def on_mount(self) -> None:
        # Now self is available — safe to assign functions
        self.loading_steps = [
            ("Starting Setup", 10, None),
            ("Loading Configuration Files", 15, self.getConfig),
            ("Establishing Model Connection", 10, self.startLLM),
            ("Starting Text-to-Speech Service", 5, self.loadTTS),
            ("Finalizing Setup", 5, self.finalize_setup)
        ]

        self.step_index = 0
        self.elapsed = 0
        self.total_duration = sum(t for _, t, _ in self.loading_steps)
        self.progress_bar = self.query_one(ProgressBar)
        self.progress_bar.total = self.total_duration
        self.status_widget = self.query_one("#status", Static)

        self.set_step()
        self.timer = self.app.set_interval(0.5, self.update_progress)

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
        with open("config.json") as f:
            self.config = json.load(f)

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
        self.app.install_screen(Dashboard(self.config,self.tts,self.llm), "Dashboard")
        self.dismiss(1)



class Dashboard(Screen):
    CSS_PATH = "main.tcss"
    BINDINGS= [
        Binding("ctrl+r", "run_ai_task", "Run AI Task"),
        
    ]

    def __init__(self, config, tts, llm):
        super().__init__()
        self.config = config
        if tts:
            self.tts = tts
        else: 
            self.ttsEnabled = False
            self.tts = None
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
        self.run_ai_task()
        self.user_input.text = "Query sent to AI. Waiting for response..."
        self.user_input.text = ""  # Clear user input after processing

    @work(exclusive=True)
    async def run_ai_task(self) -> None:
        """Run the AI task and update the AI output area."""
        self.user_input.text = "Processing your query..."
        await self.llm.startQuery(self.user_input ,self.ai_output)  # Pass the Static widget to update directly
        
        

    async def on_exit(self) -> None:
        await self.llm.saveHistory()
        self.llm.closeConnection()


class mainApp(App):

    BINDINGS = [Binding("ctrl+q", "quit", "Quit Enzo")]

    def on_mount(self) -> None:
        self.loaded = False
        self.install_screen(LoadingScreen(), name="loading")
    
    @work
    async def on_ready(self) -> None:
        if await self.push_screen_wait(LoadingScreen()) == 1:
            self.loaded = True
            self.push_screen("Dashboard")


    async def on_key(self, event: Key) -> None:
        if event.key == "q":
            await self.action_quit()

    async def action_quit(self) -> None:           



        self.exit()
        super().exit()
        




if __name__ == "__main__":
    import os
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = mainApp()
    app.run()
