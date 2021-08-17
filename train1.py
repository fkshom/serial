import os, pty, serial
import asyncio
import serial_asyncio

import os, subprocess, serial, time


class SerialEmulator(object):
    def __init__(self, device_port='./ttydevice', client_port='./ttyclient'):
        self.device_port = device_port
        self.client_port = client_port
        cmd=['/usr/bin/socat','-d','-d','PTY,link=%s,raw,echo=0' %
                self.device_port, 'PTY,link=%s,raw,echo=0' % self.client_port]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        self.serial = serial.Serial(self.device_port, 9600, rtscts=True, dsrdtr=True)
        self.err = ''
        self.out = ''

    def write(self, out):
        self.serial.write(out)

    def read(self):
        line = ''
        while self.serial.inWaiting() > 0:
            line += self.serial.read(1)
        print(line)
        

    def __del__(self):
        self.stop()

    def stop(self):
        self.proc.kill()
        self.out, self.err = self.proc.communicate()

async def main2():
    emulator = SerialEmulator('./ttydevice','./ttyclient') 
    emulator.write("foo".encode())
    while True:
        msg = emulator.read()

async def main():
    device_port = './device'
    client_port = './client'
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

    print("Loop start")
    buf = bytes()
    while True:
        msg = await reader.readuntil(b'\n')
        print(f"Received: {msg}")
        buf += msg
        if msg.rstrip() == b'wakeup':
            print("Waking up my computer!")
            writer.write("ok\n".encode())
        else:
            print(f"Unknown command received: {msg.rstrip()}")
            writer.write("unknown\n".encode())

async def main1():
    master, slave = pty.openpty()
    s_name = os.ttyname(slave)
    print(f"dev: {s_name}")
    reader, writer = await serial_asyncio.open_serial_connection(
        loop=None,
        limit=None,
        url=s_name,
        baudrate=115200,
    )

    print("Loop start")
    buf = bytes()
    while True:
        import pdb; pdb.set_trace()
        msg = await reader.read()
        print(f"{msg}")
        buf += msg
        if msg.rstrip() == b'wakeup':
            print("Waking up my computer!")
            writer.write("ok".encode())
        else:
            print(f"Unknown command received: {msg.rstrip()}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

# master, slave = pty.openpty()
# s_name = os.ttyname(slave)
# print(os.ttyname(master))
# print(os.ttyname(slave))
# ser = serial.Serial(s_name)

# # To Write to the device
# ser.write('Your text'.encode())

# # To read from the device
# line = os.read(master,1000)
# print(line)

