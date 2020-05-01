from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import re

ROUTER_FILE = './redirect-request.yaml'


def request(flow: http.HTTPFlow) -> None:
    routers = utils.readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, redirectURL in routers.items():
            if re.match(patternURL, url) is not None:
                ctx.log.alert(url + '>>> FOUND url "' + url + '" to redirect host: ' + redirectURL)
                flow.request.host = redirectURL
