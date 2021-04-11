import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('10.31.16.25', 5000)

    while True:
        message = input("input your message to be sent: ")
        if message != "quit":
            print(f'Send: {message!r}')
            writer.write(message.encode())

            data = await reader.read(100)
            print(f'Received: {data.decode()!r}')

            print('Close the connection')
    writer.close()