chrome-remote-interface-python
=======================

[Chrome Debugging Protocol] interface that helps to instrument Chrome (or any
other suitable [implementation](#implementations)) by providing a simple
abstraction of commands and notifications using a straightforward Python
API.

This module is one of the many [third-party protocol clients][3rd-party].

[3rd-party]: https://developer.chrome.com/devtools/docs/debugging-clients#chrome-remote-interface

For now description is just a copy-paste of [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface).

Sample API usage
----------------

The following snippet loads `https://github.com` and dumps every request made:

```python
Nope yet
```

Installation
------------

    maybe pip install one day


Implementations
---------------

Maybe I will understand later

Setup
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

`chrome-remote-interface` uses the [local version] of the protocol descriptor by
default. This file is manually updated from time to time using
`scripts/update-protocol.sh` and pushed to this repository.

This behavior can be changed by setting the `remote` option to `true`
upon [connection](#cdpoptions-callback), in which case the remote instance is
*asked* to provide its own protocol descriptor.

Currently Chrome is not able to do that (see [#10]), so the protocol descriptor
is fetched from the proper [source repository].

To override the above behavior there are basically three options:

- pass a custom protocol descriptor upon [connection](#cdpoptions-callback)
  (`protocol` option);

- use the *raw* version of the [commands](#clientsendmethod-params-callback)
  and [events](#event-domainmethod) interface;

- update the local copy with `scripts/update-protocol.sh` (not present when
  fetched with `npm install`).

[local version]: lib/protocol.json
[#10]: https://github.com/cyrus-and/chrome-remote-interface/issues/10
[source repository]: https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/

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