import os, sys, json, urllib.parse
from ruamel.yaml import YAML
from mitmproxy import http
from mitmproxy import ctx

DATA_FILE = './analytics.yaml'

def readFile(file):
    """Read file and return json data or dict

    Read file and return all its content as json format or dict

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        ctx.log.error("File: " + file + ' not found!')
        return None

    fname, fext = os.path.splitext(file)

    with open(file) as data:
        if fext == ".yaml":
            yaml = YAML(typ="safe")
            return yaml.load(data)
        else:
            return json.load(data)

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

    check_data(flow.request.url, readFile(DATA_FILE), flow)
