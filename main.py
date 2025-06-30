from textual.app import App, ComposeResult
from load import loadscreen
import asyncio, gc

def main():
    ld =    loadscreen()
    if ld is None:
        print("Loading screen was interrupted or failed.")
        return
    from enzoApp import EnzoApp
    tts = ld.tts
    llm = ld.llm
    config = ld.config

    
    app = EnzoApp(tts, llm, config)
    app.run()
    


if __name__ == "__main__":
    main()
      # Run garbage collection to clean up resources
    #app = EnzoApp()
    #app.run()
    #print("Enzo App is running.")