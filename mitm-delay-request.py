from mitmproxy import http
from mitmutils import utils

CONFIG_FILE = './delay-request.yaml'


def request(flow: http.HTTPFlow) -> None:
    utils.delay(flow, CONFIG_FILE)


def response(flow: http.HTTPFlow) -> None:
    utils.delay(flow, CONFIG_FILE)
