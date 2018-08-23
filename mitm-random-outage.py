import random
from mitmproxy import http
from mitmproxy import ctx

percentage=25

def response(flow: http.HTTPFlow) -> None:
    if random.randint(1,100) < percentage:
        ctx.log.warn('Down ' + flow.request.url)
        flow.response = http.HTTPResponse.make(503, '', {})
