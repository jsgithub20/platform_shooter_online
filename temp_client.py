import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('192.168.3.10', 5000)

    while True:
        message = input("input your message to be sent: ")
        if message != "quit":
            print(f'Send: {message!r}')
            writer.write(message.encode())

            data = await reader.read(100)
            print(f'Received: {data.decode()!r}')

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