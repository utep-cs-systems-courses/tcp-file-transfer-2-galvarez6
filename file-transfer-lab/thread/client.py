#! /usr/bin/env python3

import socket, sys, re
sys.path.append("../../lib")
import params
from os import path
from os.path import exists

from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "testClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Cant parse Server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)

#connect to server 
sock.connect(addrPort)
#let encapFramedSock handle receiving files
fsock = EncapFramedSock((sock, addrPort))

for i in range(1):
    #let the user type the file they want to send to the server
    fileToSend = input("enter file name:")

    #open the file in read binary to send as binary to the server
    file = open(fileToSend, 'rb')
    
    #payload contains the msg from the file to send to the server
    payload = file.read()
    
    #if there is no more data read from the file it has been sent to the server
    #in my previous i didnt have a payload it was just read in read binary

    #send payload to server
    fsock.send(payload)
