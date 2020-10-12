#! /usr/bin/env python3

import sys
sys.path.append("../../lib")
import re, socket, params, os
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )


progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        numFiles = 0
        while True:
            #recieve the name of the file
            fileFromClient = self.fsock.receive()
            payload = self.fsock.receive()
            print("got file: " + fileFromClient.decode())
            print("contents of file: " + payload.decode())

            #write to new file on server
            #check if file exists
            #this will influence the file name by placing a number next to it
            if exists(fileFromClient):
                numFiles = numFiles + 1

            fileNew = str(numFiles)+fileFromClient.decode()
            serverFile = open(fileNew, 'wb')
            serverFile.write(payload)

            # #get the name of the file and message from the testClient
            # #the file name will be used to write to a new file of the same
            # #name on the server side
            # fileFromClient, payload = self.fsock.receive(debug)
            # #check to see if the contents of the
            # if debug:
            #     print("Received: ", payload)
            #     #there was an issue exit with a problem
            # if payload is None:
            #     print("EMPTY CONTENTS")
            #     sys.exit(1)
            # #write to the new file in wb write binary
            # fileFromClient = fileFromClient.decode()
            # outfile = open(fileFromClient+"1", "wb")
            # outfile.write(payload)
            # print("saved file")
            # outfile.close()



while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
