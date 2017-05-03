import requests, base64, json, os, websocket




class Protocol:
    '''
    Load and updates protocol
    '''
    BASE = 'https://chromium.googlesource.com'
    BROWSER_PROTOCOL = '/chromium/src/+/master/third_party/WebKit/Source/core/inspector/browser_protocol.json?format=TEXT'
    JS_PROTOCOL = '/v8/v8/+/master/src/inspector/js_protocol.json?format=TEXT'
    PROTOCOL_FILE_NAME = 'protocol.json'

    _protocol = None

    @classmethod
    def get_protocol(cls):
        cls._check()
        return cls._protocol

    @classmethod
    def update_protocol(cls):
        cls._protocol = cls._update_protocol()
        return cls._protocol

    @classmethod
    def _check(cls):
        if cls._protocol is None:
            cls._protocol = cls._load_protocol()

    @classmethod
    def _load_protocol(cls):
        try:
            with open (cls._get_protocol_file_path(), 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return cls._update_protocol()

    @classmethod
    def _update_protocol(cls):
        result = cls._download_protocol(cls.BASE + cls.BROWSER_PROTOCOL)
        result['domains'] += cls._download_protocol(cls.BASE + cls.JS_PROTOCOL)['domains']
        with open(cls._get_protocol_file_path(), 'wb') as f:
            json.dump(result, f)
        return result

    @classmethod
    def _download_protocol(cls, url):
        resp = requests.get(url)
        data = base64.b64decode(resp.text)
        return json.loads(data)

    @classmethod
    def _get_protocol_file_path(cls):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), cls.PROTOCOL_FILE_NAME)

class TabInstances:
    '''
    I put tabs handler here
    '''
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def __repr__(self):
        return 'TabInstances("{0}", {1})'.format(self._host, self._port)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def tabs(self):
        resp = requests.get('http://{0}:{1}/json'.format(self._host, self._port))
        rawTabInstances = json.loads(resp.text)
        tabs = []
        for rawTab in rawTabInstances:
            tabs.append(TabInstance(rawTab))
        return tabs

    def connect(self, tabPosition):
        return SocketClient(self.tabs[tabPosition])

class TabInstance:
    ''' 
    Tab wrapper
    '''
    def __init__(self, dictValue):
        self._dictValue = dictValue
        if 'webSocketDebuggerUrl' in dictValue:
            self._webSocketDebuggerUrl = dictValue['webSocketDebuggerUrl']
            del dictValue['webSocketDebuggerUrl']
        else:
            self._webSocketDebuggerUrl = None

    @property
    def busy(self):
        return self._webSocketDebuggerUrl is None

    def make_busy(self):
        self._webSocketDebuggerUrl = None

    def webSocketDebuggerUrl(setattr):
        return self._webSocketDebuggerUrl

    def __getattr__(self, name):
        if name in self._dictValue:
            return self._dictValue[name]
        else:
            return super().__getattr__(name)

    def __dir__(self):
        return super().__dir__() + list(self._dictValue.keys())

    def __repr__(self):
        return 'TabInstance({0})'.format(self._dictValue)

class SocketClient:
    '''
    CLient 
    '''
    def __init__(self, wsUrl):
        if isinstance(wsUrl, TabInstance):
            if wsUrl.busy:
                raise ValueError('{0} is busy'.format(wsUrl))
            self._wsUrl = wsUrl.webSocketDebuggerUrl
            wsUrl.make_busy()
        else:
            self._wsUrl = wsUrl
        self._soc = websocket.create_connection(self._wsUrl)
        self._i = 0

    @property
    def ws_url(self):
        return self._wsUrl

    def __repr__(self):
        return 'SocketClient("{0}")'.format(self._wsUrl)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def send_raw(self, method, params):
        self._i += 1
        self._soc.send(json.dumps({'id': self._i, 'method': method, 'params': params}))

    def recv_raw(self):
        resp = json.loads(self._soc.recv())
        if 'id' in resp and 'result' in resp:
            idd = resp['id']
            result = resp['result']
        elif 'method' in resp and 'params' in resp:
            method = resp['method']
            params = resp['params']
        else:
            raise RuntimeError('Unknown data came: {0}'.format(resp))

    def close(self):
        if self._soc is not None:
            self._soc.close()
            self._soc = None

class callbacks:
    def Network__data_received():
        pass

