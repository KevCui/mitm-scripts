from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import re


CONFIG_FILE = './kill-request.yaml'


def request(flow: http.HTTPFlow) -> None:
    config = utils.readFile(CONFIG_FILE)
    method = flow.request.method
    url = flow.request.url

    if config is not None:
        for matchMethod in config:
            if matchMethod == method:
                for patternURL in config[matchMethod]:
                    if re.match(patternURL, url) is not None:
                        ctx.log.warn('>>> FOUND request to kill: ' + method + ' ' + url)
                        flow.kill()
