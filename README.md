# mitm-script

This is a collection of some handy [mitmproxy](https://github.com/mitmproxy/mitmproxy) inline scripts.

## PRECONDITION:

1. Install [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/)

2. Client side CA setup: http://docs.mitmproxy.org/en/stable/certinstall.html

---

## LIST OF SCRIPTS:

- [mitm-rewrite](#mitm-rewrite): ./mitm-rewrite.py, ./rewrite-router.yaml
- [mitm-replace](#mitm-replace): ./mitm-replace.py, ./replace-router.yaml
- [mitm-redirect-host](#mitm-redirect-host): ./mitm-redirect-host.py, ./redirect-router.yaml
- [mitm-redirect-url](#mitm-redirect-url): ./mitm-redirect-url.py, ./redirect-router.yaml
- [mitm-delay-request](#mitm-delay-request): ./mitm-delay-request.py, ./delay-request.yaml
- [mitm-kill-request](#mitm-kill-request): ./mitm-kill-request.py, ./kill-request.yaml
- [mitm-show-header](#mitm-show-header): ./mitm-show-header.py, ./show-header.yaml
- [mitm-check-analytics](#mitm-check-analytics): ./mitm-check-analytics.py, ./check-analytics.yaml
- [mitm-dump-curl](#mitm-dump-curl): ./mitm-dump-curl.py, ./dump-curl.yaml
- [mitm-record](#mitm-record): ./mitm-record.py, ./record-request.yaml
- [mitm-random-outage](#mitm-random-outage): ./mitm-random-outage.py

All the scripts above can be used with `mitmproxy` and `mitmdump` command:

```bash
~$ mitmproxy -s <script-name>.py
```

OR

```bash
~$ mitmdump -s <script-name>.py
```

### mitm-rewrite

`./mitm-rewrite.py` can return mock JSON response for certain target URLs.

1. Run `mitmdump`:

```bash
~$ mitmdump -s mitm-rewrite.py
```

2. Quick check setup on client side:
- Open http://example.com/pass should return data in test_pass.json
- Open http://example.com/fail should return data in test_fail.json

3. Update `rewrite-router.yaml`, pair URL with JSON file, for e.g:

```
http://example.com: example
```

The response of "http://exmaple.com" will be rewrote by the content
in example.json file. Using yaml file is easy for human to read and
it's possible to add comment in yaml.

4. Add static JSON file, file example:

```json
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

**[`^        back to top        ^`](#)**

---

### mitm-replace

`./mitm-replace.py` can replace the specific string to another one. `replace-router.yaml` is used to link URL and yaml file in `response` folder. In the yaml file, the matching string and result strings can be defined as a pair. Don't forget to uncomment URLs in `replace-router.yaml` and make it work on the fly!

```
~$ mitmdump -s mitm-replace.py
```

**[`^        back to top        ^`](#)**

---

### mitm-redirect-host

`./mitm-redirect-host.py` can redirect the request **host** of URL request to another host. The matching URL and redirect host can be defined in `redirect-router.yaml`. Attention: only the host part of request URL will be replaced.

```bash
~$ mitmdump -s mitm-redirect-host.py
```

**[`^        back to top        ^`](#)**

---

### mitm-redirect-url

`./mitm-redirect-url.py` can redirect the whole request to another URL. The matching URL and redirect URL can be defined in `redirect-router.yaml`.

```bash
~$ mitmdump -s mitm-redirect-url.py
```

**[`^        back to top        ^`](#)**

---

### mitm-delay-request

`./mitm-delay-request.py` can delay HTTP/HTTPS request time and response time, in order to simulate the slow network. To configure matching URL and delay time, edit `delay-request.yaml`.

```bash
~$ mitmdump -s mitm-delay-request.py
```

**[`^        back to top        ^`](#)**

---

### mitm-kill-request

`./mitm-kill-request.py` can kill all matching requests. The matching request methods and URls can be defined in `kill-request.yaml`.

```bash
~$ mitmdump -s mitm-kill-request.py
```

**[`^        back to top        ^`](#)**

---

### mitm-show-header

`./mitm-show-header.py` can print out matched request header and response header, with its value. The matching URL and header can be defined in `show-header.yaml`.

```bash
~$ mitmdump -s mitm-show-header.py | grep '>>\|->'
```

**[`^        back to top        ^`](#)**

---

### mitm-check-analytics

`./mitm-check-analytics.py` can display real-time analytics key and value, in order to help checking analytics efficiently. To configure URL and keywords, edit `check-analytics.yaml`.

1. Run mitmdump:

```bash
~$ mitmdump -s mitm-check_analytics.py
```

2. Visit target web page in clients: browsers or apps. The matched analytics keyword and value will show up in terminal.

**[`^        back to top        ^`](#)**

---

### mitm-dump-curl

`./mitm-dump-curl` can find matching request URL and dump the request to a file in as cURL format. The matching URL and dump folder can be defined in `dump-curl.yaml`.

```bash
~$ mitmdump -s mitm-dump-curl.py
```

**[`^        back to top        ^`](#)**

---

### mitm-record

`./mitm-record.py` can save matching request details (request headers, request body, response headers and response body) to a specific file. The matching URl and dump folder can be defined in `record-request.yaml`.

```bash
~$ mitmdump -s mitm-record.py
```

**[`^        back to top        ^`](#)**

---

### mitm-random-outage

`./mitm-random-outage.py` can simulate sever outage and return 503 code. It will pick randomly the requests to make it 503. The percentage of outage can be changed as the variable `percentage` inside the script.

```bash
~$ mitmdump -s mitm-random-outage.py
```

**[`^        back to top        ^`](#)**
