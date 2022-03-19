import http.client, urllib.parse

def http_post(ip, port, url, opts):
    params = urllib.parse.urlencode(opts)
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/xml"}
    conn = http.client.HTTPConnection(ip, port=port)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    return response


if __name__ == "__main__":
    print("Main Entry")
    resp = http_post("192.168.100.168", 8080, "/north/", {"CMD": "poll", "SN": "00090002"})
    xmlstr = resp.read().decode()
    print("edge polling get response", xmlstr)