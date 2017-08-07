#
# asynchronous.py
#

import time
import asyncio
import aiohttp


async def fetch(address, url):

    print('DEBUG: Fetching URL {} for {}.'.format(url, address))

    connector = aiohttp.TCPConnector(verify_ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            content = await response.text()
            return url, content


async def producer(sink, url, content):

    sink.write('URL: {}'.format(url).encode())
    sink.write('Content: '.encode())
    sink.write(content.encode())


async def consume(address, port, loop):

    async def handler(reader, writer):

        addr = writer.get_extra_info('peername')
        addr = '{}:{}'.format(addr[0], addr[1])

        print('DEBUG: new connection from {}.'.format(addr))

        urls = await reader.read()
        urls = urls.decode()
        urls = [u.rstrip('\n') for u in urls.split('\n') if u]

        start = time.time()

        tasks = [loop.create_task(fetch(addr, u)) for u in urls]

        results = await asyncio.gather(*tasks)

        for url, content in results:
            await producer(writer, url, content)

        await writer.drain()

        end = time.time()

        print('DEBUG: closing connection with {}.'.format(addr))
        print('DEBUG: Total time: {:0.2f} seconds.'.format(end - start))

        writer.close()

    return await asyncio.start_server(handler, address, port)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    server = consume('127.0.0.1', 9990, loop)
    loop.create_task(server)

    print('DEBUG: Starting event loop.')

    loop.run_forever()