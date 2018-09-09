from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import re

ROUTER_FILE = './redirect-router.yaml'

def request(flow: http.HTTPFlow) -> None:
    """Mock request

    If URL corresponds to redirect-router.yaml, it will be redirected to other URL difined in redirect-router.yaml

    Arg:
        flow: http flow, from mitm
    """

    routers = utils.readFile(ROUTER_FILE)
    url = flow.request.url

    if routers is not None:
        for patternURL, redirectURL in routers.items():
            if re.match(patternURL, url) is not None:
                ctx.log.alert(url + ' found. Redirect it to "' + redirectURL + '"')
                flow.request.host = redirectURL
