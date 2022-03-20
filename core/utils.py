import os
import json



class Config:
    __instance = None

    @staticmethod
    def getInstance():
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self

    def loadconfig(self, configfile):
        with open(configfile) as json_file:
            self._config = json.load(json_file)

        try:
            self._config["nodeName"]
        except Exception as e:
            raise Exception("node name is not set in " + configfile)

        try:
            self._config["tennantId"]
        except Exception as e:
            raise Exception("tennant id is not set in " + configfile)

        try:
            self._config["tennantApiKey"]
        except Exception as e:
            raise Exception("tennant api key is not set in " + configfile)

        self._configfile = configfile

    def configfile(self):
        return self._configfile;

    def nodeName(self):
        return self._config["nodename"]

    def tennantId(self):
        return self._config["tennantId"]

    def tennantApiKey(self):
        return self._config["tennantApiKey"]



if __name__ == "__main__":
    config = Config.getInstance()
    print("Current working directory: ", os.getcwd())
    config.loadconfig("../config.json")