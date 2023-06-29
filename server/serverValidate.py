import os 
import socket
import tqdm
from pathlib import Path
from rsa import *



# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# bind the socket to a public host, and a port
server_socket.bind((host, 9999))

# set the number of clients that can be queued up to 5
server_socket.listen(5)

while True:
    # establish a connection
    client_socket, address = server_socket.accept()

    done = False
    file_bytes = b""
    # receive data from the client
    while not done:
        data  = client_socket.recv(1024)
        # print(data)
        if data[-5:] == b"<END>":
            done = True
        
        file_bytes += data
    
    # split content
    file_bytes = file_bytes.split(b"!v/v?")
    certNum =  file_bytes[0].decode('utf-8')
    cert = file_bytes[1]

    # compare the file of certificate with content
    p = Path(__file__).parent.joinpath('certs').joinpath(f'N0{certNum}.cert')

    try:
        with p.open('rb') as f:
            content = f.read()

        if(content.replace(b'\r', b"").replace(b'\n', b"")  == cert[:-5].replace(b'\r', b"").replace(b'\n', b"")):
            message = "valide"
        else:
           message = "File not valide"   

    except FileNotFoundError:
        message = "Cetificate doesn't exist in our system"

    
    client_socket.sendall(message.encode('utf-8'))
    # close the client socket
    client_socket.close()
    # server_socket.close()
