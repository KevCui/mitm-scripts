import random
import logging
from mitmproxy import http

percentage = 25


def response(flow: http.HTTPFlow) -> None:
    if random.randint(1, 100) < percentage:
        logging.warn('>>> Down ' + flow.request.url)
        flow.response = http.Response.make(503, '', {})
