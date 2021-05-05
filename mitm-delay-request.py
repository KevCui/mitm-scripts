from mitmproxy import http
from mitmutils import utils
from mitmproxy.script import concurrent

CONFIG_FILE = './delay-request.yaml'


@concurrent
def request(flow: http.HTTPFlow) -> None:
    utils.delay(flow, CONFIG_FILE)


@concurrent
def response(flow: http.HTTPFlow) -> None:
    utils.delay(flow, CONFIG_FILE)
