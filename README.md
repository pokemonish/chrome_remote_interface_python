chrome-remote-interface-python
=======================

[Chrome Debugging Protocol] interface that helps to instrument Chrome (or any
other suitable [implementation](#implementations)) by providing a simple
abstraction of commands and notifications using a straightforward Python
API.

This module is one of the many [third-party protocol clients][3rd-party].

[3rd-party]: https://developer.chrome.com/devtools/docs/debugging-clients#chrome-remote-interface

Sample API usage
----------------

The following snippet loads `https://github.com` and dumps every request made:

```python
import asyncio
import chrome_remote_interface

if __name__ == '__main__':
    class callbacks:
        async def start(tabs):
            tab = await tabs.add()
            await tab.Page.enable()
            await tab.Network.enable()
            await tab.Page.navigate(url='http://github.com')
        async def network__response_received(tabs, tab, requestId, **kwargs):
            try:
                body = tabs.helpers.unpack_response_body(await tab.Network.get_response_body(requestId=requestId))
                print('body:', len(body))
            except tabs.FailReponse as e:
                print('fail:', e)
        async def any(tabs, tab, callback_name, parameters):
            pass
            # print('Unknown event fired', callback_name)

    asyncio.get_event_loop().run_until_complete(chrome_remote_interface.Tabs.run('localhost', 9222, callbacks))
```

Installation
------------

```bash
git clone https://github.com/wasiher/chrome-remote-interface-python.git
python setup.py install
```


Implementations

Setup (all description from [here](https://github.com/cyrus-and/chrome-remote-interface))
-----

An instance of either Chrome itself or another implementation needs to be
running on a known port in order to use this module (defaults to
`localhost:9222`).

### Chrome/Chromium

#### Desktop

Start Chrome with the `--remote-debugging-port` option, for example:

    google-chrome --remote-debugging-port=9222

##### Headless

Since version 57, additionally use the `--headless` option, for example:

    google-chrome --headless --remote-debugging-port=9222

Please note that currently the *DevTools* methods are not properly supported in
headless mode; use the [Target domain] instead. See [#83] and [#84] for more
information.

[#83]: https://github.com/cyrus-and/chrome-remote-interface/issues/83
[#84]: https://github.com/cyrus-and/chrome-remote-interface/issues/84
[Target domain]: https://chromedevtools.github.io/debugger-protocol-viewer/tot/Target/

#### Android

Plug the device and enable the [port forwarding][adb], for example:

    adb forward tcp:9222 localabstract:chrome_devtools_remote

[adb]: https://developer.chrome.com/devtools/docs/remote-debugging-legacy

##### WebView

In order to be inspectable, a WebView must
be [configured for debugging][webview] and the corresponding process ID must be
known. There are several ways to obtain it, for example:

    adb shell grep -a webview_devtools_remote /proc/net/unix

Finally, port forwarding can be enabled as follows:

    adb forward tcp:9222 localabstract:webview_devtools_remote_<pid>

[webview]: https://developers.google.com/web/tools/chrome-devtools/remote-debugging/webviews#configure_webviews_for_debugging

### Edge

Install and run the [Edge Diagnostics Adapter][edge-adapter].

[edge-adapter]: https://github.com/Microsoft/edge-diagnostics-adapter

### Node.js

Start Node.js with the `--inspect` option, for example:

    node --inspect=9222 script.js

### Safari (iOS)

Install and run the [iOS WebKit Debug Proxy][iwdp].

[iwdp]: https://github.com/google/ios-webkit-debug-proxy

Chrome Debugging Protocol versions
----------------------------------

You can update it using this way (It will be downloaded automatically first time)

```python
import chrome_remote_interface
chrome_remote_interface.Protocol.update_protocol()
```

Protocols are loaded from [here](https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/inspector/browser_protocol.json) and [here](https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/inspector/browser_protocol.json)


Contributors
------------

- [Me](https://github.com/wasiher)

Resources
---------

- [Chrome Debugging Protocol]
- [Chrome Debugging Protocol Viewer](https://chromedevtools.github.io/debugger-protocol-viewer/)
- [Chrome Debugging Protocol Google group](https://groups.google.com/forum/#!forum/chrome-debugging-protocol)
- [devtools-protocol official repo](https://github.com/ChromeDevTools/devtools-protocol)
- [Showcase Chrome Debugging Protocol Clients](https://developer.chrome.com/devtools/docs/debugging-clients)
- [Awesome chrome-devtools](https://github.com/ChromeDevTools/awesome-chrome-devtools)

[Chrome Debugging Protocol]: https://developer.chrome.com/devtools/docs/debugger-protocol