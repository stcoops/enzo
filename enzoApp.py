from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, TextArea, Select, Button, Footer
from textual.containers import Grid, VerticalScroll, Container
from textual.reactive import reactive
from textual.binding import Binding
import asyncio
from textual import on
from customUtils import cmd


class EnzoApp(App):
    BINDINGS= [
        Binding("ctrl+q", "quit", "Quit Enzo"),
        Binding("ctrl+r", "run_ai_task", "Run AI Task"),
        Binding("ctrl+s","SaveReloadConfig","Save config and Reload")
    ]
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 3fr 7fr;
        grid-rows: 1fr 3fr;
        background: rgb(30, 30, 30);
    }

    #menu-title {
        color: rgb(210, 210, 210);  
        align: center middle;
    }

    #menu {
        border: round rgb(120, 120, 120);
        border-title-align: center;
        margin: 1 0 0 2;
        align: center middle;
    }

    #ai-output {
        border: round rgb(120, 120, 120);
        border-title-align: center;
        margin: 1 2 1 0; /* Margin: top, right, bottom, left */
        row-span: 2;  /* Spans both rows */
        height: 100%;
    }


    #user-input {
        border: round rgb(120, 120, 120);
        border-title-align: center;
        margin: 0 0 1 2;
        
    }

    Select {
        margin: 0;
        color: rgb(210, 210, 210);
        background: rgb(30, 30, 30);
        keyline: double rgb(120, 120, 120);
        

    }

    TextArea {
        background: rgb(30, 30, 30);
        color: rgb(210, 210, 210);
    }
    """

    def __init__(self, tts, llm, config) -> None:
        self.tts = tts
        self.llm = llm
        self.config = config  
        self.aiTotalMessage = ""
        super().__init__()


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

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        pass
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

    

    async def on_exit(self) -> None:
        # Close the TTS aiohttp session
        await self.tts.close()
        #await super().on_exit()  # If App has an async on_exit

    def action_quit(self) -> None:
        """Action to quit the application."""
        # For async cleanup, schedule the coroutine to close tts session
        asyncio.create_task(self.tts.close())
        self.exit()
        super().exit()
        








