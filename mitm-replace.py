import os, sys, re, json
from ruamel.yaml import YAML
from mitmproxy import http
from mitmproxy import ctx

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'replace-router.yaml'

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

    If URL corresponds to router.yaml, use matched yaml file with replacement strings
    Link url and yaml file in router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, yamlfilename in routers.items():
            if re.match(patternURL, url) is not None:
                yamlfile = DATA_DIR + str(yamlfilename) + '.yaml'
                ctx.log.info(url + ' found. Replace strings from "' + yamlfile + '"')

                data = readFile(yamlfile)

                if data is not None:
                    for old, new in data.items():
                        flow.response.content = flow.response.content.replace(bytes(old.encode('utf8')), bytes(new.encode('utf8')))
