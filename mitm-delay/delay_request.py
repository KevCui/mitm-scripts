import os, yaml, re
from mitmproxy import http
from time import sleep
from random import randint

HOME_DIR = './'
CONFIG_FILE = HOME_DIR + 'request.yaml'

def readFile(file):
    """Read file and return json data or dict

    Read file and return all its content as json format or dict

    Arg:
        file: File name, including its path
    """

    if not os.path.isfile(file):
        print("File: " + file + ' not found!')
        sys.exit(1)

    fname, fext = os.path.splitext(file)

    with open(file) as data:
        if fext == ".yaml":
             return yaml.load(data)
        else:
             return json.load(data)

def delay(flow):
    """Delay http flow

    delay flow according to CONFIG_FILE

    Arg:
        flow : http flow
    """

    config = readFile(CONFIG_FILE)
    url = flow.request.url

    for patternURL, timer in config.items():
        delay = randint(min(timer[0], timer[1]), max(timer[0], timer[1]))
        if re.match(patternURL, url) is not None:
            print('--------------------')
            print(str(delay) + 's delay: ' + url)
            sleep(int(delay))

def request(flow: http.HTTPFlow) -> None:
    delay(flow)

def response(flow: http.HTTPFlow) -> None:
    delay(flow)
