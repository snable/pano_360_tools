# -*- coding: utf-8 -*-
from bluetooth import *
import time

deviceName = "PapyMerlin"
addr = "00:12:6F:27:04:A1"
port = 1

# nd = discover_devices()
# print nd
#
# for address in nd:
#     ln =  lookup_name(address)
#     if ln == deviceName:
#         addr = address
#         print addr


sock = BluetoothSocket(RFCOMM)
sock.connect((addr, port))
sock.settimeout(1.)
time.sleep(1)


def reverseOrder(orig):
    return orig[4:6]+orig[2:4]+orig[0:2]

def sendCmd(cmd, axis, opts=""):
    command = ":%s%d%s\r" % (cmd, axis, opts)
    sock.send(command)
    c = ''
    while c not in ('=', '!'):
        c = sock.recv(1)
    response = ""
    if c == "!":
        c = sock.recv(1)
        print "ERROR: " + c
        return "Error code: " + c
    while c != '\r':
        c = sock.recv(1)
        response += c
    response = response[:-1]
    if cmd in ("a", "D", "j"):
        response = reverseOrder(response)

    # Actual response is "=" + response + "\r"
    print repr(command), "=>", repr(response)
    return response

for axis in xrange(1,3):
    sendCmd("L", axis)
    sendCmd("F", axis)
    sendCmd("e", axis)
    sendCmd("a", axis)
    sendCmd("D", axis)
    sendCmd("j", axis)
    sendCmd("f", axis)

fc = 0x0E62D3
ez = 0x800000
nv = "000080"
sendCmd("L", 2)
sendCmd("G", 2, "00")
sendCmd("S", 2, nv)
sendCmd("J", 2)
sendCmd("L", 1)
sendCmd("G", 1, "00")
sendCmd("S", 1, nv)
sendCmd("J", 1)
while True:
    time.sleep(0.25)
    status1 = sendCmd("f", 1)[1]
    status2 = sendCmd("f", 2)[1]
    if status1 == "0" and status2 == "0":
        print "COMPLETE!"
        break


sock.close()