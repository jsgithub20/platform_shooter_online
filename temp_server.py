import asyncio, pygame, time, logging

pygame.init()
cnt = 0
game_dict = {}

# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.basicConfig(format='\x1b[32m%(asctime)s %(levelname)s: %(message)s\x1b[32m', datefmt='%H:%M:%S', level=logging.INFO)


async def new_client(reader, writer):
    global cnt, game_dict
    cnt += 1
    # if cnt == 3:
    #     breakpoint()
    clock = pygame.time.Clock()
    logging.info(f"Total connections: {cnt}")
    writer.write(str(cnt).encode())

    game_id = (cnt - 1) // 2
    if cnt % 2 == 1:
        player_id = 0  # this is the first player in a new game
        game_dict[game_id] = [False, reader, writer]
    else:
        player_id = 1  # this is the 2nd player in a new game
        game_dict[game_id] += [reader, writer]
        game_dict[game_id][0] = True

    while True:
        # data = input("Msg to be sent to the clients: ").encode()  # Max number of bytes to read
        t = clock.tick(1)
        # print(f"Active tasks: {len(asyncio.all_tasks())}")
        data = f"[{t}]server msg: tasks - {len(asyncio.all_tasks())}".encode()
        if not data:
            writer.close()
            break
        if game_dict[game_id][0]:
            if player_id == 1:
                logging.warning(f"Task for connection {cnt} in game_id {game_id} is being returned")
                return
            game_dict[game_id][2].write(data)
            # await game_dict[game_id][2].drain()
            msg0 = await game_dict[game_id][1].read(100)
            logging.info(f"Received {time.strftime('%X')}: '{msg0.decode()}'")
            game_dict[game_id][4].write(data)
            # await game_dict[game_id][4].drain()
            msg1 = await game_dict[game_id][3].read(100)
            logging.info(f"Received {time.strftime('%X')}: '{msg1.decode()}'")
        else:
            game_dict[game_id][2].write(data)
            # await game_dict[game_id][2].drain()
            msg0 = await game_dict[game_id][1].read(100)
            logging.info(f"Received: '{msg0.decode()}'")


async def main(host, port):
    server = await asyncio.start_server(new_client, host, port)
    # print(f"Server started with {host}:{port}")
    logging.info(f"Server started at {host}:{port}")
    await server.serve_forever()


asyncio.run(main('192.168.3.18', 5000))

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