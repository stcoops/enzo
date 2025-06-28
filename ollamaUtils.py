import json, os, time
import customUtils as utils
from ollama import AsyncClient
import asyncio
class model:
    def __init__(self, config):
        self.config = config
        self.question = ""
        


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
    
    
    
    async def query(self):
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
