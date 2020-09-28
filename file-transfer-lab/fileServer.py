import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 50001))
serverSocket.listen(1)
print("WAITING FOR CONNECTIONS..")

#boolean to close the server socket when we are done receving messages
#from the client
run = True

while run:
    conn, address = serverSocket.accept()
    print("CONNECTED TO: ", address)
    text_file = 'serverFile.txt'
    #create a file with open and write to it in binary mode
    #because we are receving the data in binary from the client
    with open(text_file, "wb") as fw:
        #we want the whole file not just the receved number of bytes
        #so we use a for loop to keep recving the data from the clients file
        while True:
            #receving the data from the clients file in 32 bytes
            data = conn.recv(32)
            # if data == b'BEGIN':
            #     continue

            #if the client sends a message ENDED that means the whole file
            #has been sent and we should stop  so we break the while lopp
            if data == b'ENDED':
                print('BREAKING!! DONE!!')
                run = False
                break
            else:
                #Else if we havent gotten the end message we write the
                #messages we have recived to the file

                #print('Received: ', data.decode('utf-8'))
                fw.write(data)
                #print('Wrote to file', data.decode('utf-8'))
        #close the file we wrote to
        #its the file we saved the clients data to
        fw.close()
    print("Received..")
print("CLOSING SERVER SOCKET")
serverSocket.close()
