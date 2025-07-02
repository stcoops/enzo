import json, asyncio
from customUtils import cmd
import edge_tts, aiohttp
import pyaudio

class voice:
    def __init__(self, config):
        super().__init__()
        self.config = config #type: ignore
        self.session = aiohttp.ClientSession()
        self.Queue = []  # Initialize an empty queue
        

    async def addToQueue(self, fileName: str):
        """Add a file to the queue."""
        self.Queue.append(fileName)
    
    async def startprocessQueue(self):
        self.runQueue = True  # Flag to indicate the queue is running
        """Process the queue by playing each file in order."""
        while self.runQueue: 
            if not self.Queue:  # If the queue is empty, wait for a while before checking again
                await asyncio.sleep(1)
                continue

            fileName = self.Queue.pop()
            


    async def speak(self, data: str):
        if self.speaking:
            self.txtfile.write
        voice = self.config["voice"]
        audioFile = self.config["cacheDirectory"] + "/TTS.mp3"
        self.fileName = audioFile
        textFile = self.config["cacheDirectory"] + "/TTS.txt"
        with open(textFile, "w") as f:
            f.write(data)

        rate = self.config["rate"] - 100#rate increase of voice.
        if rate >= 0:
            ratePrefix = "+"
        else:
            ratePrefix = "-"

        #self.clearCache()
        # Ensure the audio file is empty before writing
        async for chunk in edge_tts.Communicate(data, voice, rate = f"{ratePrefix}{str(rate)}%").stream():
            if chunk["type"] == "audio" and "data" in chunk:
                with open(audioFile, "ab") as self.file:
                    self.file.write(chunk["data"])

        return audioFile
        
    async def close(self):
        # Properly close the aiohttp session
        if not self.session.closed:
            self.clearCache()
            await self.session.close()

    def clearCache(self):
        cmd.rmRecursive(self.config["cacheDirectory"])
        cmd.mkdir(self.config["cacheDirectory"])

    async def play(self, data: str):
        voice = self.config["voice"]
        rate = self.config["rate"] - 100
        if rate >= 0:
            ratePrefix = "+"
        else:
            ratePrefix = "-"
        
    

        communicate = edge_tts.Communicate(data, voice, rate = f"{ratePrefix}{str(rate)}%")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])        

