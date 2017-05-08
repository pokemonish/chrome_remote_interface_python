import asyncio, sys, lib

if __name__ == '__main__':
    class callbacks:
        async def start(tabs):
            tab = await tabs.add()
            await tab.Page.enable()
            await tab.Network.enable()
            await tab.Page.navigate(url='http://example.com')
        async def network__response_received(tabs, tab, requestId, **kwargs):
            body = lib.helpers.unpack_response_body(await tab.Network.get_response_body(requestId=requestId))
            print(body)
        async def any(tabs, tab, callback_name, parameters):
            print('Unknown event fired', callback_name)

    asyncio.get_event_loop().run_until_complete(lib.Tabs.run('localhost', 9222, callbacks))


