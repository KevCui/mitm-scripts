from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import re, json

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'rewrite-router.yaml'

def response(flow: http.HTTPFlow) -> None:
    """Mock response

    If URL corresponds to router.yaml, use matched json file as response
    Link url and json file in router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = utils.readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, jsonfilename in routers.items():
            if re.match(patternURL, url) is not None:
                jsonfile = DATA_DIR + str(jsonfilename) + '.json'
                ctx.log.info(url + ' found. Send data from "' + jsonfile + '"')

                data = utils.readFile(jsonfile)

                if data is not None:
                    status = int(data['status'])
                    try:
                        content = json.dumps(data['content'])
                    except:
                        content = ''
                    header = data['header']

                    flow.response = http.HTTPResponse.make(status, content, header)
