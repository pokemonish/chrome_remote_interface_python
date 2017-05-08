''' Client for the Google Chrome browser's remote debugging api.

Chrome Debugging Protocol interface that helps to instrument Chrome (or any other suitable implementation) by providing a simple abstraction of commands and notifications using a straightforward Python API.
This module is one of the many third-party protocol clients.
'''


from .library import (
    Protocol,
    FailReponse,
    API,
    TabsSync,
    SocketClientSync,
    Tabs,
    SocketClient,
    helpers
)