from textual.app import App, ComposeResult
from load import LoadingScreen

class EnzoApp(App):
    CSS_PATH = "styles.tcss"

    def on_mount(self):
        self.push_screen(LoadingScreen())

if __name__ == "__main__":
    EnzoApp().run()
