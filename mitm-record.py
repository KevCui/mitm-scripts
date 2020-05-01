from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import os
import re
import time

CONFIG_FILE = './record-request.yaml'


def response(flow: http.HTTPFlow) -> None:
    matches = utils.readFile(CONFIG_FILE)
    url = flow.request.url

    if matches is not None:
        for patternURL, dumpFolder in matches.items():
            if not os.path.exists(dumpFolder):
                os.makedirs(dumpFolder)

            if re.match(patternURL, url) is not None:
                dumpFile = dumpFolder + '/' + str(int(round(time.time() * 1000)))

                ctx.log.info('>>> Save ' + url + ' request details to ' + dumpFile)
                with open(dumpFile, 'a') as f:
                    f.write(str(flow.request.method) + ' ' + str(flow.request.url) + '\n')
                    for k, v in flow.request.headers.items():
                        f.write(str(k) + ': ' + str(v) + '\n')
                    f.write('\n' + str(flow.request.content.decode('utf-8')) + '\n')
                    f.write('---\n')
                    for k, v in flow.response.headers.items():
                        f.write(str(k) + ': ' + str(v) + '\n')
                    f.write('\n' + str(flow.response.content.decode('utf-8')) + '\n')
