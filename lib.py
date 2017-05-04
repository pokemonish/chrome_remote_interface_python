import requests, base64, json, os, types, websocket, copy




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
        with open(cls._get_protocol_file_path(), 'w') as f:
            json.dump(result, f, indent=4, sort_keys=True)
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
        raw_tab_instances = json.loads(resp.text)
        tabs = []
        for raw_tab in raw_tab_instances:
            tabs.append(TabInstance(raw_tab))
        return tabs

    def connect(self, tab_position):
        return SocketClient(self.tabs[tab_position])

class TabInstance:
    ''' 
    Tab wrapper
    '''
    def __init__(self, dict_value):
        self._dict_value = dict_value
        if 'webSocketDebuggerUrl' in dict_value:
            self._web_socket_debugger_url = dict_value['webSocketDebuggerUrl']
            del dict_value['webSocketDebuggerUrl']
        else:
            self._web_socket_debugger_url = None

    @property
    def busy(self):
        return self._web_socket_debugger_url is None

    def make_busy(self):
        self._web_socket_debugger_url = None

    def web_socket_debugger_url(self):
        return self._web_socket_debugger_url

    def __getattr__(self, name):
        if name in self._dict_value:
            return self._dict_value[name]
        else:
            return super().__getattr__(name)

    def __dir__(self):
        return super().__dir__() + list(self._dict_value.keys())

    def __repr__(self):
        return 'TabInstance({0})'.format(self._dict_value)

class SocketClient:
    '''
    CLient 
    '''
    def __init__(self, ws_url):
        if isinstance(ws_url, TabInstance):
            if ws_url.busy:
                raise ValueError('{0} is busy'.format(ws_url))
            self._ws_url = ws_url.web_socket_debugger_url
            ws_url.make_busy()
        else:
            self._ws_url = ws_url
        self._soc = websocket.create_connection(self._ws_url)
        self._i = 0

    @property
    def ws_url(self):
        return self._ws_url

    def __repr__(self):
        return 'SocketClient("{0}")'.format(self._ws_url)

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

