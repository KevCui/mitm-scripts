import os, sys, re, json
from ruamel.yaml import YAML
from mitmproxy import http
from mitmproxy import ctx

HOME_DIR = './'
ROUTER_FILE = HOME_DIR + 'redirect-router.yaml'

def readFile(file):
    """Read file and return json data or dict

    Read file and return all its content as json format or dict

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        ctx.log.error("File: " + file + ' not found!')
        return None

    fname, fext = os.path.splitext(file)

    with open(file) as data:
        if fext == ".yaml":
            yaml = YAML(typ='safe')
            return yaml.load(data)
        else:
            return json.load(data)

def request(flow: http.HTTPFlow) -> None:
    """Mock request

    If URL corresponds to redirect-router.yaml, it will be redirected to other URL difined in redirect-router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, redirectURL in routers.items():
            if re.match(patternURL, url) is not None:
                ctx.log.alert(url + ' found. Redirect it to "' + redirectURL + '"')
                flow.request.host = redirectURL
