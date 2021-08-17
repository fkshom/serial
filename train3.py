def mycomports(include_links=False):
    import glob
    from serial.tools import list_ports_common
    from serial.tools.list_ports_linux import SysFS
    devices = glob.glob('/dev/ttyS*')           # built-in serial ports
    devices.extend(glob.glob('/dev/ttyUSB*'))   # usb-serial with own driver
    devices.extend(glob.glob('/dev/ttyXRUSB*')) # xr-usb-serial port exar (DELL Edge 3001)
    devices.extend(glob.glob('/dev/ttyACM*'))   # usb-serial with CDC-ACM profile
    devices.extend(glob.glob('/dev/ttyAMA*'))   # ARM internal port (raspi)
    devices.extend(glob.glob('/dev/rfcomm*'))   # BT serial devices
    devices.extend(glob.glob('/dev/ttyAP*'))    # Advantech multi-port serial controllers
    devices.extend(glob.glob('./ttyUSB*'))
    if include_links:
        devices.extend(list_ports_common.list_links(devices))
    return [info
            for info in [SysFS(d) for d in devices]
            if info.subsystem != "platform"]    # hide non-present internal serial ports

import serial.tools.list_ports_linux
serial.tools.list_ports_linux.comports = mycomports

import os, pty, serial
import asyncio
import serial_asyncio

import os, subprocess, serial, time

import serial
from serial.tools import list_ports
import time

def list_devices():
    ports = list_ports.comports(include_links=True)    # ポートデータを取得
    for port in ports:
        print(vars(port))

if __name__ == '__main__':
    list_devices()