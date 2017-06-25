import os
import sys
import json
from mitmproxy import http

# This script is a mitmproxy inline script.
# The purpose of this script is to return mock JSON response for
# certain target URLs.
#
# PRECONDITION:
# 1. mitmproxy installation:
#    http://docs.mitmproxy.org/en/stable/install.html
#
# 2. Client side CA setup:
#    http://docs.mitmproxy.org/en/stable/certinstall.html
#
# HOW TO USE:
# 1. Configure global variables:
#    - HOME_DIR: script directory
#    - DATA_DIR: JSON files directory
#    - ROUTER_JSON: router.json file directory
#
# 2. Run mitmproxy:
#    ~$ mitmdump -s rewrite.py
#
# 3. Quick check setup:
#    http://example.com/pass should return data in test_pass.json
#    http://example.com/fail should return data in test_fail.json
#
# 4. Update routeerjson, pair URL with JSON file, for e.g:
#    ```
#    "http://exmaple.com": "exmaple"
#    ```
#    The response of "http://exmaple.com" will be rewrote by the content
#    in exmaple.json file
#
# 5. Add static JSON file, file example:
#    ```
#    {
#      "status": 200,
#      "header": { ... },
#      "content": ...
#    }
#    ```
#    status:http status code, an INT number
#    header: http response headers
#    content: http response body

HOME_DIR = './'
DATA_DIR = './data/'
ROUTER_JSON = HOME_DIR + 'router.json'

def readJsonFile(file):
    """Read file and return json data

    Read file and return all its content as json format

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        print("File: " + file + ' not found!')
        sys.exit(1)

    with open(file) as data:
        return json.load(data)

def request(flow: http.HTTPFlow) -> None:
    """Mock response

    If URL corresponds to router.json, use matched json file as response
    Link url and json file in router.json

    Arg:
        flow: http flow, fom mitm
    """

    router = readJsonFile(ROUTER_JSON)
    url = flow.request.url

    if url in router:
        jsonfile = DATA_DIR + router[url] + '.json'
        print(url + ' found in router. Send data from "' + jsonfile + '"')

        data = readJsonFile(jsonfile)

        status = int(data['status'])
        try:
            content = json.dumps(data['content'])
        except:
            content = ''
        header = data['header']

        flow.response = http.HTTPResponse.make(status, content, header)
