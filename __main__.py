# !/usr/bin/python3
# Description: run in pi, connect web server, and get controlled through ssh reverse
# Run this script:
#   python3 __main__.py --config="./config.json" --loglevel=10
#
import http
import json
import sys
import os
import urllib
import http.client, urllib.parse
from getopt import getopt
import logging
import subprocess


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
        self._configfile = configfile
        with open(configfile) as json_file:
            self._config = json.load(json_file)

        try:
            self._config["nodename"]
        except Exception as e:
            raise Exception("Wrong edge config file: " + configfile)

    def nodename(self):
        return self._config["nodename"]

    def server(self):
        return self._config["server"]

    def port(self):
        return self._config["port"]

    def configfile(self):
        return self._configfile;


def http_post(ip, port, url, opts):
    params = urllib.parse.urlencode(opts)
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/xml"}
    conn = http.client.HTTPConnection(ip, port=port)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    return response

def usage():
    print("")
    print("python3 __main__.py [-h|--help] [--log=logfile] [--loglevel=loglevel] [--config=config]")
    print("")
    print("\tlogfile: default is stdout if not specified. Run as service, normally logfile is /var/log/webapp2pi/log")
    print("")
    print("\tloglevel: default is 30, [CRITICAL:50 ERROR:40 WARNING:30 INFO:20 DEBUG:10]")
    print("")
    print("\tconfig: configfile, default is /etc/webapp2pi/config.json if not specified")
    print("")

def logsetup(logfile, loglevel):
    logger = logging.getLogger("webapp2pi")

    if logfile == None:
        logging.basicConfig(level=loglevel, format="%(asctime)s - %(levelname)s: %(name)s{%(filename)s:%(lineno)s}\t%(message)s")
    else:
        subprocess.run(["mkdir", "-p", os.path.dirname(logfile)])
        handler = logging.FileHandler(logfile)
        logging.basicConfig(level=loglevel)
        handler.setLevel(loglevel)
        formater = logging.Formatter("%(asctime)s - %(levelname)s: %(name)s{%(filename)s:%(lineno)s}\t%(message)s")
        handler.setFormatter(formater)
        logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    #input parameters
    opts, args = getopt(sys.argv[1:], "-h", ["log=", "loglevel=", "config=", "help"])

    logfile = None #default is stdout
    configfile = "/etc/webapp2pi/config.json"
    loglevel = logging.WARNING

    for o, v in opts:
        if o in "-h" or o in "--help":
            usage()
            sys.exit(-1)
        elif o in "--log":
            logfile = v
        elif o in "--loglevel":
            loglevel = int(v)
        elif o in "--config":
            configfile = v

    #check parameters

    #logfile
    print("Setup logger ...logfile", logfile, "loglevel:", loglevel)
    logger = logsetup(logfile, loglevel)

    #configfile
    print("Load config from ", configfile)
    config = Config.getInstance()
    config.loadconfig(configfile)
    # Any more pre-run environment checking can be add here

    try:
        nodename = config.nodename()
    except:
        logger.error("Please specify nodename in config file")
        sys.exit(-1)

    try:
        response = http_post(config.server(), config.port(), "/north/", {"CMD": "poll", "SN": nodename})
        logger.info(response.read().decode())
    except ConnectionRefusedError as e:
        logger.warning(e)
        sys.exit(-1)
    except Exception as e:
        logger.warning(e)
        sys.exit(-1)

    #
    logger.info("End of script")









