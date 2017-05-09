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
                print('body length:', len(body))
            except tabs.FailReponse as e:
                print('fail:', e)
        async def network__loading_finished(tabs, tab, **kwargs):
            print('finish')
            tabs.terminate()
        async def any(tabs, tab, callback_name, parameters):
            pass
            # print('Unknown event fired', callback_name)

    asyncio.get_event_loop().run_until_complete(chrome_remote_interface.Tabs.run('localhost', 9222, callbacks))