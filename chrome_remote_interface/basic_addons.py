import pyperclip, asyncio

class targets:
    '''
    Used to handle tabs which opened without our wish
    '''
    class events:
        async def tab_start(tabs, tab):
            await tab.Target.set_discover_targets(True)
            await tab.Page.set_auto_attach_to_created_pages(True)
            await tab.Inspector.enable()
        async def target__target_created(tabs, tab, targetInfo, **kwargs):
            if targetInfo.type != 'browser' and targetInfo.targetId not in tabs._initial_tabs and targetInfo.targetId not in tabs._tabs:
                try:
                    tab = await tab.__class__(tabs._host, tabs._port, tabs, targetInfo.targetId).__aenter__()
                    tab.manual = False
                    tabs._tabs[tab.id] = tab
                    await tab.Runtime.run_if_waiting_for_debugger()
                    tab._emit_event('tab_start')
                except (KeyError, ValueError, tabs.ConnectionClosed, tabs.InvalidHandshake):
                    pass
        async def inspector__detached(tabs, tab, reason):
            await tab.close(force=True)
            tab._emit_event('tab_suicide', reason=reason)
        async def inspector__target_crashed(tabs, tab):
            await tab.close(force=True)
            tab._emit_event('tab_suicide', reason='target_crashed')


class mouse:
    '''
    
    '''


class KeysTuple:
    def __init__(self, code, key, text, unmodified_text, windows_virtual_key_code, native_virtual_key_code, is_system_key, is_keypad):
        self.code = code
        self.key = key
        self.text = text
        self.unmodified_text = unmodified_text
        self.key_code = native_virtual_key_code
        self.windows_virtual_key_code = windows_virtual_key_code
        self.native_virtual_key_code = native_virtual_key_code
        self.is_system_key = is_system_key
        self.is_keypad = is_keypad
    def __repr__(self):
        return 'KeysTuple({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(
            self.code, self.key, self.text, self.unmodified_text, self.windows_virtual_key_code,
            self.native_virtual_key_code, self.is_keypad, self.is_system_key
        )
