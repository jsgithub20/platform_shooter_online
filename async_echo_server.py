import asyncio


async def handle_echo(reader, writer):
    running = True
    data = ""
    while running:
        try:
            data = await reader.readuntil(separator=b"||")
            print(data.decode())
            message = data.decode()[:-2]
            addr = writer.get_extra_info('peername')

            print(f"Received {message!r} from {addr!r}")

            print(f"Send: {message!r}")
            writer.write(data)
            await writer.drain()
        except (ConnectionError, asyncio.IncompleteReadError):
            writer.close()
            running = False
            print("connection lost")


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


asyncio.run(main())