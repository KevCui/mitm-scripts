import os, sys, re, json
from ruamel.yaml import YAML
from mitmproxy import http
from mitmproxy import ctx

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'rewrite-router.yaml'

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

def response(flow: http.HTTPFlow) -> None:
    """Mock response

    If URL corresponds to router.yaml, use matched json file as response
    Link url and json file in router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, jsonfilename in routers.items():
            if re.match(patternURL, url) is not None:
                jsonfile = DATA_DIR + str(jsonfilename) + '.json'
                ctx.log.info(url + ' found. Send data from "' + jsonfile + '"')

                data = readFile(jsonfile)

                if data is not None:
                    status = int(data['status'])
                    try:
                        content = json.dumps(data['content'])
                    except:
                        content = ''
                    header = data['header']

                    flow.response = http.HTTPResponse.make(status, content, header)