class keyboard:
    '''
    Basic example of key input.
    Only basic chars right now :(
    '''
    class macros:
        async def Input__press_key(tabs, tab, key, modifiers=None):
            if modifiers is None:
                modifiers = tabs.helpers.keyboard.modifiers()
            button = tabs.helpers.keyboard.buttons[key]
            await tab.Input.dispatch_key_event(type='keyDown', timestamp=tab.timestamp(), code=button.code, windowsVirtualKeyCode=button.windows_virtual_key_code, nativeVirtualKeyCode=button.native_virtual_key_code, key=button.key, autoRepeat=False, isKeypad=button.is_keypad, isSystemKey=button.is_system_key, modifiers=modifiers)
            if button.text is not None:
                await tab.Input.dispatch_key_event(type='char', timestamp=tab.timestamp(), code=button.code, windowsVirtualKeyCode=button.windows_virtual_key_code, nativeVirtualKeyCode=button.native_virtual_key_code, key=button.key, autoRepeat=False, isKeypad=button.is_keypad, isSystemKey=button.is_system_key, modifiers=modifiers, text=button.text, unmodifiedText=button.unmodified_text)
            await tab.Input.dispatch_key_event(type='keyUp', timestamp=tab.timestamp(), code=button.code, windowsVirtualKeyCode=button.windows_virtual_key_code, nativeVirtualKeyCode=button.native_virtual_key_code, key=button.key, autoRepeat=False, isKeypad=button.is_keypad, isSystemKey=button.is_system_key, modifiers=modifiers)
        async def Input__send_keys(tabs, tab, keys):
            for key in keys:
                await Input.press_key(key)
        async def Input__paste(tabs, tab, data):
            try:
                backup = pyperclip.determine_clipboard()[1]() # Not sure if is correct D:
            except:
                backup = None
            pyperclip.copy(data)
            await tab.Input.press_key(tabs.helpers.keyboard.PASTE)
            if backup is not None:
                pyperclip.copy(backup)
    class helpers:
        buttons = {
            '\b': KeysTuple('Backspace', 'Backspace', None, None, 8, 8, False, False),
            '\t': KeysTuple('Tab', 'Tab', None, None, 9, 9, False, False),
            '\r': KeysTuple('Enter', 'Enter', '\r', '\r', 13, 13, False, True),
            '\u001b': KeysTuple('Escape', 'Escape', None, None, 27, 27, False, False),
            ' ': KeysTuple('Space', ' ', ' ', ' ', 32, 32, False, True),
            '!': KeysTuple('Digit1', '!', '!', '1', 49, 49, True, True),
            '\'': KeysTuple('Quote', '\'', '\'', '\'', 222, 222, True, True),
            '#': KeysTuple('Digit3', '#', '#', '3', 51, 51, True, True),
            '$': KeysTuple('Digit4', '$', '$', '4', 52, 52, True, True),
            '%': KeysTuple('Digit5', '%', '%', '5', 53, 53, True, True),
            '&': KeysTuple('Digit7', '&', '&', '7', 55, 55, True, True),
            '\'': KeysTuple('Quote', '\'', '\'', '\'', 222, 222, False, True),
            '(': KeysTuple('Digit9', '(', '(', '9', 57, 57, True, True),
            '),': KeysTuple('Digit0', '),', '),', '0', 48, 48, True, True),
            '*': KeysTuple('Digit8', '*', '*', '8', 56, 56, True, True),
            '+': KeysTuple('Equal', '+', '+', '=', 187, 187, True, True),
            ',': KeysTuple('Comma', ',', ',', ',', 188, 188, False, True),
            '-': KeysTuple('Minus', '-', '-', '-', 189, 189, False, True),
            '.': KeysTuple('Period', '.', '.', '.', 190, 190, False, True),
            '/': KeysTuple('Slash', '/', '/', '/', 191, 191, False, True),
            '0': KeysTuple('Digit0', '0', '0', '0', 48, 48, False, True),
            '1': KeysTuple('Digit1', '1', '1', '1', 49, 49, False, True),
            '2': KeysTuple('Digit2', '2', '2', '2', 50, 50, False, True),
            '3': KeysTuple('Digit3', '3', '3', '3', 51, 51, False, True),
            '4': KeysTuple('Digit4', '4', '4', '4', 52, 52, False, True),
            '5': KeysTuple('Digit5', '5', '5', '5', 53, 53, False, True),
            '6': KeysTuple('Digit6', '6', '6', '6', 54, 54, False, True),
            '7': KeysTuple('Digit7', '7', '7', '7', 55, 55, False, True),
            '8': KeysTuple('Digit8', '8', '8', '8', 56, 56, False, True),
            '9': KeysTuple('Digit9', '9', '9', '9', 57, 57, False, True),
            ':': KeysTuple('Semicolon', ':', ':', ';', 186, 186, True, True),
            ';': KeysTuple('Semicolon', ';', ';', ';', 186, 186, False, True),
            '<': KeysTuple('Comma', '<', '<', ',', 188, 188, True, True),
            '=': KeysTuple('Equal', '=', '=', '=', 187, 187, False, True),
            '>': KeysTuple('Period', '>', '>', '.', 190, 190, True, True),
            '?': KeysTuple('Slash', '?', '?', '/', 191, 191, True, True),
            '@': KeysTuple('Digit2', '@', '@', '2', 50, 50, True, True),
            'A': KeysTuple('KeyA', 'A', 'A', 'a', 65, 65, True, True),
            'B': KeysTuple('KeyB', 'B', 'B', 'b', 66, 66, True, True),
            'C': KeysTuple('KeyC', 'C', 'C', 'c', 67, 67, True, True),
            'D': KeysTuple('KeyD', 'D', 'D', 'd', 68, 68, True, True),
            'E': KeysTuple('KeyE', 'E', 'E', 'e', 69, 69, True, True),
            'F': KeysTuple('KeyF', 'F', 'F', 'f', 70, 70, True, True),
            'G': KeysTuple('KeyG', 'G', 'G', 'g', 71, 71, True, True),
            'H': KeysTuple('KeyH', 'H', 'H', 'h', 72, 72, True, True),
            'I': KeysTuple('KeyI', 'I', 'I', 'i', 73, 73, True, True),
            'J': KeysTuple('KeyJ', 'J', 'J', 'j', 74, 74, True, True),
            'K': KeysTuple('KeyK', 'K', 'K', 'k', 75, 75, True, True),
            'L': KeysTuple('KeyL', 'L', 'L', 'l', 76, 76, True, True),
            'M': KeysTuple('KeyM', 'M', 'M', 'm', 77, 77, True, True),
            'N': KeysTuple('KeyN', 'N', 'N', 'n', 78, 78, True, True),
            'O': KeysTuple('KeyO', 'O', 'O', 'o', 79, 79, True, True),
            'P': KeysTuple('KeyP', 'P', 'P', 'p', 80, 80, True, True),
            'Q': KeysTuple('KeyQ', 'Q', 'Q', 'q', 81, 81, True, True),
            'R': KeysTuple('KeyR', 'R', 'R', 'r', 82, 82, True, True),
            'S': KeysTuple('KeyS', 'S', 'S', 's', 83, 83, True, True),
            'T': KeysTuple('KeyT', 'T', 'T', 't', 84, 84, True, True),
            'U': KeysTuple('KeyU', 'U', 'U', 'u', 85, 85, True, True),
            'V': KeysTuple('KeyV', 'V', 'V', 'v', 86, 86, True, True),
            'W': KeysTuple('KeyW', 'W', 'W', 'w', 87, 87, True, True),
            'X': KeysTuple('KeyX', 'X', 'X', 'x', 88, 88, True, True),
            'Y': KeysTuple('KeyY', 'Y', 'Y', 'y', 89, 89, True, True),
            'Z': KeysTuple('KeyZ', 'Z', 'Z', 'z', 90, 90, True, True),
            '[': KeysTuple('BracketLeft', '[', '[', '[', 219, 219, False, True),
            '\\': KeysTuple('Backslash', '\\', '\\', '\\', 220, 220, False, True),
            ']': KeysTuple('BracketRight', ']', ']', ']', 221, 221, False, True),
            '^': KeysTuple('Digit6', '^', '^', '6', 54, 54, True, True),
            '_': KeysTuple('Minus', '_', '_', '-', 189, 189, True, True),
            '`': KeysTuple('Backquote', '`', '`', '`', 192, 192, False, True),
            'a': KeysTuple('KeyA', 'a', 'a', 'a', 65, 65, False, True),
            'b': KeysTuple('KeyB', 'b', 'b', 'b', 66, 66, False, True),
            'c': KeysTuple('KeyC', 'c', 'c', 'c', 67, 67, False, True),
            'd': KeysTuple('KeyD', 'd', 'd', 'd', 68, 68, False, True),
            'e': KeysTuple('KeyE', 'e', 'e', 'e', 69, 69, False, True),
            'f': KeysTuple('KeyF', 'f', 'f', 'f', 70, 70, False, True),
            'g': KeysTuple('KeyG', 'g', 'g', 'g', 71, 71, False, True),
            'h': KeysTuple('KeyH', 'h', 'h', 'h', 72, 72, False, True),
            'i': KeysTuple('KeyI', 'i', 'i', 'i', 73, 73, False, True),
            'j': KeysTuple('KeyJ', 'j', 'j', 'j', 74, 74, False, True),
            'k': KeysTuple('KeyK', 'k', 'k', 'k', 75, 75, False, True),
            'l': KeysTuple('KeyL', 'l', 'l', 'l', 76, 76, False, True),
            'm': KeysTuple('KeyM', 'm', 'm', 'm', 77, 77, False, True),
            'n': KeysTuple('KeyN', 'n', 'n', 'n', 78, 78, False, True),
            'o': KeysTuple('KeyO', 'o', 'o', 'o', 79, 79, False, True),
            'p': KeysTuple('KeyP', 'p', 'p', 'p', 80, 80, False, True),
            'q': KeysTuple('KeyQ', 'q', 'q', 'q', 81, 81, False, True),
            'r': KeysTuple('KeyR', 'r', 'r', 'r', 82, 82, False, True),
            's': KeysTuple('KeyS', 's', 's', 's', 83, 83, False, True),
            't': KeysTuple('KeyT', 't', 't', 't', 84, 84, False, True),
            'u': KeysTuple('KeyU', 'u', 'u', 'u', 85, 85, False, True),
            'v': KeysTuple('KeyV', 'v', 'v', 'v', 86, 86, False, True),
            'w': KeysTuple('KeyW', 'w', 'w', 'w', 87, 87, False, True),
            'x': KeysTuple('KeyX', 'x', 'x', 'x', 88, 88, False, True),
            'y': KeysTuple('KeyY', 'y', 'y', 'y', 89, 89, False, True),
            'z': KeysTuple('KeyZ', 'z', 'z', 'z', 90, 90, False, True),
            '[': KeysTuple('BracketLeft', '[', '[', '[', 219, 219, False, True),
            '\\': KeysTuple('Backslash', '\\', '\\', '\\', 220, 220, False, True),
            ']': KeysTuple('BracketRight', ']', ']', ']', 221, 221, False, True),
            '~': KeysTuple('Backquote', '~', '~', '`', 192, 192, True, True),
            '\u007f': KeysTuple('Delete', 'Delete', None, None, 46, 46, False, False),
            '¥': KeysTuple('IntlYen', '¥', '¥', '¥', 220, 220, False, True),
            '\u0102': KeysTuple('AltLeft', 'Alt', None, None, 164, 164, False, False),
            '\u0104': KeysTuple('CapsLock', 'CapsLock', None, None, 20, 20, False, False),
            '\u0105': KeysTuple('ControlLeft', 'Control', None, None, 162, 162, False, False),
            '\u0106': KeysTuple('Fn', 'Fn', None, None, 0, 0, False, False),
            '\u0107': KeysTuple('FnLock', 'FnLock', None, None, 0, 0, False, False),
            '\u0108': KeysTuple('Hyper', 'Hyper', None, None, 0, 0, False, False),
            '\u0109': KeysTuple('MetaLeft', 'Meta', None, None, 91, 91, False, False),
            '\u010a': KeysTuple('NumLock', 'NumLock', None, None, 144, 144, False, False),
            '\u010c': KeysTuple('ScrollLock', 'ScrollLock', None, None, 145, 145, False, False),
            '\u010d': KeysTuple('ShiftLeft', 'Shift', None, None, 160, 160, False, False),
            '\u010e': KeysTuple('Super', 'Super', None, None, 0, 0, False, False),
            '\u0301': KeysTuple('ArrowDown', 'ArrowDown', None, None, 40, 40, False, False),
            '\u0302': KeysTuple('ArrowLeft', 'ArrowLeft', None, None, 37, 37, False, False),
            '\u0303': KeysTuple('ArrowRight', 'ArrowRight', None, None, 39, 39, False, False),
            '\u0304': KeysTuple('ArrowUp', 'ArrowUp', None, None, 38, 38, False, False),
            '\u0305': KeysTuple('End', 'End', None, None, 35, 35, False, False),
            '\u0306': KeysTuple('Home', 'Home', None, None, 36, 36, False, False),
            '\u0307': KeysTuple('PageDown', 'PageDown', None, None, 34, 34, False, False),
            '\u0308': KeysTuple('PageUp', 'PageUp', None, None, 33, 33, False, False),
            '\u0401': KeysTuple('NumpadClear', 'Clear', None, None, 12, 12, False, False),
            '\u0402': KeysTuple('Copy', 'Copy', None, None, 0, 0, False, False),
            '\u0404': KeysTuple('Cut', 'Cut', None, None, 0, 0, False, False),
            '\u0407': KeysTuple('Insert', 'Insert', None, None, 45, 45, False, False),
            '\u0408': KeysTuple('Paste', 'Paste', None, None, 0, 0, False, False),
            '\u0409': KeysTuple('Redo', 'Redo', None, None, 0, 0, False, False),
            '\u040a': KeysTuple('Undo', 'Undo', None, None, 0, 0, False, False),
            '\u0502': KeysTuple('Again', 'Again', None, None, 0, 0, False, False),
            '\u0504': KeysTuple('Abort', 'Cancel', None, None, 0, 0, False, False),
            '\u0505': KeysTuple('ContextMenu', 'ContextMenu', None, None, 93, 93, False, False),
            '\u0507': KeysTuple('Find', 'Find', None, None, 0, 0, False, False),
            '\u0508': KeysTuple('Help', 'Help', None, None, 47, 47, False, False),
            '\u0509': KeysTuple('Pause', 'Pause', None, None, 19, 19, False, False),
            '\u050b': KeysTuple('Props', 'Props', None, None, 0, 0, False, False),
            '\u050c': KeysTuple('Select', 'Select', None, None, 41, 41, False, False),
            '\u050d': KeysTuple('ZoomIn', 'ZoomIn', None, None, 0, 0, False, False),
            '\u050e': KeysTuple('ZoomOut', 'ZoomOut', None, None, 0, 0, False, False),
            '\u0601': KeysTuple('BrightnessDown', 'BrightnessDown', None, None, 216, 0, False, False),
            '\u0602': KeysTuple('BrightnessUp', 'BrightnessUp', None, None, 217, 0, False, False),
            '\u0604': KeysTuple('Eject', 'Eject', None, None, 0, 0, False, False),
            '\u0605': KeysTuple('LogOff', 'LogOff', None, None, 0, 0, False, False),
            '\u0606': KeysTuple('Power', 'Power', None, None, 152, 0, False, False),
            '\u0608': KeysTuple('PrintScreen', 'PrintScreen', None, None, 44, 44, False, False),
            '\u060b': KeysTuple('WakeUp', 'WakeUp', None, None, 0, 0, False, False),
            '\u0705': KeysTuple('Convert', 'Convert', None, None, 28, 28, False, False),
            '\u070d': KeysTuple('NonConvert', 'NonConvert', None, None, 29, 29, False, False),
            '\u0711': KeysTuple('Lang1', 'HangulMode', None, None, 21, 21, False, False),
            '\u0712': KeysTuple('Lang2', 'HanjaMode', None, None, 25, 25, False, False),
            '\u0716': KeysTuple('Lang4', 'Hiragana', None, None, 0, 0, False, False),
            '\u0718': KeysTuple('KanaMode', 'KanaMode', None, None, 21, 21, False, False),
            '\u071a': KeysTuple('Lang3', 'Katakana', None, None, 0, 0, False, False),
            '\u071d': KeysTuple('Lang5', 'ZenkakuHankaku', None, None, 0, 0, False, False),
            '\u0801': KeysTuple('F1', 'F1', None, None, 112, 112, False, False),
            '\u0802': KeysTuple('F2', 'F2', None, None, 113, 113, False, False),
            '\u0803': KeysTuple('F3', 'F3', None, None, 114, 114, False, False),
            '\u0804': KeysTuple('F4', 'F4', None, None, 115, 115, False, False),
            '\u0805': KeysTuple('F5', 'F5', None, None, 116, 116, False, False),
            '\u0806': KeysTuple('F6', 'F6', None, None, 117, 117, False, False),
            '\u0807': KeysTuple('F7', 'F7', None, None, 118, 118, False, False),
            '\u0808': KeysTuple('F8', 'F8', None, None, 119, 119, False, False),
            '\u0809': KeysTuple('F9', 'F9', None, None, 120, 120, False, False),
            '\u080a': KeysTuple('F10', 'F10', None, None, 121, 121, False, False),
            '\u080b': KeysTuple('F11', 'F11', None, None, 122, 122, False, False),
            '\u080c': KeysTuple('F12', 'F12', None, None, 123, 123, False, False),
            '\u080d': KeysTuple('F13', 'F13', None, None, 124, 124, False, False),
            '\u080e': KeysTuple('F14', 'F14', None, None, 125, 125, False, False),
            '\u080f': KeysTuple('F15', 'F15', None, None, 126, 126, False, False),
            '\u0810': KeysTuple('F16', 'F16', None, None, 127, 127, False, False),
            '\u0811': KeysTuple('F17', 'F17', None, None, 128, 128, False, False),
            '\u0812': KeysTuple('F18', 'F18', None, None, 129, 129, False, False),
            '\u0813': KeysTuple('F19', 'F19', None, None, 130, 130, False, False),
            '\u0814': KeysTuple('F20', 'F20', None, None, 131, 131, False, False),
            '\u0815': KeysTuple('F21', 'F21', None, None, 132, 132, False, False),
            '\u0816': KeysTuple('F22', 'F22', None, None, 133, 133, False, False),
            '\u0817': KeysTuple('F23', 'F23', None, None, 134, 134, False, False),
            '\u0818': KeysTuple('F24', 'F24', None, None, 135, 135, False, False),
            '\u0a01': KeysTuple('Close', 'Close', None, None, 0, 0, False, False),
            '\u0a02': KeysTuple('MailForward', 'MailForward', None, None, 0, 0, False, False),
            '\u0a03': KeysTuple('MailReply', 'MailReply', None, None, 0, 0, False, False),
            '\u0a04': KeysTuple('MailSend', 'MailSend', None, None, 0, 0, False, False),
            '\u0a05': KeysTuple('MediaPlayPause', 'MediaPlayPause', None, None, 179, 179, False, False),
            '\u0a07': KeysTuple('MediaStop', 'MediaStop', None, None, 178, 178, False, False),
            '\u0a08': KeysTuple('MediaTrackNext', 'MediaTrackNext', None, None, 176, 176, False, False),
            '\u0a09': KeysTuple('MediaTrackPrevious', 'MediaTrackPrevious', None, None, 177, 177, False, False),
            '\u0a0a': KeysTuple('New', 'New', None, None, 0, 0, False, False),
            '\u0a0b': KeysTuple('Open', 'Open', None, None, 43, 43, False, False),
            '\u0a0c': KeysTuple('Print', 'Print', None, None, 0, 0, False, False),
            '\u0a0d': KeysTuple('Save', 'Save', None, None, 0, 0, False, False),
            '\u0a0e': KeysTuple('SpellCheck', 'SpellCheck', None, None, 0, 0, False, False),
            '\u0a0f': KeysTuple('AudioVolumeDown', 'AudioVolumeDown', None, None, 174, 174, False, False),
            '\u0a10': KeysTuple('AudioVolumeUp', 'AudioVolumeUp', None, None, 175, 175, False, False),
            '\u0a11': KeysTuple('AudioVolumeMute', 'AudioVolumeMute', None, None, 173, 173, False, False),
            '\u0b01': KeysTuple('LaunchApp2', 'LaunchApplication2', None, None, 183, 183, False, False),
            '\u0b02': KeysTuple('LaunchCalendar', 'LaunchCalendar', None, None, 0, 0, False, False),
            '\u0b03': KeysTuple('LaunchMail', 'LaunchMail', None, None, 180, 180, False, False),
            '\u0b04': KeysTuple('MediaSelect', 'LaunchMediaPlayer', None, None, 181, 181, False, False),
            '\u0b05': KeysTuple('LaunchMusicPlayer', 'LaunchMusicPlayer', None, None, 0, 0, False, False),
            '\u0b06': KeysTuple('LaunchApp1', 'LaunchApplication1', None, None, 182, 182, False, False),
            '\u0b07': KeysTuple('LaunchScreenSaver', 'LaunchScreenSaver', None, None, 0, 0, False, False),
            '\u0b08': KeysTuple('LaunchSpreadsheet', 'LaunchSpreadsheet', None, None, 0, 0, False, False),
            '\u0b09': KeysTuple('LaunchWebBrowser', 'LaunchWebBrowser', None, None, 0, 0, False, False),
            '\u0b0c': KeysTuple('LaunchContacts', 'LaunchContacts', None, None, 0, 0, False, False),
            '\u0b0d': KeysTuple('LaunchPhone', 'LaunchPhone', None, None, 0, 0, False, False),
            '\u0c01': KeysTuple('BrowserBack', 'BrowserBack', None, None, 166, 166, False, False),
            '\u0c02': KeysTuple('BrowserFavorites', 'BrowserFavorites', None, None, 171, 171, False, False),
            '\u0c03': KeysTuple('BrowserForward', 'BrowserForward', None, None, 167, 167, False, False),
            '\u0c04': KeysTuple('BrowserHome', 'BrowserHome', None, None, 172, 172, False, False),
            '\u0c05': KeysTuple('BrowserRefresh', 'BrowserRefresh', None, None, 168, 168, False, False),
            '\u0c06': KeysTuple('BrowserSearch', 'BrowserSearch', None, None, 170, 170, False, False),
            '\u0c07': KeysTuple('BrowserStop', 'BrowserStop', None, None, 169, 169, False, False),
            '\u0d0a': KeysTuple('ChannelDown', 'ChannelDown', None, None, 0, 0, False, False),
            '\u0d0b': KeysTuple('ChannelUp', 'ChannelUp', None, None, 0, 0, False, False),
            '\u0d12': KeysTuple('ClosedCaptionToggle', 'ClosedCaptionToggle', None, None, 0, 0, False, False),
            '\u0d15': KeysTuple('Exit', 'Exit', None, None, 0, 0, False, False),
            '\u0d22': KeysTuple('Guide', 'Guide', None, None, 0, 0, False, False),
            '\u0d25': KeysTuple('Info', 'Info', None, None, 0, 0, False, False),
            '\u0d2c': KeysTuple('MediaFastForward', 'MediaFastForward', None, None, 0, 0, False, False),
            '\u0d2d': KeysTuple('MediaLast', 'MediaLast', None, None, 0, 0, False, False),
            '\u0d2f': KeysTuple('MediaPlay', 'MediaPlay', None, None, 0, 0, False, False),
            '\u0d30': KeysTuple('MediaRecord', 'MediaRecord', None, None, 0, 0, False, False),
            '\u0d31': KeysTuple('MediaRewind', 'MediaRewind', None, None, 0, 0, False, False),
            '\u0d43': KeysTuple('Settings', 'Settings', None, None, 0, 0, False, False),
            '\u0d4e': KeysTuple('ZoomToggle', 'ZoomToggle', None, None, 251, 251, False, False),
            '\u0e02': KeysTuple('AudioBassBoostToggle', 'AudioBassBoostToggle', None, None, 0, 0, False, False),
            '\u0f02': KeysTuple('SpeechInputToggle', 'SpeechInputToggle', None, None, 0, 0, False, False),
            '\u1001': KeysTuple('SelectTask', 'AppSwitch', None, None, 0, 0, False, False),
        }
