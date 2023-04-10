from mitmproxy import http
from mitmutils import utils
import re
import logging

CONFIG_FILE = './show-header.yaml'


def searchHeaders(flow, config, state):
    config = utils.readFile(config)
    url = flow.request.url

    if config is not None:
        for patternURL, headers in config.items():
            if re.match(patternURL, url) is not None:

                if state == 'request':
                    items = flow.request.headers.items()
                else:
                    items = flow.response.headers.items()

                logging.warn('>> FOUND ' + state + ' header in: ' + url)
                for k, v in items:
                    if k.lower() in [x.lower() for x in headers]:
                        logging.warn('-> ' + str(k) + ': ' + str(v))


def request(flow: http.HTTPFlow) -> None:
    searchHeaders(flow, CONFIG_FILE, 'request')


def response(flow: http.HTTPFlow) -> None:
    searchHeaders(flow, CONFIG_FILE, 'response')
