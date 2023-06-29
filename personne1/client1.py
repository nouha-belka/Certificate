import os 
import socket
from pathlib import Path
from rsa import *
import base64
from keys import private


file_name = 'turt.png'
file_ext = b'png----extention'
p = Path(__file__).with_name('nouha.cert')

with p.open( "rb") as f:
    data = f.read()
certificate = data


p = Path(__file__).with_name(file_name)

# file content
with p.open( "rb") as f:
    data = f.read()

#signature
hash_doc = hash_crypt(data,private)
signature = str(hash_doc).encode('utf-8')

doc_sign_cert = file_ext + data + b"\n---sign---\n"+signature +b"\n---sign---\n"+ certificate


# Encode binary data as Base64
base64_data = base64.b64encode(doc_sign_cert)


# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# connect to the server on a specified port
client_socket.connect((host, 9998))


# send a message to the other client
client_socket.sendall(base64_data)
client_socket.send(b"<END>")



# close the socket
client_socket.close()
