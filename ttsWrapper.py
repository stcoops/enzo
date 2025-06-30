import json, asyncio
from customUtils import cmd
import edge_tts, aiohttp

class voice:
    def __init__(self, config):
        super().__init__()
        self.config = config #type: ignore
        self.session = aiohttp.ClientSession()
        
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
        
    async def close(self):
        # Properly close the aiohttp session
        if not self.session.closed:
            self.clearCache()
            await self.session.close()

    def clearCache(self):
        cmd.rmRecursive(self.config["cacheDirectory"])
        cmd.mkdir(self.config["cacheDirectory"])