keyboard.helpers.BACKSPACE = keyboard.helpers.buttons['\b']
keyboard.helpers.TAB = keyboard.helpers.buttons['\t']
keyboard.helpers.ENTER = keyboard.helpers.buttons['\r']
keyboard.helpers.ESCAPE = keyboard.helpers.buttons['\u001b']
keyboard.helpers.QUOTE = keyboard.helpers.buttons['\'']
keyboard.helpers.BACKSLASH = keyboard.helpers.buttons['\\']
keyboard.helpers.DELETE = keyboard.helpers.buttons['\u007f']
keyboard.helpers.ALT = keyboard.helpers.buttons['\u0102']
keyboard.helpers.CAPS_LOCK = keyboard.helpers.buttons['\u0104']
keyboard.helpers.CONTROL = keyboard.helpers.buttons['\u0105']
keyboard.helpers.FN = keyboard.helpers.buttons['\u0106']
keyboard.helpers.FN_LOCK = keyboard.helpers.buttons['\u0107']
keyboard.helpers.HYPER = keyboard.helpers.buttons['\u0108']
keyboard.helpers.META = keyboard.helpers.buttons['\u0109']
keyboard.helpers.NUM_LOCK = keyboard.helpers.buttons['\u010a']
keyboard.helpers.SCROLL_LOCK = keyboard.helpers.buttons['\u010c']
keyboard.helpers.SHIFT = keyboard.helpers.buttons['\u010d']
keyboard.helpers.SUPER = keyboard.helpers.buttons['\u010e']
keyboard.helpers.ARROW_DOWN = keyboard.helpers.buttons['\u0301']
keyboard.helpers.ARROW_LEFT = keyboard.helpers.buttons['\u0302']
keyboard.helpers.ARROW_RIGHT = keyboard.helpers.buttons['\u0303']
keyboard.helpers.ARROW_UP = keyboard.helpers.buttons['\u0304']
keyboard.helpers.END = keyboard.helpers.buttons['\u0305']
keyboard.helpers.HOME = keyboard.helpers.buttons['\u0306']
keyboard.helpers.PAGE_DOWN = keyboard.helpers.buttons['\u0307']
keyboard.helpers.PAGE_UP = keyboard.helpers.buttons['\u0308']
keyboard.helpers.CLEAR = keyboard.helpers.buttons['\u0401']
keyboard.helpers.COPY = keyboard.helpers.buttons['\u0402']
keyboard.helpers.CUT = keyboard.helpers.buttons['\u0404']
keyboard.helpers.INSERT = keyboard.helpers.buttons['\u0407']
keyboard.helpers.PASTE = keyboard.helpers.buttons['\u0408']
keyboard.helpers.REDO = keyboard.helpers.buttons['\u0409']
keyboard.helpers.UNDO = keyboard.helpers.buttons['\u040a']
keyboard.helpers.AGAIN = keyboard.helpers.buttons['\u0502']
keyboard.helpers.CANCEL = keyboard.helpers.buttons['\u0504']
keyboard.helpers.CONTEXT_MENU = keyboard.helpers.buttons['\u0505']
keyboard.helpers.FIND = keyboard.helpers.buttons['\u0507']
keyboard.helpers.HELP = keyboard.helpers.buttons['\u0508']
keyboard.helpers.PAUSE = keyboard.helpers.buttons['\u0509']
keyboard.helpers.PROPS = keyboard.helpers.buttons['\u050b']
keyboard.helpers.SELECT = keyboard.helpers.buttons['\u050c']
keyboard.helpers.ZOOM_IN = keyboard.helpers.buttons['\u050d']
keyboard.helpers.ZOOM_OUT = keyboard.helpers.buttons['\u050e']
keyboard.helpers.BRIGHTNESS_DOWN = keyboard.helpers.buttons['\u0601']
keyboard.helpers.BRIGHTNESS_UP = keyboard.helpers.buttons['\u0602']
keyboard.helpers.EJECT = keyboard.helpers.buttons['\u0604']
keyboard.helpers.LOG_OFF = keyboard.helpers.buttons['\u0605']
keyboard.helpers.POWER = keyboard.helpers.buttons['\u0606']
keyboard.helpers.PRINT_SCREEN = keyboard.helpers.buttons['\u0608']
keyboard.helpers.WAKE_UP = keyboard.helpers.buttons['\u060b']
keyboard.helpers.CONVERT = keyboard.helpers.buttons['\u0705']
keyboard.helpers.NON_CONVERT = keyboard.helpers.buttons['\u070d']
keyboard.helpers.HANGUL_MODE = keyboard.helpers.buttons['\u0711']
keyboard.helpers.HANJA_MODE = keyboard.helpers.buttons['\u0712']
keyboard.helpers.HIRAGANA = keyboard.helpers.buttons['\u0716']
keyboard.helpers.KANA_MODE = keyboard.helpers.buttons['\u0718']
keyboard.helpers.KATAKANA = keyboard.helpers.buttons['\u071a']
keyboard.helpers.ZENKAKU_HANKAKU = keyboard.helpers.buttons['\u071d']
keyboard.helpers.F1 = keyboard.helpers.buttons['\u0801']
keyboard.helpers.F2 = keyboard.helpers.buttons['\u0802']
keyboard.helpers.F3 = keyboard.helpers.buttons['\u0803']
keyboard.helpers.F4 = keyboard.helpers.buttons['\u0804']
keyboard.helpers.F5 = keyboard.helpers.buttons['\u0805']
keyboard.helpers.F6 = keyboard.helpers.buttons['\u0806']
keyboard.helpers.F7 = keyboard.helpers.buttons['\u0807']
keyboard.helpers.F8 = keyboard.helpers.buttons['\u0808']
keyboard.helpers.F9 = keyboard.helpers.buttons['\u0809']
keyboard.helpers.F10 = keyboard.helpers.buttons['\u080a']
keyboard.helpers.F11 = keyboard.helpers.buttons['\u080b']
keyboard.helpers.F12 = keyboard.helpers.buttons['\u080c']
keyboard.helpers.F13 = keyboard.helpers.buttons['\u080d']
keyboard.helpers.F14 = keyboard.helpers.buttons['\u080e']
keyboard.helpers.F15 = keyboard.helpers.buttons['\u080f']
keyboard.helpers.F16 = keyboard.helpers.buttons['\u0810']
keyboard.helpers.F17 = keyboard.helpers.buttons['\u0811']
keyboard.helpers.F18 = keyboard.helpers.buttons['\u0812']
keyboard.helpers.F19 = keyboard.helpers.buttons['\u0813']
keyboard.helpers.F20 = keyboard.helpers.buttons['\u0814']
keyboard.helpers.F21 = keyboard.helpers.buttons['\u0815']
keyboard.helpers.F22 = keyboard.helpers.buttons['\u0816']
keyboard.helpers.F23 = keyboard.helpers.buttons['\u0817']
keyboard.helpers.F24 = keyboard.helpers.buttons['\u0818']
keyboard.helpers.CLOSE = keyboard.helpers.buttons['\u0a01']
keyboard.helpers.MAIL_FORWARD = keyboard.helpers.buttons['\u0a02']
keyboard.helpers.MAIL_REPLY = keyboard.helpers.buttons['\u0a03']
keyboard.helpers.MAIL_SEND = keyboard.helpers.buttons['\u0a04']
keyboard.helpers.MEDIA_PLAY_PAUSE = keyboard.helpers.buttons['\u0a05']
keyboard.helpers.MEDIA_STOP = keyboard.helpers.buttons['\u0a07']
keyboard.helpers.MEDIA_TRACK_NEXT = keyboard.helpers.buttons['\u0a08']
keyboard.helpers.MEDIA_TRACK_PREVIOUS   = keyboard.helpers.buttons['\u0a09']
keyboard.helpers.NEW = keyboard.helpers.buttons['\u0a0a']
keyboard.helpers.OPEN = keyboard.helpers.buttons['\u0a0b']
keyboard.helpers.PRINT = keyboard.helpers.buttons['\u0a0c']
keyboard.helpers.SAVE = keyboard.helpers.buttons['\u0a0d']
keyboard.helpers.SPELL_CHECK = keyboard.helpers.buttons['\u0a0e']
keyboard.helpers.AUDIO_VOLUME_DOWN = keyboard.helpers.buttons['\u0a0f']
keyboard.helpers.AUDIO_VOLUME_UP = keyboard.helpers.buttons['\u0a10']
keyboard.helpers.AUDIO_VOLUME_MUTE = keyboard.helpers.buttons['\u0a11']
keyboard.helpers.LAUMCH_APPLICATION_2 = keyboard.helpers.buttons['\u0b01']
keyboard.helpers.LAUNCH_CALENDAT = keyboard.helpers.buttons['\u0b02']
keyboard.helpers.LAUNCH_MAIL = keyboard.helpers.buttons['\u0b03']
keyboard.helpers.LAUNCH_MEDIA_PLAYER = keyboard.helpers.buttons['\u0b04']
keyboard.helpers.LAUNCH_MUSIC_PLAYER = keyboard.helpers.buttons['\u0b05']
keyboard.helpers.LAUNCH_APPLICATION_1   = keyboard.helpers.buttons['\u0b06']
keyboard.helpers.LAUNCH_SCREEN_SAVER = keyboard.helpers.buttons['\u0b07']
keyboard.helpers.LAUNCH_SPREADSHEET = keyboard.helpers.buttons['\u0b08']
keyboard.helpers.LAUNCH_WEB_BROWSER = keyboard.helpers.buttons['\u0b09']
keyboard.helpers.LAUNCH_CONTACTS = keyboard.helpers.buttons['\u0b0c']
keyboard.helpers.LAUNCH_PHONE = keyboard.helpers.buttons['\u0b0d']
keyboard.helpers.BROWSER_BACK = keyboard.helpers.buttons['\u0c01']
keyboard.helpers.BROWSER_FAVORITES = keyboard.helpers.buttons['\u0c02']
keyboard.helpers.BROWSER_FORWARD = keyboard.helpers.buttons['\u0c03']
keyboard.helpers.BROWSER_HOME = keyboard.helpers.buttons['\u0c04']
keyboard.helpers.BROWSER_REFRESH = keyboard.helpers.buttons['\u0c05']
keyboard.helpers.BROWSER_SEARCH = keyboard.helpers.buttons['\u0c06']
keyboard.helpers.BROWSER_STOP = keyboard.helpers.buttons['\u0c07']
keyboard.helpers.CHANNEL_DOWN = keyboard.helpers.buttons['\u0d0a']
keyboard.helpers.CHANNEL_UP = keyboard.helpers.buttons['\u0d0b']
keyboard.helpers.CLOSED_CAPTION_TOGGLE = keyboard.helpers.buttons['\u0d12']
keyboard.helpers.EXIT = keyboard.helpers.buttons['\u0d15']
keyboard.helpers.GUIDE = keyboard.helpers.buttons['\u0d22']
keyboard.helpers.INFO = keyboard.helpers.buttons['\u0d25']
keyboard.helpers.MEDIA_FAST_FORWARD = keyboard.helpers.buttons['\u0d2c']
keyboard.helpers.MEDIA_LAST = keyboard.helpers.buttons['\u0d2d']
keyboard.helpers.MEDIA_PLAY = keyboard.helpers.buttons['\u0d2f']
keyboard.helpers.MEDIA_RECORD = keyboard.helpers.buttons['\u0d30']
keyboard.helpers.MEDIA_REWIND = keyboard.helpers.buttons['\u0d31']
keyboard.helpers.SETTINGS = keyboard.helpers.buttons['\u0d43']
keyboard.helpers.ZOOM_TOGGLE = keyboard.helpers.buttons['\u0d4e']
keyboard.helpers.AUDIO_BASS_BOOST_TOGGLE = keyboard.helpers.buttons['\u0e02']
keyboard.helpers.SPEECH_INPUT_TOGGLE = keyboard.helpers.buttons['\u0f02']
keyboard.helpers.APP_SWITCH = keyboard.helpers.buttons['\u1001']
class modifiers(dict):
    ALT = 1
    CTRL = 2
    META = 4
    COMMAND = 4
    SHIFT = 8
    def __init__(self):
        super().__init__()
        for key in filter(lambda x: not x.startswith('_') and x.isupper(), dir(self)):
            self[key] = getattr(self, key)
    def __call__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            args = args[0]
        result = 0
        for flag in set(args):
            result ^= flag
        return result
