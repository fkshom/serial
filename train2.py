import os, pty, serial
import asyncio
import serial_asyncio

class MagonoteDeviceProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        remote_addr = self.transport.get_extra_info('peername')
        print(f'Magonote Server start on {remote_addr}')

    def data_received(self, data):
        remote_addr = self.transport.get_extra_info('peername')
        if data.decode().rstrip() == 'wakeup':
            print("Waking up my computer!")
            self.transport.write(b"ok\n")
        else:
            print(f"Unknown command received: {data}")
            self.transport.write(b"unknown\n")

    def connection_lost(self, exc):
        print('Connection closed')

host = 'localhost'
port = 8000
loop = asyncio.get_event_loop()
coro = loop.create_server(MagonoteDeviceProtocol, host, port)
server = loop.run_until_complete(coro)

print("server start up")
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Server stop")

server.cloe()
loop.run_until_complete(server.wait_closed())
loop.close()
