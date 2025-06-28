import os, subprocess, json, asyncio

# Note : Class for all OS-dependant operations, excluding those made simple by  the cmd.call() function
class cmdUtils:
    def __init__(self):
        self.currentWorkingDirectory = ""
        if os.name == "nt":
            self.osType = "windows"
            self.directorySeperator = "\\"
            import playsound 
        elif os.name == "posix":
            self.osType = "linux"
            self.directorySeperator = "/"

    def play(self, file):
        if self.osType == "windows":
            playsound.playsound(file)
            
        else:
            self.call(f"ffplay {file} -nodisp -autoexit &> /dev/null")

    def call(self, command:str):
        if self.osType  == "windows":
            subprocess.call(command)
        else:
            subprocess.call(command, shell=True)
        
    
    def mkdir(self, directory: str):
        os.system("mkdir " + self.currentWorkingDirectory + directory)

    def cd(self, directory: str):
        if directory == "..":
            return NotImplemented
        elif directory == ".":
            pass
        else:
            self.currentWorkingDirectory = self.currentWorkingDirectory + directory + self.directorySeperator
    
    def rmRecursive(self, directory: str):
        #subprocess.call("rm" , self.currentWorkingDirectory + directory)
        pass
        

    def initializeDirectories(self, structure: list, Verbose: bool = False):
        for i in range(len(structure)):
            for dir in structure[i].split("/"):
                if Verbose:
                    print(dir)
                self.mkdir(dir)
                self.cd(dir)
            self.currentWorkingDirectory = ""


#if __name__ == "__main__":
cmd = cmdUtils()


    

def loadConfig(path: str, section: str):
    with open("./" + path) as f:
            config = json.load(f)[section]
    return config
    


