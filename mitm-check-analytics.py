import json, urllib.parse
from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils

DATA_FILE = './check-analytics.yaml'

def check_analytics(keyword, source, format):
    """Check and display matched keyword in source

    Arg:
        keyword: str
        source: str
        format: str
    """

    if format is 'form':
        for s in str(source).split("&"):
            if keyword in s:
                ctx.log.warn('MATCH: ' + urllib.parse.unquote(str(s)))

    if format is 'json':
        txt = json.loads(source)
        try:
            ctx.log.warn('MATCH: ' + keyword + '=' + txt[keyword])
        except:
            pass

def check_data(url, data, flow):
    """Check data in request flow

    Arg:
        url: flow url
        data: {link1: [keyword1, keyword2...]}
        flow: http flow, from mitm
    """

    if data is not None:
        for link in data:
            if link in url:
                ctx.log.warn('>> FOUND: ' + str(url))
                for keyword in data[link]:
                    # Check request url
                    check_analytics(keyword, flow.request.url, 'form')

                    for header,value in flow.request.headers.items():
                        if 'Content-Type' in str(header):
                            # Check request body, form format
                            if 'form' in str(value):
                                check_analytics(keyword, flow.request.text, 'form')
                            # Check request body, json format
                            if 'json' in str(value):
                                check_analytics(keyword, flow.request.text, 'json')

def request(flow: http.HTTPFlow) -> None:
    """Show matched analytics keyword and value

    Arg:
        flow: http flow, from mitm
    """

    check_data(flow.request.url, utils.readFile(DATA_FILE), flow)