class MessagePass:
    '''
    Making magick with json data to create classes and functions
    '''
    def __init__(self):
        raw_type_handlers = []
        self._raw_protocol = copy.deepcopy(Protocol.get_protocol())
        self.events = self._empty_class()
        self._event_name_to_callback_name = {}
        versions = self._raw_protocol['version']
        for value in self._raw_protocol['domains']:
            domain = value['domain']
            if not hasattr(self, domain):
                setattr(self, domain, self._repr_class(domain))
            current_child = getattr(self, domain)
            if 'description' in value:
                current_child.__doc__ = value['description']
            current_child.experimental = value['experimental'] if 'experimental' in value else False
            current_child.dependencies = value['dependencies'] if 'dependencies' in value else []
            raw_types = value['types'] if 'types' in value else []
            for raw_type in raw_types:
                self._connect_raw_type(raw_type, domain, raw_type_handlers, current_child, raw_type['id'], domain+'.'+raw_type['id'])
            raw_commands = value['commands'] if 'commands' in value else [] # DIR
            for raw_command in raw_commands:
                method = self._make_send_method(raw_command['name'], domain+'.'+raw_command['name'])
                method.parameters = {}
                raw_parameters = raw_command['parameters'] if 'parameters' in raw_command else []
                for raw_parameter in raw_parameters:
                    self._connect_raw_parameter_or_result(raw_parameter, domain, raw_type_handlers, method.parameters)
                method.returns = {}
                raw_returns = raw_command['returns'] if 'returns' in raw_command else []
                for raw_return in raw_returns:
                    self._connect_raw_parameter_or_result(raw_return, domain, raw_type_handlers, method.returns)
                method.redirect = raw_command['redirect'] if 'redirect' in raw_command else None
                method.experimental = raw_command['experimental'] if 'experimental' in raw_command else False
                if 'description' in raw_command:
                    method.__doc__ = raw_command['description']
                setattr(current_child, self._pythonic_method_name(raw_command['name']), method)
            raw_events = value['events'] if 'events' in value else [] # DOC?
            for raw_event in raw_events:
                callback_name = domain + '__' + self._pythonic_method_name(raw_event['name'])
                event_name = domain + '.' + raw_event['name']
                self._event_name_to_callback_name[event_name] = callback_name
                event = self._repr_class(callback_name)
                if 'description' in raw_event:
                    event.__doc__ = raw_event['description']
                event.experimental = raw_event['experimental'] if 'experimental' in raw_event else False
                raw_parameters = raw_event['parameters'] if 'parameters' in raw_event else []
                event.parameters = {}
                for raw_parameter in raw_parameters:
                    self._connect_raw_parameter_or_result(raw_parameter, domain, raw_type_handlers, event.parameters)
                setattr(self.events, callback_name, event)
        while len(raw_type_handlers) > 0:
            for parent, key, raw_type, connect_funcion, domain, class_repr, callbacks in raw_type_handlers:
                self._connect_raw_type(raw_type, domain, raw_type_handlers, parent, key, class_repr, connect_funcion, callbacks)

    def _connect_raw_type(self, raw_type, domain, raw_type_handlers, parent, key, class_repr, connect_funcion=setattr, callback=None):
        success_remove_tuple = parent, key, raw_type, connect_funcion, domain, class_repr, callback
        if '$ref' in raw_type:
            ref = raw_type['$ref']
            try:
                var1, var2 = ref.split('.', 1)
            except ValueError:
                var1 = domain
                var2 = ref
            try:
                connect_funcion(parent, key, getattr(getattr(self, var1), var2))
                if success_remove_tuple in raw_type_handlers:
                    raw_type_handlers.remove(success_remove_tuple)
                if callback is not None:
                    callback()
            except AttributeError:
                if success_remove_tuple not in raw_type_handlers:
                    raw_type_handlers.append(success_remove_tuple)
        elif 'type' in raw_type:
            t = raw_type['type']
            if t == 'array':
                class CoolType(list, metaclass=self._CustomClassRepr):
                    def __init__(slf, values):
                        if slf.min_items is not None and len(values) < slf.min_items:
                            raise ValueError('Min items is lower than')
                        if slf.max_items is not None and len(values) > slf.max_items:
                            raise ValueError('Max items is lower than')
                        if slf.items_type is None:
                            super().__init__(values)
                        else:
                            resulting_values = []
                            for value in values:
                                resulting_values.append(slf.items_type(value))
                            super().__init__(resulting_values)
                CoolType._class_repr = class_repr if class_repr is not None else 'array'
                CoolType.max_items = raw_type['max_items'] if 'max_items' in raw_type else None
                CoolType.min_items = raw_type['min_items'] if 'min_items' in raw_type else None
                raw_items = raw_type['items'] if 'items' in raw_type else None
                if raw_items is None:
                    CoolType.items_type = None
                else:
                    self._connect_raw_type(raw_items, domain, raw_type_handlers, CoolType, 'items_type', None)
            elif t == 'object':
                if 'id' in raw_type:
                    class CoolType(metaclass=self._CustomClassRepr):
                        def __init__(slf, values):
                            to_add = set(slf._propertyNameToType.keys())
                            for key in values:
                                if key not in slf._propertyNameToType:
                                    raise ValueError('there is no such property: {0}'.format(key))
                                else:
                                    setattr(slf, key, slf._propertyNameToType[key](values[key]))
                                    to_add.remove(key)
                            if len(to_add) > 0:
                                raise ValueError('Not enough parameters: {0}'.format(', '.join(to_add)))
                    CoolType._class_repr = class_repr
                    raw_properties = raw_type['properties'] if 'properties' in raw_type else []
                    CoolType._propertyNameToType = {}
                    for raw_property in raw_properties:
                        self._connect_raw_type(raw_property, domain, raw_type_handlers, CoolType._propertyNameToType, raw_property['name'], None, dict.__setitem__.__call__)
                    CoolType.propertyNames = set(CoolType._propertyNameToType.keys())
                else:
                    CoolType = self._dummy_cool_type(class_repr, dict)
            elif t == 'string':
                enum = raw_type['enum'] if 'enum' in raw_type else None
                if enum is None:
                    CoolType = self._dummy_cool_type(class_repr, str)
                else:
                    class CoolType(str, metaclass=self._CustomClassRepr):
                        def __new__(cls, value):
                            if value not in cls.enum:
                                raise ValueError('string must be one of the following: {0}'.format(', '.join(cls.enum)))
                            return value
                    CoolType.enum = enum
                    CoolType._class_repr = class_repr
            elif t in ['integer', 'number', 'any', 'boolean']:
                CoolType = self._dummy_cool_type(class_repr, {'integer': int, 'number': float, 'boolean': bool, 'any': None}[t])
            else:
                raise ValueError('Unknown type: {0}'.format(t))
            if 'description' in raw_type:
                CoolType.__doc__ = raw_type['description']
            CoolType.experimental = raw_type['experimental'] if 'experimental' in raw_type else None
            CoolType.deprecated = raw_type['deprecated'] if 'deprecated' in raw_type else False
            connect_funcion(parent, key, CoolType)
            if success_remove_tuple in raw_type_handlers:
                raw_type_handlers.remove(success_remove_tuple)
            if callback is not None:
                callback()
        else:
            raise ValueError('There is no type or $ref {0}'.format(raw_type))

    def _connect_raw_parameter_or_result(self, raw_value, domain, raw_type_handlers, parent):
        value = self._empty_class()
        name = raw_value['name']
        if 'optional' in raw_value:
            optional_value = raw_value['optional']
            del raw_value['optional']
        else:
            optional_value = False
        def callback():
            o = parent[name]
            o._optional = optional_value
            if hasattr(o, '_type'):
                o._class_repr = o._type.__name__
        self._connect_raw_type(raw_value, domain, raw_type_handlers, parent, name, None, dict.__setitem__.__call__, callback)

    def _make_send_method(self, original_name, class_repr):
        class result():
            def __call__(slf, **kwargs):
                for key, value in slf.parameters.items():
                    if not value._optional and key not in kwargs:
                        raise TypeError('Required argument \'{0}\' not found'.format(key))
                for key, arg in kwargs.items():
                    param = slf.parameters[key]
                    potential_class = param._type if hasattr(param, '_type') else param
                    valid = (arg.__class__ == potential_class) or (potential_class == float and arg.__class__ == int)
                    if not valid:
                        raise ValueError('Param \'{0}\' must be {1}'.format(key, potential_class))
                self.send_raw(slf._original_name, kwargs)
            def __repr__(self):
                return self._class_repr
        result._original_name = original_name
        result._class_repr = class_repr
        return result()

    def send_raw(self, command_name, parameters):
        print('sending:', command_name, parameters)

    def notify(self, event_name, params):
        callback_name = self._event_name_to_callback_name[event_name]

    def _pythonic_method_name(self, old_name):
        old_one = list(old_name)
        new_one = []
        previous_was_low = True
        previous_was_underscore = False
        for i in reversed(range(len(old_one))):
            c = old_one[i]
            if c.isupper():
                if previous_was_low:
                    new_one.append('_'+c.lower())
                    previous_was_underscore = True
                else:
                    new_one.append(c.lower())
                    previous_was_underscore = False
                previous_was_low = False
            else:
                if previous_was_low:
                    new_one.append(c)
                else:
                    if previous_was_underscore:
                        new_one.append(c)
                    else:
                        new_one.append(c+'_')
                previous_was_underscore = False
                previous_was_low = True
        return ''.join(reversed(new_one))

    def _dummy_cool_type(self, class_repr, t):
        class CoolType(metaclass=self._CustomClassRepr):
            def __new__(cls, obj):
                if cls._type == float and type(obj) == int:
                    obj = float(obj)
                if cls._type is not None and cls._type != type(obj):
                    raise ValueError('Type must be {0}, not {1}'.format(cls._type, type(obj)))
                return obj
        CoolType._type = t
        CoolType._class_repr = class_repr
        return CoolType

    class _CustomClassRepr(type):
        def __repr__(self):
            if self._class_repr is not None:
                return self._class_repr
            else:
                return super().__repr__()

    def _empty_class(self):
        class a: pass
        return a

    def _repr_class(self, class_repr):
        class a(metaclass=self._CustomClassRepr): pass
        a._class_repr = class_repr
        return a


















