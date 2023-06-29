import base64
import socket
import tqdm
from pathlib import Path

from validate import validateDoc


# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# bind the socket to a public host, and a port
server_socket.bind((host, 9998))

# set the number of clients that can be queued up to 5
server_socket.listen()

while True:
    # establish a connection
    client_socket, address = server_socket.accept()


    done = False
    file_bytes = b""
    # receive data from the client
    while not done:
        data  = client_socket.recv(1024)
        if data[-5:] == b"<END>":
            done = True
        
        file_bytes += data

    # Decode Base64 data back to binary
    decoded_data = base64.b64decode(file_bytes[:-5])
    # print(validateDoc(decoded_data))
    p = Path(__file__).with_name('tut.txt')

    with p.open( "wb") as f:
        f.write(decoded_data)
    print(validateDoc(decoded_data))



    
    # # close the client socket
    client_socket.close()
    # server_socket.close()
