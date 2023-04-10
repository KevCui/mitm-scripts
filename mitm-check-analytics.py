import json
import urllib.parse
from mitmproxy import http
from mitmutils import utils
import logging

DATA_FILE = './check-analytics.yaml'


def check_analytics(keyword, source, format):
    if format == 'form':
        for s in str(source).split("&"):
            if keyword in s:
                logging.warn('MATCH: ' + urllib.parse.unquote(str(s)))

    if format == 'json':
        txt = json.loads(source)
        try:
            logging.warn('MATCH: ' + keyword + '=' + txt[keyword])
        except:
            pass


def check_data(url, data, flow):
    if data is not None:
        for link in data:
            if link in url:
                logging.warn('>> FOUND: ' + str(url))
                for keyword in data[link]:
                    check_analytics(keyword, flow.request.url, 'form')
                    for header, value in flow.request.headers.items():
                        if 'Content-Type' in str(header):
                            if 'form' in str(value):
                                check_analytics(keyword, flow.request.text, 'form')
                            if 'json' in str(value):
                                check_analytics(keyword, flow.request.text, 'json')


def request(flow: http.HTTPFlow) -> None:
    check_data(flow.request.url, utils.readFile(DATA_FILE), flow)
