from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup, Center
from textual.screen import Screen
from textual.widgets import Label, Button, ProgressBar, Input, TextArea
from rich.panel import Panel
from textual.events import Event
from textual import on 
from textual.widget import Widget
from rich.progress import Progress
import time, asyncio
"""
WIDGETS
"""
class CustomProgressBar(Widget):
    def render(self, percent: int):
        bar = {("#")}
        out = f"[{bar} {percent}%  ]"
        return out

"""
SCREENS
"""

class WelcomeScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Welcome to Enzo version Alpha 1.0.1")
        )

class LoadingScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Loading: "+  NAME, id = "CurrentTask")
        )

class DashboardScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id = "DashboardScreenContainer"):
            yield TextArea("1", id = "LeftTextArea")
            yield Label("2")
            yield Label("3")


"""
MODAL SCREENS
"""
"""
APP CLASS
"""
class EnzoApp(App):
    
    #BINDINGS
    CSS_PATH = "styles.tcss"
    SCREENS = {"LoadingScreen": LoadingScreen, "MainDashboard": DashboardScreen}

    def __init__(self) -> None:
        super().__init__()
        

    def compose(self) -> ComposeResult:
        yield Center(
            VerticalGroup(
                HorizontalGroup(
                    Button("Welcome", id="welcome_button"),
                    Button("Loading", id="loading_button"),
                    Button("Dashboard", id="dashboard_button")
                ),
                Label("Enzo App - Alpha 1.0.1"),
                Label("This is a demo app for Enzo."),
                Label("Click the buttons to navigate.")
            ),
        Label("Hello World"),
        ProgressBar(id="progress_bar", total=100))
        
        
    #def on_mount(self) -> None:
        #self.install_screen(WelcomeScreen(), "WelcomeScreen")
        #self.install_screen(LoadingScreen(), "LoadingScreen")
        #self.push_screen("LoadingScreen")

"""
MAIN CLASS
"""
def main(loop) -> None:
    """Main function to run the EnzoApp."""
    # Create an instance of the EnzoApp and run it.
    # This will initialize the app and display the welcome screen.
    ENZO = EnzoApp()
    ENZO.run(loop=loop)
            #self.app.switch_screen("LoadingScreen")
    time.sleep(0.5)
        
    ENZO.push_screen(LoadingScreen())
    i = 0
    while i != 100:
        time.sleep(0.03)
        i += 1
                
        ENZO.query_one(ProgressBar).update(progress=i, total=100)
        print(i)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        (main(loop=loop))
    except KeyboardInterrupt:
        pass







