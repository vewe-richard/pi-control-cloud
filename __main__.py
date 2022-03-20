# !/usr/bin/python3
# Description: run in pi, connect web server, and get controlled through ssh reverse
# Run this script:
#   python3 __main__.py --config="./config.json" --loglevel=10
#
import http
import sys
import os
import urllib
import http.client, urllib.parse
from getopt import getopt
import logging
import subprocess
import xml.etree.ElementTree as ET





def http_post(ip, port, url, opts):
    params = urllib.parse.urlencode(opts)
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/xml"}
    conn = http.client.HTTPConnection(ip, port=port)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    return response

def parse_response(resp):
    logger.info("http post response: " + resp)
    root = ET.fromstring(resp)
    content = dict()
    for x in root:
        if x.tag == "head":
            content["version"] = x.attrib["version"]
            content["sn"] = x.attrib["sn"]
            content["actionid"] = x.attrib["actionid"]
            content["atype"] = x.attrib["actiontype"]
        elif x.tag == "subprocess":
            params = dict()
            for y in x:
                if y.tag == "args":
                    params[y.tag] = json.loads(y.text)
                else:
                    params[y.tag] = y.text
            content["subprocess"] = params
    return content

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
        # check if name is unique on WebApp
        response = http_post(config.server(), config.port(), "/north/", {"CMD": "poll", "SN": nodename})
        content = parse_response(response.read().decode())
        logger.info(str(content))
        # check result and avaliable port
        if content["sn"] != nodename:  #Name is used
            raise Exception("nodename is occupied")
        port = content["actionid"]
    except ConnectionRefusedError as e:
        logger.warning(e)
        sys.exit(-1)
    except Exception as e:
        logger.warning(e)
        sys.exit(-1)



    logger.info("port: " + port)

    #
    logger.info("End of script")









