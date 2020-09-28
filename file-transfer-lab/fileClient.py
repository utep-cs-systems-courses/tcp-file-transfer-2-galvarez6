import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("localhost", 50001))

text_file = 'sendingThis.txt'

#open the file we are sending in binary mode , read only
with open(text_file, 'rb') as fs:
    #Using with, no file close is necessary,
    #with automatically handles file close
    #clientSocket.send(b'BEGIN')
    while True:
        data = fs.read(1024)
        #send data from the file we are reading to the server this case is
        #1mb of data at a time
        clientSocket.send(data)
        #if there is no more data from the file to send break the loop
        #of sending data to the server
        if not data:
            print('SENT DATA SUCCESFULY')
            break
    #send a message to the server to indicate we are done sending the data
    clientSocket.send(b'ENDED')
    #close the file we were reading from
    fs.close()
#close the client socket
print("CLOSING CLIENT SOCKET")
clientSocket.close()
