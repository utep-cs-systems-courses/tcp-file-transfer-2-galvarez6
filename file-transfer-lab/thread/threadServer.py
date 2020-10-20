#! /usr/bin/env python3

import sys
sys.path.append("../../lib")
import re, socket, params, os
from os.path import exists
from threading import Thread, enumerate, Lock

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

#globally declare a list so the list is present during the duration of the descriptor
fileLockList = []
#when adding all we care about is adding the file onto the list and not
#the position it geos to so we can use append() to add to the end of the list
#but then we also need to get it position to find out where it is to remove it
#just in case more threads run at the same time and append to the list
#however instead of pop() we can use remove(value)
#it removes the first element of the list with that same value
global locker
locker = Lock()


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
            fileNameFromC = fileFromClient.decode()
            #check if the file is in the list of files being used at the moment
            #if not append it so we know what files are being used and are locked
            if(fileNameFromC not in fileLockList):
                fileLockList.append(fileNameFromC)

                print("LOCKING FILE: "+fileNameFromC)
                print(*fileLockList)
                locker.acquire()
                #####lock this critical area for threads that dont have a lock so they cannot access this part
                payload = self.fsock.receive()
                #client sent the name of the file first so we got that
                #we can use the name to lock the file descriptor while its being used
                #we can put the name of the file on a dictionary/list/array object and if other threads
                #want to write to that same file they check if it is on the stack
                #if it is they have to wait for the lock
                #if not the we give the lock to the thread that wants to
                #write to that file on the server with that name
                #and when the thread is done remove the file name from the file dictionary/list/array object
                print("got file: " + fileFromClient.decode())
                print("contents of file: " + payload.decode())
                #write to new file on server
                #check if file exists
                #this will influence the file name by placing a number next to it

                fileNew = str(numFiles)+fileFromClient.decode()
                serverFile = open(fileNew, 'wb')
                serverFile.write(payload)
                serverFile.close()
                #done with this file close it and pop it from the list so it can be used again
                #our own method
                fileLockList.remove(fileNameFromC)
                locker.release()
                print("UNLOCKING FILE: "+fileNameFromC)
                print(*fileLockList)
                ######end of lock
            #else if the file is in the list we have to make the thread wanting to use it wait
            #to acquire the lock





            ######
            #for now this is useless
            #if exists(fileFromClient):
                #numFiles = numFiles + 1
            ####





            #thrash but dont wanna get rid of
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
