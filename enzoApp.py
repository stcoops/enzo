from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup, Center
from textual.screen import Screen
from textual.widgets import Label, Button, ProgressBar, Input, TextArea
from rich.panel import Panel
from textual.events import Event
from textual import on 
from textual.widget import Widget
from rich.progress import Progress
import time
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
            Label("Loading babalabs..", id = "CurrentTask"),
            ProgressBar(total = 10)
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
    #SCREENS = {"LoadingScreen": LoadingScreen, "MainDashboard": DashboardScreen}

    def __init__(self) -> None:
        super().__init__()
        

    def compose(self) -> ComposeResult:
        yield Label("Hello World")
        
    def on_mount(self) -> None:
        self.install_screen(WelcomeScreen(), "WelcomeScreen")
        self.install_screen(LoadingScreen(), "LoadingScreen")
        self.push_screen("LoadingScreen")

"""
MAIN CLASS
"""
class z():
    def __init__(self):
        super().__init__()
        self.app = EnzoApp()
        self.app.run()
        #self.app.switch_screen("LoadingScreen")
        time.sleep(0.5)
        self.Load()
    
    def Load(self) -> None:
        i = 0
        while i != 100:
            time.sleep(0.03)
            i += 1
            self.app.query_one(ProgressBar).advance(1)
        print(i)


if __name__ == "__main__":
    Enzo = z()

