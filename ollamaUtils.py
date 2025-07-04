import json, os, time
from ollama import AsyncClient
import asyncio, subprocess, requests, edge_tts, wave, sys, pyaudio, time
from openai.helpers import LocalAudioPlayer
import pygame

class model:
    def __init__(self, config):
        super().__init__()
        self.config = config #type: ignore
        self.question = ""
        self.client = AsyncClient()
        self.query = False

    def startOllama(self) -> None:
        try:
            if self.is_ollama_running():
                print("Ollama server already running.")
                return
            print("Attempting to start Ollama server...")
            subprocess.Popen("ollama serve")
            # Wait for Ollama server to become available
            for i in range(20):
                if self.is_ollama_running():
                    print("Ollama server is running.")
                    subprocess.Popen("ollama run " + self.config["name"])
                    return
                print(f"Waiting for Ollama...{i+1}/20")
                time.sleep(1)
            raise RuntimeError("Ollama server did not start in time.")
        except Exception as e:
            print(f"Failed to start Ollama server: {e}")
            raise

    def is_ollama_running(self):
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            return r.status_code == 200
        except Exception as e:
            # Optionally print error for debugging
            # print(f"Ollama health check failed: {e}")
            return False

    def loadHistory(self) -> bool:      # Also initializes previousMessages + currentMessages (empty)
        try:
            self.previousMessages = []
            directory = [fileName for fileName in os.listdir(self.config["historyDirectory"])]    # type: ignore
            for i in range(len(directory)):
                with open(self.config["historyDirectory"] + "/" + directory[i]) as f:     # type: ignore
                    self.previousMessages += json.load(f)
                print("Previous messages file: " + directory[i] + ".json Loaded successfully.")

            self.currentMessages = []
            return True
        
        except:
            return False
        
    def saveHistory(self):
        with open(self.config["historyDirectory"] + "/" + self.sessionTimestamp + ".json", "w") as f: # type: ignore
            json.dump(self.currentMessages, f)

    def closeConnection(self):
        pass
    def createModel(self):
            self.client.create(
                model = self.config["modelsAvailable"][self.config["modelIndex"]]["id"],           # type: ignore
                from_ = self.config["modelsAvailable"][self.config["modelIndex"]]["id"],    # type: ignore
                system = f"""
                Your Name is: {self.config["name"]}.\n"""      # type: ignore
                + f"""{self.config["context"]} """)    # type: ignore
    
    #async def close(self):
        # Properly close any aiohttp session from AsyncClient
        #await self.client.close()
    
    async def startQuery(self, input, output, tts = None) -> None:
            if self.query == False:
                self.query = True
                self.fullMessage = ""
                self.lastPart = ""
                id = time.strftime("%d%b%Y-%H%M%S")
                audioFile = f"{self.config['cacheDirectory']}/{id}.mp3"
                async for part in await self.client.chat(model = self.config["modelsAvailable"][self.config["modelIndex"]]["id"], messages = [*self.previousMessages,*self.currentMessages,{"role": "user", "content" : self.question}],stream = True):
                        self.fullMessage += part["message"]["content"]
                        self.lastPart = part["message"]["content"]
                            
                        output.update(content = self.fullMessage)
                            


                
                                

                self.currentMessages += [
                        {"role": "user", "content" : self.question},
                        {"role": "assistant", "content" : self.fullMessage}
                    ]
                await self.makeNoise(input)
                
                #async for chunk in edge_tts.Communicate(data, voice, rate = f"{ratePrefix}{str(rate)}%").stream():
                #    if chunk["type"] == "audio" and "data" in chunk:
                #        with open(audioFile, "ab") as self.file:
                #            self.file.write(chunk["data"])

            else:
                pass


    async def makeNoise(self, input):
        """TTS FUNCTIONALITY"""

                #rate = #rate increase of voice.
                
        audioFile = f"{self.config['cacheDirectory']}/{time.strftime('%D%M%Y%a%d')}.mp3"

        rate = self.config["rate"] - 100
        if rate >= 0:
            ratePrefix = "+"
        else:
            ratePrefix = "-"

        with open(f"{self.config['cacheDirectory']}/temp.txt", "w") as f:
            f.write(self.fullMessage)

        voice = self.config["voice"]
        rate = ratePrefix + str(rate) + "%"

        playback = subprocess.Popen(f"edge-playback --file {self.config['cacheDirectory']}/temp.txt --voice {voice} --rate {rate}"
                                    , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = playback.communicate()
        playback.terminate()
            

        input.text = "Chat with Enzo:"
        self.query = False
        return
        