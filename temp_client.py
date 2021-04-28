import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('192.168.3.18', 5000)
    data = await reader.read(100)
    client_id = data.decode()
    print(f"This is client# {client_id}")

    while True:
        data = await reader.read(100)
        msg = data.decode()
        if msg != "quit":
            print(f'Received: {msg!r}')
            reply = f"{int(client_id)}: msg received is {msg!r}"
            writer.write(reply.encode())
            await writer.drain()
        else:
            writer.close()
            print('Closing the connection')
            break

asyncio.run(tcp_echo_client())

# import asyncio
#
# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection(
#         '192.168.3.10', 8888)
#
#     print(f'Send: {message!r}')
#     writer.write(message.encode())
#
#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')
#
#     print('Close the connection')
#     writer.close()
#
# asyncio.run(tcp_echo_client('Hello World!'))