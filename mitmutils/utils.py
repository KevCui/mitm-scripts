import os
import re
import json
import random
from ruamel.yaml import YAML
from mitmproxy import ctx
from time import sleep


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
            yaml = YAML(typ='safe')
            return yaml.load(data)
        else:
            return json.load(data)


def delay(flow, conf):
    """Delay http flow

    delay flow according to conf file

    Arg:
        flow : http flow
    """

    config = readFile(conf)
    url = flow.request.url

    if config is not None:
        for patternURL, timer in config.items():
            delay = round(random.uniform(min(timer[0], timer[1]), max(timer[0], timer[1])), 2)
            if re.match(patternURL, url) is not None:
                sleep(delay)
