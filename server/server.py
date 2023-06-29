import os 
import socket
import tqdm
from pathlib import Path
from rsa import *
from validate import *

def addCertNum():
    p = Path(__file__).with_name('conf.txt')
    file = p.open("r")
    num = file.read()
    file.close()

    num = int(num)
    num += 1
    file = p.open("w")
    file.write(str(num))

    return num


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

    certNum = addCertNum()
    p = Path(__file__).parent.joinpath('csrs').joinpath(f'N0{certNum}.csr')
    file = p.open("wb")

    done = False
    file_bytes = b""
    # receive data from the client
    while not done:
        data  = client_socket.recv(1024)
        # print(data)
        if data[-5:] == b"<END>":
            done = True
        
        file_bytes += data


    file.write(file_bytes[:-5])
    file.close()

    
    if(validateCsr(file_bytes)):
        message = formatCert(file_bytes,certNum)
        p = Path(__file__).parent.joinpath('certs').joinpath(f'N0{certNum}.cert')
        with p.open( "wb") as f:
            f.write(message.encode('utf-8'))
    else:
        message = "infos not valide or someone tampered with the document\n please resend"

    
    client_socket.sendall(message.encode('utf-8'))
    client_socket.send(b"<END>")
    # close the client socket
    client_socket.close()
    # server_socket.close()
