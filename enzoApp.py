from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, TextArea, Select, Button
from textual.containers import Grid, Vertical
from textual.reactive import reactive




class EnzoApp(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 30% 70%;
        grid-rows: auto 1fr;
        background: rgb(30, 30, 30);
    }

    #menu {
        border: round rgb(120, 120, 120);
        margin: 1;
        align-horizontal: center;
    }

    #ai-output {
        border: round rgb(120, 120, 120);
        margin: 1;
    }

    #user-input {
        border: round rgb(120, 120, 120);
        margin: 1;
        row-span: 2;  /* Spans both rows */
    }

    Select, Button {
        width: 90%;
        margin: 1 0;
        color: rgb(210, 210, 210);
        background: rgb(30, 30, 30);
        keyline: double rgb(120, 120, 120);
        border: round rgb(120, 120, 120);
    }

    TextArea {
        background: rgb(30, 30, 30);
        color: rgb(210, 210, 210);
    }
    """

    def __init__(self, tts, llm, APPConfig, MODELconfig, TTSconfig) -> None:
        self.tts = tts
        self.llm = llm
        self.APPConfig = APPConfig  
        self.MODELconfig = MODELconfig
        self.TTSconfig = TTSconfig 
        super().__init__()


    def compose(self) -> ComposeResult:
        # Top-left: Menu container
        yield Vertical(
            Static(" Enzo version 1.0.1", id="menu-title"),
            Select(
                options=[("GPT-4o", "gpt-4o"), ("GPT-3.5", "gpt-3.5")],
                prompt="Select Model",
                id="model-select",
            ),
            Select(
                options=[("Voice 1", "voice1"), ("Voice 2", "voice2")],
                prompt="TTS Voice",
                id="tts-select",
            ),
            Button("Run AI Task", id="run-button"),
            id="menu",
        )

        # Right: User input text area (spans both rows)
        yield TextArea("Type your AI prompt here...", id="user-input")

        # Bottom-left: AI output area
        yield TextArea("AI output will appear here...", id="ai-output", read_only=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-button":
            model_select = self.query_one("#model-select", Select)
            tts_select = self.query_one("#tts-select", Select)
            user_input = self.query_one("#user-input", TextArea)
            ai_output = self.query_one("#ai-output", TextArea)

            model = model_select.value
            tts = tts_select.value
            self.llm.question = user_input.text
            
            await self.llm.query()
            if tts:
                await self.tts.speak(self.llm.response)

            ai_output.text = self.llm.response
            #ai_output.update()
    







