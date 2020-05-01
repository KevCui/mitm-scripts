from mitmproxy import http
from mitmproxy import ctx
from mitmutils import utils
import os
import re
import time

CONFIG_FILE = './dump-curl.yaml'


def request(flow: http.HTTPFlow) -> None:
    matches = utils.readFile(CONFIG_FILE)
    url = flow.request.url

    if matches is not None:
        for patternURL, dumpFolder in matches.items():
            if not os.path.exists(dumpFolder):
                os.makedirs(dumpFolder)

            if re.match(patternURL, url) is not None:
                dumpFile = dumpFolder + '/' + str(int(round(time.time() * 1000)))
                ctx.log.info('>>> Dump ' + url + ' to ' + dumpFile)
                ctx.master.commands.call("export.file", 'curl', flow, dumpFile)
