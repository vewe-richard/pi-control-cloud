import urllib
import http.client, urllib.parse
import http
import json

class Apis:
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        pass

    def CheckNodeName(self):
        url = "/api/v1/tennant/devices/setup/checkNodeName"
        resp = self.http_post(url, {"nodeName": self._config.nodeName()})
        code = resp.getcode()
        self._logger.info("response code: " + str(code))
        if code == 200:
            content = self.parse_response(resp.read().decode())
            return [content["isAvailable"], content["message"]]
        elif code == 404:
            return [False, url + " is not exist"]
        elif code == 403:
            #TODO, need parse error message from response
            return [False, "no tennant id or tennant api key were provided or the provided values were invalid."]
        else:
            return [False, "Unknow http response code " + code]

    def AddNewDevice(self, authKey, bluetoothName = ""):
        url = "/api/v1/tennant/devices/setup/add"
        resp = self.http_post(url, {"nodeName": self._config.nodeName(), "authKey": authKey, "bluetoothName": bluetoothName})
        code = resp.getcode()
        self._logger.info("response code: " + str(code))
        if code == 200:
            content = self.parse_response(resp.read().decode())
            self._logger.info(content)
            return [True, content["deviceId"], content["message"]]
        elif code == 404:
            return [False, url + " is not exist"]
        elif code == 400:
            # TODO, need parse error message from response
            return [False, "the node name already exists"]
        elif code == 403:
            #TODO, need parse error message from response
            return [False, "no tennant id or tennant api key were provided or the provided values were invalid."]
        else:
            return [False, "Unknow http response code " + code]

    def DeleteDevice(self):
        url = "/api/v1/tennant/devices/setup/delete/" + self._config.nodeName()
        resp = self.http_post(url, {"nodeName": self._config.nodeName()})
        code = resp.getcode()
        if code == 200:
            content = self.parse_response(resp.read().decode())
            self._logger.info(content)
            return [True, content["message"]]
        elif code == 404:
            return [False, url + " is not exist"]
        elif code == 403:
            #TODO, need parse error message from response
            return [False, "no tennant id or tennant api key were provided or the provided values were invalid."]
        else:
            return [False, "Unknow http response code " + code]

    def http_post(self, url, opts):
        if self._config.debug():
            debugurl = "/north/"
            opts["CMD"] = "poll"
            opts["SN"] = "00090002"
            self._logger.warn("Debug on, change url from " + url + " to " + debugurl)
            self._logger.warn("Debug on, parameters " + str(opts))
            url = debugurl
        params = urllib.parse.urlencode(opts)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/xml",
                   "x-tennant-id": self._config.tennantId(),
                   "x-tennant-apiKey": self._config.tennantApiKey()
                   }
        conn = http.client.HTTPConnection(self._config.webServer(), port=self._config.serverPort())
        conn.request("POST", url, params, headers)
        response = conn.getresponse()
        return response

    def parse_response(self, resp):
        self._logger.info("parse_response: " + resp)
        if self._config.debug():
            resp = '''{"isAvailable": true, 
                    "message": "message from debug",
                    "deviceId": "1234567890"
                    }'''


        return json.loads(resp)

if __name__ == "__main__":
    import utils
    import logging

    logger = logging.getLogger("webapp2pi")
    logging.basicConfig(level=10, format="%(asctime)s - %(levelname)s: %(name)s{%(filename)s:%(lineno)s}\t%(message)s")

    config = utils.Config.getInstance()
    config.loadconfig("../config.json")
    apis = Apis(config, logger)
    result = apis.CheckNodeName()
    logger.info("CheckNodeName: " + str(result))

    authKey = '''ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCyXKTfYOOUITCcq84xEVv8d3G3WHwR4tE+vjEezcABqzX/sRcPidYY+6ZmErIp\
JtKLoxX94BRKgr0y0AA9knRCAVwakr3fpt04K8z6SAECL+eJGZtdF4Bz/6PNN+rZmNu7pZepEGkONHWaQ8US/+7ge/mTXir8JStW\
SrkabNmEtY8G8xJWfDCXvzJLY/qpMiPH438mZrBRc+t8+4gJOn6ETmOg5GyMRlhquV6VaLEZUfNO5rUktnVfMXyx64ZwrM0vrbSt\
FFqw7SIrC+GORd7IXzlxjaxcK2gUuED//vxVKWpvdzyq+kOr78wT8cDiK5Wh1LEQgbVRXDlN3GuUJyz3 richard@richard-NH5\
0-70RA'''

    result = apis.AddNewDevice(authKey)

    logger.info(result)
    pass