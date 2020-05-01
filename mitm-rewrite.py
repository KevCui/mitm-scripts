from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import re
import json

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'rewrite-router.yaml'


def response(flow: http.HTTPFlow) -> None:
    routers = utils.readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, jsonfilename in routers.items():
            if re.match(patternURL, url) is not None:
                jsonfile = DATA_DIR + str(jsonfilename) + '.json'
                ctx.log.warn('>>> FOUND "' + url + '". Send response data from "' + jsonfile + '"')

                data = utils.readFile(jsonfile)

                if data is not None:
                    status = int(data['status'])
                    try:
                        content = json.dumps(data['content'])
                    except:
                        content = ''
                    header = data['header']

                    flow.response = http.HTTPResponse.make(status, content, header)
