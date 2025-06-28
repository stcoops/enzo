import json, asyncio
from customUtils import cmd
import edge_tts

class voice:
    def __init__(self, config):
        self.config = config
        
    async def speak(self, data: str):
        voice = self.config["voice"]
        audioFile = self.config["cacheDirectory"] + "/TTS.mp3"

        textFile = self.config["cacheDirectory"] + "/TTS.txt"
        with open(textFile, "w") as f:
            f.write(data)

        rate = self.config["rate"] - 100#rate increase of voice.
        if rate >= 0:
            ratePrefix = "+"
        else:
            ratePrefix = "-"

        #self.clearCache()
        await edge_tts.Communicate(data, voice, rate = f"{ratePrefix}{str(rate)}%").save(audioFile)
        await cmd.play(audioFile)
        

    def clearCache(self):
        cmd.rmRecursive(self.config["cacheDirectory"])
        cmd.mkdir(self.config["cacheDirectory"])

async def main():
    v = voice("config.json")
    await v.speak("Hello Sam")

if __name__ == "__main__":
    import load
    asyncio.run(main())
    
