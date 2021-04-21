import asyncio, pygame, time

pygame.init()
clock = pygame.time.Clock()
cnt = 0
game_dict = {}


async def echo_server(reader, writer):
    global cnt, game_dict
    cnt += 1
    print(f"Total connections: {cnt}")
    writer.write(str(cnt).encode())

    game_id = (cnt - 1) // 2
    if cnt % 2 == 1:
        game_dict[game_id] = (reader, writer)
        # print(f"game_dict[{game_id}] = {type(game_dict[game_id][-1])}")
    else:
        game_dict[game_id+1] = (reader, writer)
        # print(f"game_dict[{game_id+1}] = {type(game_dict[game_id][-1])}")

    while True:
        # data = input("Msg to be sent to the clients: ").encode()  # Max number of bytes to read
        clock.tick(1)
        data = "server msg".encode()
        if not data:
            writer.close()
            break
        if cnt % 2 == 0:
            if writer == game_dict[game_id][1]:
                return "this task is done"
            game_dict[game_id][1].write(data)
            await game_dict[game_id][1].drain()
            msg0 = await game_dict[game_id][0].read(100)
            print(f"Received {time.strftime('%X')}: '{msg0.decode()}'")
            game_dict[game_id+1][1].write(data)
            await game_dict[game_id+1][1].drain()
            msg1 = await game_dict[game_id+1][0].read(100)
            print(f"Received {time.strftime('%X')}: '{msg1.decode()}'")
        else:
            game_dict[game_id][1].write(data)
            await game_dict[game_id][1].drain()
            msg0 = await game_dict[game_id][0].read(100)
            print(f"Received: '{msg0.decode()}'")


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    print(f"Server started with {host}:{port}")
    await server.serve_forever()


asyncio.run(main('10.31.16.25', 5000))

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