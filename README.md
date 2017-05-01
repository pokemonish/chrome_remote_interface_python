chrome-remote-interface-python
=======================

[Chrome Debugging Protocol] interface that helps to instrument Chrome (or any
other suitable [implementation](#implementations)) by providing a simple
abstraction of commands and notifications using a straightforward JavaScript
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

Find more examples in the [wiki], in particular notice how the above can be
rewritten using the [`async`/`await`][async-await-example] primitives.

[wiki]: https://github.com/cyrus-and/chrome-remote-interface/wiki
[async-await-example]: https://github.com/cyrus-and/chrome-remote-interface/wiki/Async-await-example

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

API
---

The API consists of three parts:

- *DevTools* methods (for those [implementations](#implementations) that support
  them, e.g., [List](#cdplistoptions-callback), [New](#cdpnewoptions-callback),
  etc.);

- [connection](#cdpoptions-callback) establishment;

- the actual [protocol interaction](#class-cdp).

### CDP([options], [callback])

Connects to a remote instance using the [Chrome Debugging Protocol].

`options` is an object with the following optional properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`;
- `target`: determines which target this client should attach to. The behavior
  changes according to the type:

  - a `function` that takes the array returned by the `List` method and returns
    a target or its numeric index relative to the array;
  - a target `object` like those returned by the `New` and `List` methods;
  - a `string` representing the raw WebSocket URL, in this case `host` and
    `port` are not used to fetch the target list, yet they are used to complete
    the URL if relative.

  Defaults to a function which returns the first available target according to
  the implementation (note that at most one connection can be established to the
  same target);
- `protocol`: [Chrome Debugging Protocol] descriptor object. Defaults to use the
  protocol chosen according to the `remote` option;
- `remote`: a boolean indicating whether the protocol must be fetched *remotely*
  or if the local version must be used. It has no effect if the `protocol`
  option is set. Defaults to `false`.

These options are also valid properties of all the instances of the `CDP` class.

`callback` is a listener automatically added to the `connect` event of the
returned `EventEmitter`. When `callback` is omitted a `Promise` object is
returned which becomes fulfilled if the `connect` event is triggered and
rejected if any of the `disconnect` or `error` events are triggered.

The `EventEmitter` supports the following events:

#### Event: 'connect'

```javascript
function (client) {}
```

Emitted when the connection to the WebSocket is established.

`client` is an instance of the `CDP` class.

#### Event: 'disconnect'

```javascript
function () {}
```

Emitted when an instance closes the WebSocket connection.

This may happen for example when the user opens DevTools for the currently
inspected Chrome target.

#### Event: 'error'

```javascript
function (err) {}
```

Emitted when `http://host:port/json` cannot be reached or if it is not possible
to connect to the WebSocket.

`err` is an instance of `Error`.

### CDP.Protocol([options], [callback])

Fetch the [Chrome Debugging Protocol] descriptor.

`options` is an object with the following optional properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`;
- `remote`: a boolean indicating whether the protocol must be fetched *remotely*
  or if the local version must be returned. If it is not possible to fulfill the
  request then the local version is used. Defaults to `false`.

`callback` is executed when the protocol is fetched, it gets the following
arguments:

- `err`: a `Error` object indicating the success status;
- `protocol`: an object with the following properties:
   - `remote`: a boolean indicating whether the returned descriptor is the
     remote version or not (due to user choice or error);
   - `descriptor`: the [Chrome Debugging Protocol] descriptor.

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.Protocol(function (err, protocol) {
    if (!err) {
        console.log(JSON.stringify(protocol.descriptor, null, 4));
    }
});
```

### CDP.List([options], [callback])

Request the list of the available open targets/tabs of the remote instance.

`options` is an object with the following optional properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`.

`callback` is executed when the list is correctly received, it gets the
following arguments:

- `err`: a `Error` object indicating the success status;
- `targets`: the array returned by `http://host:port/json/list` containing the
  target list.

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.List(function (err, targets) {
    if (!err) {
        console.log(targets);
    }
});
```

### CDP.New([options], [callback])

Create a new target/tab in the remote instance.

`options` is an object with the following optional properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`;
- `url`: URL to load in the new target/tab. Defaults to `about:blank`.

`callback` is executed when the target is created, it gets the following
arguments:

- `err`: a `Error` object indicating the success status;
- `target`: the object returned by `http://host:port/json/new` containing the
  target.

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.New(function (err, target) {
    if (!err) {
        console.log(target);
    }
});
```

### CDP.Activate([options], [callback])

Activate an open target/tab of the remote instance.

`options` is an object with the following properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`;
- `id`: Target id. Required, no default.

`callback` is executed when the response to the activation request is
received. It gets the following arguments:

- `err`: a `Error` object indicating the success status;

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.Activate({'id': 'CC46FBFA-3BDA-493B-B2E4-2BE6EB0D97EC'}, function (err) {
    if (!err) {
        console.log('target is activated');
    }
});
```

### CDP.Close([options], [callback])

Close an open target/tab of the remote instance.

`options` is an object with the following properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`;
- `id`: Target id. Required, no default.

`callback` is executed when the response to the close request is received. It
gets the following arguments:

- `err`: a `Error` object indicating the success status;

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.Close({'id': 'CC46FBFA-3BDA-493B-B2E4-2BE6EB0D97EC'}, function (err) {
    if (!err) {
        console.log('target is closing');
    }
});
```

Note that the callback is fired when the target is *queued* for removal, but the
actual removal will occur asynchronously.

### CDP.Version([options], [callback])

Request version information from the remote instance.

`options` is an object with the following optional properties:

- `host`: HTTP frontend host. Defaults to `localhost`;
- `port`: HTTP frontend port. Defaults to `9222`;
- `secure`: HTTPS/WSS frontend. Defaults to `false`.

`callback` is executed when the version information is correctly received, it
gets the following arguments:

- `err`: a `Error` object indicating the success status;
- `info`: a JSON object returned by `http://host:port/json/version` containing
  the version information.

When `callback` is omitted a `Promise` object is returned.

For example:

```javascript
const CDP = require('chrome-remote-interface');
CDP.Version(function (err, info) {
    if (!err) {
        console.log(info);
    }
});
```

### Class: CDP

#### Event: 'event'

```javascript
function (message) {}
```

Emitted when the remote instance sends any notification through the WebSocket.

`message` is the object received, it has the following properties:

- `method`: a string describing the notification (e.g.,
  `'Network.requestWillBeSent'`);
- `params`: an object containing the payload.

Refer to the [Chrome Debugging Protocol] specification for more information.

For example:

```javascript
client.on('event', function (message) {
    if (message.method === 'Network.requestWillBeSent') {
        console.log(message.params);
    }
});
```

#### Event: '`<domain>`.`<method>`'

```javascript
function (params) {}
```

Emitted when the remote instance sends a notification for `<domain>.<method>`
through the WebSocket.

`params` is an object containing the payload.

This is just a utility event which allows to easily listen for specific
notifications (see [`'event'`](#event-event)), for example:

```javascript
client.on('Network.requestWillBeSent', console.log);
```

#### Event: 'ready'

```javascript
function () {}
```

Emitted every time that there are no more pending commands waiting for a
response from the remote instance. The interaction is asynchronous so the only
way to serialize a sequence of commands is to use the callback provided by
the [`send`](#clientsendmethod-params-callback) method. This event acts as a
barrier and it is useful to avoid the *callback hell* in certain simple
situations.

Users are encouraged to extensively check the response of each method and should
prefer the promises API when dealing with complex asynchronous program flows.

For example to load a URL only after having enabled the notifications of both
`Network` and `Page` domains:

```javascript
client.Network.enable();
client.Page.enable();
client.once('ready', function () {
    client.Page.navigate({'url': 'https://github.com'});
});
```

In this particular case, not enforcing this kind of serialization may cause that
the remote instance does not properly deliver the desired notifications the
client.

#### client.send(method, [params], [callback])

Issue a command to the remote instance.

`method` is a string describing the command.

`params` is an object containing the payload.

`callback` is executed when the remote instance sends a response to this
command, it gets the following arguments:

- `error`: a boolean value indicating the success status, as reported by the
  remote instance;
- `response`: an object containing either the response (`result` field, if
  `error === false`) or the indication of the error (`error` field, if `error
  === true`).

When `callback` is omitted a `Promise` object is returned instead, with the
fulfilled/rejected states implemented according to the `error` parameter.

Note that the field `id` mentioned in the [Chrome Debugging Protocol]
specification is managed internally and it is not exposed to the user.

For example:

```javascript
client.send('Page.navigate', {'url': 'https://github.com'}, console.log);
```

#### client.`<domain>`.`<method>`([params], [callback])

Just a shorthand for:

```javascript
client.send('<domain>.<method>', params, callback);
```

For example:

```javascript
client.Page.navigate({'url': 'https://github.com'}, console.log);
```

#### client.`<domain>`.`<event>`([callback])

Just a shorthand for:

```javascript
client.on('<domain>.<event>', callback);
```

The only difference is that when `callback` is omitted the event is registered
only once and a `Promise` object is returned.

For example:

```javascript
client.Network.requestWillBeSent(console.log);
```

#### client.close([callback])

Close the connection to the remote instance.

`callback` is executed when the WebSocket is successfully closed.

When `callback` is omitted a `Promise` object is returned.

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