import os 
import socket
from pathlib import Path


p = Path(__file__).with_name('nouha.csr')
# file_size  = os.path.getsize(p)

with p.open( "rb") as f:
    data = f.read()

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# connect to the server on a specified port
client_socket.connect((host, 9999))


# send a message to the server
client_socket.sendall(data)
client_socket.send(b"<END>")




# receive data from the server
file_bytes = b""
done = False
while not done:
    data  = client_socket.recv(1024)
    # print(data)
    if data[-5:] == b"<END>":
        done = True
    
    file_bytes += data

p = Path(__file__).with_name('nouha.cert')

with p.open( "wb") as f:
    f.write(file_bytes[:-5])
# print(f"{file_bytes.decode('utf-8')}")
# close the socket
client_socket.close()
