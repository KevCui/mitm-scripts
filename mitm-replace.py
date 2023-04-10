from mitmproxy import http
from mitmutils import utils
import re
import logging

HOME_DIR = './'
DATA_DIR = HOME_DIR + 'response/'
ROUTER_FILE = HOME_DIR + 'replace-router.yaml'


def response(flow: http.HTTPFlow) -> None:
    routers = utils.readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, yamlfilename in routers.items():
            if re.match(patternURL, url) is not None:
                yamlfile = DATA_DIR + str(yamlfilename) + '.yaml'
                logging.info('>>> FOUND "' + url + '" to replace strings from "' + yamlfile + '"')

                data = utils.readFile(yamlfile)
                logging.info(data)

                if data is not None:
                    for old, new in data.items():
                        flow.response.content = flow.response.content.replace(bytes(old.encode('utf8')), bytes(new.encode('utf8')))
