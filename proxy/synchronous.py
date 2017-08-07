#
# synchronous.py
#

import time
import socket
import requests


def consumer(address, port):

    # Create a simple TCP socket which will accept client connections.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((address, port))
        server.listen(20)

        # Accept client connections. Each connection will be yielded back
        # to the caller.

        while True:
            # BLOCKS
            sock, addr = server.accept()

            addr = '{}:{}'.format(addr[0], addr[1])

            print('DEBUG: new connection from {}.'.format(addr))

            start = time.time()

            with sock.makefile(mode='rw') as handle:
                yield addr, handle

            end = time.time()

            print('DEBUG: closing connection with {}.'.format(addr))
            print('DEBUG: Total time: {:0.2f} seconds.'.format(end - start))

            # BLOCKS
            sock.close()


def producer(sink, url, content):

    # BLOCKS
    sink.write('URL: {}'.format(url))
    sink.write('Response:'.format(content))
    sink.write(content)


def fetch(address, url):

    print('DEBUG: Fetching URL {} for {}.'.format(url, address))

    # BLOCKS
    request = requests.get(url)
    response = request.text

    return response


def event_loop():

    # The synchronous event loop. While normally we don't refer to it as an event
    # loop, this is the role it takes.

    print('DEBUG: Starting event loop.')

    # The basic loop:
    #   1. Start the consumer generator to accept and yield clients.
    #   2. Read a URL from the client, one per line.
    #   3. Fetch a URL from the remote site.
    #   4. Send the URL and content back to the client.
    #   5. Go to number step 2.

    for addr, conn in consumer('127.0.0.1', 9990):
        for url in conn:
            url = url.rstrip('\n')
            content = fetch(addr, url)

            producer(conn, url, content)


if __name__ == '__main__':
    event_loop()