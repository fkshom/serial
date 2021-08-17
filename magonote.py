import os, pty, serial
import asyncio
import serial_asyncio
import os, subprocess, serial, time

class MagonoteDevice():
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    
    async def run(self):
        print("Loop start")
        while True:
            msg = await self.reader.readuntil(b'\n')
            print(f"Received: {msg}")
            if msg.rstrip() == b'wakeup':
                print("  Waking up my computer!")
                self.writer.write("ok\n".encode())
            else:
                print(f"  Unknown command")
                self.writer.write("unknown\n".encode())


async def main():
    device_port = './device'
    client_port = './ttyUSB0'
    cmd=['/usr/bin/socat','-d','-d','PTY,link=%s,raw,echo=0' %
            device_port, 'PTY,link=%s,raw,echo=0' % client_port]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

    reader, writer = await serial_asyncio.open_serial_connection(
        loop=None,
        limit=None,
        url='./device',
        baudrate=115200,
    )
    m = MagonoteDevice(reader, writer)
    await m.run()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
