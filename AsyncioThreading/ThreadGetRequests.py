import aiohttp
import asyncio

class ThreadingGetRequests(object):

    def __init__(self,urls):
        # Pass Your Thread request here
        self.urls = [
                'http://python.org',
                'https://google.com',
                'http://yifei.me'
            ]
    
    
    def startThreading(self):
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def main():
            tasks = []
            async with aiohttp.ClientSession() as session:
                for url in self.urls:
                    print(url)
                    tasks.append(fetch(session, url))
                htmls = await asyncio.gather(*tasks)

                for html in htmls:
                    print("******")
                    print(html[:100])
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())    

ob=ThreadingGetRequests(urls=['Kshitiz','Sharma'])
ob.startThreading()