keyboard.helpers.modifiers = modifiers()
class types(list):
    KEY_DOWN = 'keyDown'
    KEY_UP = 'keyUp'
    RAW_KEY_DOWN = 'rawKeyDown'
    CHAR = 'char'
    def __init__(self):
        super().__init__()
        self.extend(filter(lambda x: not x.startswith('_') and x.isupper(), dir(self)))
keyboard.helpers.types = types()




class dom:
    '''
    DOM handling
    '''
    async def _load_dom_tree(tabs, tab, root):
        kv = {}
        async def extract(element):
            tab._emit_event('dom__new_node_found', node=element)
            kv[element.nodeId] = element
            if element.children is not None:
                for child in element.children:
                    await extract(child)
            if element.contentDocument is not None:
                await extract(element.contentDocument)
            if element.shadowRoots is not None:
                for shadow in element.shadowRoots:
                    await extract(shadow)
            if element.templateContent is not None:
                await extract(element.templateContent)
            if element.pseudoElements is not None:
                for pseudo in element.pseudoElements:
                    await extract(pseudo)
            if element.importedDocument is not None:
                await extract(element.importedDocument)
        await extract(root)
        return kv
    class events:
        async def tab_start(tabs, tab):
            await tab.DOM.enable()
            async with tab.lock('dom'):
                tab.dom_kv = await dom._load_dom_tree(tabs, tab, await tab.DOM.get_document(depth=-1, pierce=True))
        async def dom__document_updated(tabs, tab):
            async with tab.lock('dom'):
                tab.dom_kv = await dom._load_dom_tree(tabs, tab, await tab.DOM.get_document(depth=-1, pierce=True))
        async def dom__set_child_nodes(tabs, tab, parentId, nodes): # ???????
            async with tab.lock('dom'):
                tab.dom_kv[parentId].children = nodes
                for node in nodes:
                    tab.dom_kv.update(await dom._load_dom_tree(tabs, tab, node))
        async def dom__attribute_modified(tabs, tab, nodeId, name, value):
            async with tab.lock('dom'):
                attributes = tab.dom_kv[nodeId].attributes
                try:
                    attributes[attributes.index(name) + 1] = value
                except ValueError:
                    attributes += [name, value]
        async def dom__attribute_removed(tabs, tab, nodeId, name):
            async with tab.lock('dom'):
                attributes = tab.dom_kv[nodeId].attributes
                index = attributes.index(name)
                attributes.pop(index)
                attributes.pop(index)
        async def dom__inline_style_invalidated(tabs, tab, nodeIds):
            async with tab.lock('dom'):
                coroutines = []
                for nodeId in nodeIds:
                    coroutines.append(tab.DOM.get_attributes(nodeId))
                if len(coroutines) > 0:
                    results, _ = await asyncio.wait(coroutines)
                    for nodeId, result in zip(nodeIds, results):
                        tab.dom_kv[nodeId].attributes = result.result()
        async def dom__character_data_modified(tabs, tab, nodeId, characterData):
            async with tab.lock('dom'):
                tab.dom_kv[nodeId].nodeValue = characterData
        async def dom__child_node_count_updated(tabs, tab, nodeId, childNodeCount):
            async with tab.lock('dom'):
                tab.dom_kv[nodeId].childNodeCount = childNodeCount
        async def dom__child_node_inserted(tabs, tab, parentNodeId, previousNodeId, node):
            async with tab.lock('dom'):
                index = 0
                children = tab.dom_kv[parentNodeId].children
                if children is None:
                    tab.dom_kv[parentNodeId].children = [node]
                else:
                    current_index = 0
                    for child in children:
                        if child.nodeId == previousNodeId:
                            index = current_index + 1
                            break
                        current_index += 1
                    children.insert(index, node)
                tab.dom_kv.update(await dom._load_dom_tree(tabs, tab, node))
        async def dom__child_node_removed(tabs, tab, parentNodeId, nodeId):
            async with tab.lock('dom'):
                children = tab.dom_kv[parentNodeId].children
                index = None
                current_index = 0
                for child in children:
                    if child.nodeId == nodeId:
                        index = current_index
                        break
                    current_index += 1
                children.pop(index)
        async def dom__shadow_root_pushed(tabs, tab, hostId, root):
            async with tab.lock('dom'):
                shadowRoots = tab.dom_kv[hostId].shadowRoots
                if shadowRoots is None:
                    tab.dom_kv[hostId].shadowRoots = [root]
                else:
                    shadowRoots.append(root)
                tab.dom_kv.update(await dom._load_dom_tree(tabs, tab, root))
        async def dom__shadow_root_popped(tabs, tab, hostId, rootId):
            async with tab.lock('dom'):
                shadowRoots = tab.dom_kv[hostId].shadowRoots
                index = None
                current_index = 0
                for shadow in shadowRoots:
                    if shadow.nodeId == rootId:
                        index = current_index
                        break
                    current_index += 1
                shadowRoots.pop(index)
        async def dom__pseudo_element_added(tabs, tab, parentId, pseudoElement):
            async with tab.lock('dom'):
                pseudoElements = tab.dom_kv[parentId].pseudoElements
                if pseudoElements is None:
                    tab.dom_kv[parentId].pseudoElements = [pseudoElement]
                else:
                    pseudoElements.append(pseudoElement)
                tab.dom_kv.update(await dom._load_dom_tree(tabs, tab, pseudoElement))
        async def dom__pseudo_element_removed(tabs, tab, parentId, pseudoElementId):
            async with tab.lock('dom'):
                index = None
                pseudoElements = tab.dom_kv[parentId].pseudoElements
                current_index = 0
                for child in pseudoElements:
                    if child.nodeId == pseudoElementId:
                        index = current_index
                    current_index += 1
                del pseudoElements[index]
        async def dom__distributed_nodes_updated(tabs, tab, insertionPointId, distributedNodes):
            async with tab.lock('dom'):
                tab.dom_kv[insertionPointId].distributedNodes = distributedNodes




class old_helpers:
    class helpers:
        def unpack_response_body(packed):
            result = packed['body']
            if packed['base64Encoded']:
                result = base64.b64decode(result)
            return result






