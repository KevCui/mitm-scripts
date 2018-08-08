# mitm-script

This is a collection of some handy [mitmproxy](https://github.com/mitmproxy/mitmproxy) inline scripts.

## PRECONDITION:

1. Requirements installation:
```
~$ sudo pip3 install -r requirements.txt
```

2. Client side CA setup: http://docs.mitmproxy.org/en/stable/certinstall.html

---

## mitm-rewrite

The purpose of this script is to return mock JSON response for certain target URLs.

### HOW TO USE:

1. Run mitmdump:
```
~$ cd mitm-rewrite
~$ mitmdump -s rewrite.py
```

2. Quick check setup on client side:
- Open http://example.com/pass should return data in test_pass.json
- Open http://example.com/fail should return data in test_fail.json

3. Update router.json, pair URL with JSON file, for e.g:
```
http://example.com: example
```
The response of "http://exmaple.com" will be rewrote by the content
in example.json file. Using yaml file is easy for human to read and
it's possible to add comment in yaml.

4. Add static JSON file, file example:
```
{
  "status": 200,
  "header": { ... },
  "content": ...
}
```

- status: http status code, an INT number
- header: http response headers
- content: response body

The changes in yaml files will be applied **on the fly**, no need to restart proxy. Here is an example how it looks like:

![mitm-rewrite-example](screenshot/mitm-rewrite-example.jpg)

---

## mitm-check-analytics

The usage of this script is to display real-time analytics key and value, in order to help checking analytics efficiently.

To configure URL and keywords, edit `analytics.yaml`
It's possible to configure the url and

### HOW TO USE:

1. Run mitmdump:
```
~$ cd mitm-check-analytics
~$ mitmdump -s check_analytics.py
```

2. Visit target web page in clients: browsers or apps. The matched analytics keyword and value will show up in terminal.

---

## mitm-delay

This script will randomly delay HTTP/HTTPS request time and response time, in order to simulate the slow network.

To configure URL and delay time, edit `request.yaml`

### HOW TO USE:

```
~$ cd mitm-delay
~$ mitmdump -s delay-request.py
```

---

## mitm-replace

This scrip will replace the specific string to another on. Like *mitm-rewrite*, a `router.json` is used to link URL and yaml file in `response` folder. In the yaml file, the old and new strings can be defined. Don't forget to uncomment URLs in `router.json` and make it work on the fly! 

### HOW TO USE:

```
~$ cd mitm-replace
~$ mitmdump -s mitm-replace.py
```
