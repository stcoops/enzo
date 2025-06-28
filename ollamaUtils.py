import json, os, time
import customUtils as utils
from ollama import AsyncClient
import asyncio, subprocess, requests
class model:
    def __init__(self, config):
        self.config = config
        self.question = ""
        
    def startOllama(self) -> None:
        try:
            if self.is_ollama_running():
                print("Ollama server already running.")
                return
            print("Attempting to start Ollama server...")
            subprocess.Popen(["ollama", "serve"])
            # Wait for Ollama server to become available
            for i in range(20):
                if self.is_ollama_running():
                    print("Ollama server is running.")
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
            directory = [name for name in os.listdir(self.config["historyDirectory"])]    # type: ignore
            for i in range(len(directory)):
                with open(self.config["historyDirectory"] + "/" + directory[i]) as f:     # type: ignore
                    self.previousMessages += json.load(f)
                print("Previous messages file: " + directory[i] + ".json Loaded successfully.")

            self.currentMessages = []
            return True
        
        except:
            return False
        
    def saveHistory(self):
        try:
            with open(self.config["historyDirectory"] + "/" + self.sessionTimestamp + ".json", "w") as f: # type: ignore
                json.dump(self.currentMessages, f)
        except:
            pass

    def createModel(self) -> bool:
        try:
            AsyncClient().create(
                model=self.config["name"],           # type: ignore
                from_ = self.config["modelName"],    # type: ignore
                system = f"""
                You are {self.config["name"]}."""      # type: ignore
                + f"""{self.config["context"]} """)    # type: ignore

            return True
        except:
            return False
    
    
    
    async def query(self) -> str:
            response = await AsyncClient().chat(
                model = self.config["name"],     # type: ignore
                messages = [
                    *self.previousMessages,
                    *self.currentMessages,
                    {"role": "user", "content" : self.question}
                    ]
                )
            self.currentMessages += [
                {"role": "user", "content" : self.question},
                {"role": "assistant", "content" : response.message.content}
            ]
            self.response = response.message.content
            return self.response
