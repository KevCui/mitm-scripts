import os, sys, re, json
from ruamel.yaml import YAML
from mitmproxy import http

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'router.yaml'

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
            yaml = YAML(typ='safe')
            return yaml.load(data)
        else:
            return json.load(data)

def response(flow: http.HTTPFlow) -> None:
    """Mock response

    If URL corresponds to router.yaml, use matched yaml file with replacement strings
    Link url and yaml file in router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = readFile(ROUTER_FILE)
    url = flow.request.url

    for patternURL, yamlfilename in routers.items():
        if re.match(patternURL, url) is not None:
            yamlfile = DATA_DIR + str(yamlfilename) + '.yaml'
            print(url + ' found. Replace strings from "' + yamlfile + '"')

            data = readFile(yamlfile)

            for old, new in data.items():
                flow.response.content = flow.response.content.replace(bytes(old.encode('utf8')), bytes(new.encode('utf8')))
