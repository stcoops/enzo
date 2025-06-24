from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.screen import Screen
from textual.widgets import Label, Button, ProgressBar, Input
from textual import on 

import time

"""
SCREENS
"""

class LoadingScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
    
    def compose(self) -> ComposeResult:
        with Container(id = "LoadingScreenContainer"):
            yield Label("Loading Screen..", id = "CurrentProcess")
            #yield ProgressBar(total = 100)

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
    #SCREENS
    def compose(self) -> None:
        yield Label("Hello World")
        
    def on_mount(self) -> None:
        self.install_screen(LoadingScreen(), name = "LoadingScreen")
        self.install_screen(DashboardScreen(), name = "DashboardScreen")

        self.push_screen("LoadingScreen")


    def action_startMainDashboard(self) -> None:

        self.switch_screen("DashboardScreen")

"""
MAIN LOOP
"""
class run():

    def main():
        app = EnzoApp()
        app.run()

    __call__ = main()
