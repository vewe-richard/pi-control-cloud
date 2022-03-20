# !/usr/bin/python3
# Description: run in raspberry pi, connect web server, then get controlled through ssh reverse
# Run this script:
#   PYTHONPATH=${PWD} python3 __main__.py setup --config="./config.json" --loglevel=10
#
import sys
import os
from getopt import getopt
import logging
import subprocess
from core.utils import Config
from core.apis import Apis

def usage():
    print("")
    print("python3 __main__.py cmd [-h|--help] [--log=logfile] [--loglevel=loglevel] [--config=config]")
    print("")
    print("\tcmd:\t\tsetup | update | delete")
    print("")
    print("\tlogfile:\tDefault is stdout if not specified. \n\t\t\tIf running as a service, logfile is /var/log/webapp2pi/log")
    print("")
    print("\tloglevel:\tDefault is 20, [CRITICAL:50 ERROR:40 WARNING:30 INFO:20 DEBUG:10]")
    print("")
    print("\tconfig:\t\tDefault is /etc/webapp2pi/config.json")
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
    cmd = sys.argv[1]

    if cmd not in ["setup", "update", "delete"]:
        print("\nUnknow command")
        usage()
        sys.exit(-1)

    #input parameters
    opts, args = getopt(sys.argv[2:], "-h", ["log=", "loglevel=", "config=", "help"])

    logfile = None #default is stdout
    configfile = "/etc/webapp2pi/config.json"
    loglevel = logging.INFO

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

    #logfile
    print("Setup logger ...logfile", logfile, "loglevel:", loglevel)
    logger = logsetup(logfile, loglevel)

    #configfile
    logger.info("Load config from " + configfile)
    config = Config.getInstance()
    config.loadconfig(configfile)
    # Any more pre-run environment checking can be add here

    apis = Apis(config, logger)

    if cmd == "setup":
        result = apis.CheckNodeName()
        if result[0]:
            logger.info("Node Name " + config.nodeName() + " is usable")
        else:
            logger.info("NOde Name " + config.nodeName() + " can not be use, " + result[1])
            sys.exit(-1)

        authKey = 'ssh-rsa ... todo'  #TODO
        result = apis.AddNewDevice(authKey)
        if result[0]:
            logger.info("Add Device " + config.nodeName() + " Done")
        else:
            logger.info("Add Device " + config.nodeName() + " failed, " + result[1])
            sys.exit(-1)
        pass
    elif cmd == "update":
        pass
    elif cmd == "delete":
        result = apis.DeleteDevice()
        if result[0]:
            logger.info("Delete " + config.nodeName())
        else:
            logger.info("Fail to delete " + config.nodeName(), result[1])
    #
    logger.info("End of script")









