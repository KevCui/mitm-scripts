import os
import sys
import json
import yaml
import urllib.parse
from mitmproxy import http

HOME_DIR = '.'
YAML_DIR = HOME_DIR + '/yaml/'
DATA_FILE = YAML_DIR + 'analytics.yaml'

def readFile(file):
    """Read file and return json data or dict

    Read file and return all its content as json format or dict

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        print("File: " + file + ' not found!')
        sys.exit(1)

    fname, fext = os.path.splitext(file)

    with open(file) as data:
        if fext == ".yaml":
            return yaml.load(data)
        else:
            return json.load(data)

def check_analytics(keyword, source):
    """Check and display matched keyword in source

    Arg:
        keyword: str
        source: str
    """

    for s in str(source).split("&"):
        if keyword in s:
            print('MATCH: ' + urllib.parse.unquote(str(s)))

def check_data(url, data, flow):
    """Check data in request flow

    Arg:
        url: flow url
        data: {link1: [keyword1, keyword2...]}
        flow: http flow, fom mitm
    """
    for link in data:
        if link in url:
            print('>> FOUND: ' + str(link))
            for keyword in data[link]:
                # Check request url
                check_analytics(keyword, flow.request.url)

                # Check request body
                check_analytics(keyword, flow.request.text)

def request(flow: http.HTTPFlow) -> None:
    """Show matched analytics keyword and value

    Arg:
        flow: http flow, fom mitm
    """

    check_data(flow.request.url, readFile(DATA_FILE), flow)
