from textual.app import App, ComposeResult
from load import loadscreen
import asyncio

def main():
    ld =    loadscreen()
    if ld is None:
        print("Loading screen was interrupted or failed.")
        return
    tts = ld.tts
    llm = ld.llm
    APPConfig = ld.APPConfig 
    MODELconfig = ld.MODELconfig
    TTSconfig = ld.TTSconfig
    

    from enzoApp import EnzoApp
    app = EnzoApp(tts, llm, APPConfig, MODELconfig, TTSconfig)
    app.run()


if __name__ == "__main__":
    main()
    #app = EnzoApp()
    #app.run()
    #print("Enzo App is running.")