class MessagePass:
    def __init__(self):
        rawTypeHandlers = [] # el, key, value
        self._rawProtocol = Protocol.get_protocol()
        versions = self._rawProtocol['version']
        for value in self._rawProtocol['domains']:
            domain = value['domain']
            if not hasattr(self, domain):
                setattr(self, domain, self._result_child())
            currentChild = getattr(self, domain)
            currentChild.__doc__ = value['description'] if 'description' in value else None
            currentChild.experimental = value['experimental'] if 'experimental' in value else False
            currentChild.dependencies = value['dependencies'] if 'dependencies' in value else []
            rawTypes = value['types'] if 'types' in value else []
            for rawType in rawTypes:
                self._connect_raw_type(rawType, domain, rawTypeHandlers, currentChild.types, rawType['id'])
            rawCommands = value['commands'] if 'commands' in value else [] # DIR
            for rawCommand in rawCommands:
                currentChild.methods
                rawCommand['name']
                rawCommand['parameters'] if 'parameters' in rawCommand else []
                rawCommand['experimental'] if 'experimental' in rawCommand else False
                rawCommand['redirect'] if 'redirect' in rawCommand else None 
                rawCommand['returns'] if 'returns' in rawCommand else []
                rawCommand['description'] if 'description' in rawCommand else None
            rawEvents = value['events'] if 'events' in value else [] # DOC?
            for rawEvent in rawEvents:
                rawEvent['name']
                rawEvent['experimental'] if 'experimental' in rawEvent else False
                rawEvent['description'] if 'description' in rawEvent else None
                rawEvent['parameters'] if 'parameters' in rawEvent else []
        while len(rawTypeHandlers) > 0:
            for parent, key, rawType, connect_funcion, domain in rawTypeHandlers:
                self._connect_raw_type(rawType, domain, rawTypeHandlers, parent, key, connect_funcion)

    def _connect_raw_type(self, rawType, domain, rawTypeHandlers, parent, key, connect_funcion=setattr):
        successRemoveTuple = parent, key, rawType, connect_funcion, domain
        if '$ref' in rawType:
            ref = rawType['$ref']
            try:
                var1, var2 = ref.split('.', 1)
                print(111111, var1, var2)
            except ValueError:
                var1 = domain
                var2 = ref
                print(222222, var1, var2)
            try:
                connect_funcion(parent, key, getattr(getattr(self, var1).types, var2))
                if successRemoveTuple in rawTypeHandlers:
                    rawTypeHandlers.remove(successRemoveTuple)
            except AttributeError:
                if successRemoveTuple not in rawTypeHandlers:
                    rawTypeHandlers.append(successRemoveTuple)
        elif 'type' in rawType:
            t = rawType['type']
            if t == 'array':
                class coolType(list):
                    def __init__(slf, values):
                        if slf.minItems is not None and len(values) < slf.minItems:
                            raise ValueError('Min items is lower than')
                        if slf.minItems is not None and len(values) > slf.maxItems:
                            raise ValueError('Max items is lower than')
                        if slf.itemsType is None:
                            super().__init__(values)
                        else:
                            resultingValues = []
                            for value in values:
                                resultingValues.append(slf.itemsType(value))
                            super().__init__(resultingValues)
                coolType.maxItems = rawType['maxItems'] if 'maxItems' in rawType else None
                coolType.minItems = rawType['minItems'] if 'minItems' in rawType else None
                rawItems = rawType['items'] if 'items' in rawType else None
                if rawItems is None:
                    coolType.itemsType = None
                else:
                    self._connect_raw_type(rawItems, domain, rawTypeHandlers, coolType, 'itemsType')
            elif t == 'object':
                class coolType:
                    def __init__(slf, values):
                        toAdd = set(slf.propertyNames.keys())
                        for key in values:
                            if key not in slf.propertyNames:
                                raise ValueError('there is no such property: {0}'.format(key))
                            else:
                                setattr(slf, key, slf.propertyNames[key](values[key]))
                                toAdd.remove(key)
                        if len(toAdd) > 0:
                            raise ValueError('Not enough parameters: {0}'.format(', '.join(toAdd)))
                rawProperties = rawType['properties'] if 'properties' in rawType else []
                coolType.propertyNames = {}
                for rawProperty in rawProperties:
                    self._connect_raw_type(rawProperty, domain, rawTypeHandlers, coolType.propertyNames, rawProperty['name'], dict.__setitem__.__call__)
            elif t == 'string':
                enum = rawType['enum'] if 'enum' in rawType else None
                if enum is None:
                    coolType = self._dummy_cool_type(str)
                else:
                    class coolType(str):
                        def __init__(self, value):
                            if value not in self.enum:
                                raise ValueError('string must be one of the following: {0}'.format(', '.join(self.enum)))
                            super().__init__(value)
                    coolType.enum = enum
            elif t in ['integer', 'number', 'any', 'boolean']:
                coolType = self._dummy_cool_type({'integer': int, 'number': float, 'boolean': bool, 'any': None}[t])
            else:
                raise ValueError('Unknown type: {0}'.format(t))
            if 'description' in rawType:
                coolType.__doc__ = rawType['description']
            coolType.experimental = rawType['experimental'] if 'experimental' in rawType else None
            connect_funcion(parent, key, coolType)
            if successRemoveTuple in rawTypeHandlers:
                rawTypeHandlers.remove(successRemoveTuple)
        else:
            raise ValueError('There is no type or $ref {0}'.format(rawType))

    def _dummy_cool_type(self, t=None):
        class coolType:
            def __new__(cls, obj):
                if cls._type is not None and cls._type != type(obj):
                    raise ValueError('Type must be {0}, not {1}'.format(cls._type, type(obj)))
                return obj
        coolType._type = t
        return coolType

    def _empty_class(self):
        class a: pass
        return a

    def _result_child(self):
        class a:
            class types: pass
            class methods: pass
        return a
















