import asyncio, socket

cnt = 0
game_dict = {}


async def echo_server(reader, writer):
    global cnt
    cnt += 1
    print(f"Total connections: {cnt}")

    game_id = (cnt - 1) // 2
    if cnt % 2 == 1:
        game_dict[game_id] = (reader, writer)
    else:
        game_dict[game_id] = (game_dict[game_id], (reader, writer))
    print(f"game_dict[{game_id}] = {game_dict[game_id]}")

    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            writer.close()
            break
        writer.write(data)
        await writer.drain()  # Flow control, see later


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    print(f"Server started with {host}:{port}")
    await server.serve_forever()


asyncio.run(main('192.168.3.10', 5000))

# import asyncio
#
# async def handle_echo(reader, writer):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')
#
#     print(f"Received {message!r} from {addr!r}")
#
#     print(f"Send: {message!r}")
#     writer.write(data)
#     await writer.drain()
#
#     print("Close the connection")
#     writer.close()
#
# async def main():
#     server = await asyncio.start_server(
#         handle_echo, '192.168.3.10', 8888)
#
#     addr = server.sockets[0].getsockname()
#     print(f'Serving on {addr}')
#
#     async with server:
#         await server.serve_forever()
#
# asyncio.run(main())