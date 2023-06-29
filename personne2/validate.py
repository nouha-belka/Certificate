from datetime import datetime

from pathlib import Path
import socket
from rsa import *


def sendServer(data,num):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    # connect to the server on a specified port
    client_socket.connect((host, 9999))

    num = num + "!v/v?"
    num = num.encode('utf-8')
    # send a message to the server
    client_socket.sendall(num+data)
    client_socket.send(b"<END>")




    # receive data from the server
    answer  = client_socket.recv(1024)
    # close the socket
    client_socket.close()
    return answer

def decodeCsrCert(file_bytes):
    # pem decode
    dec = pem_decode(file_bytes.decode('utf-8')).decode('utf-8')

    #split content and signature
    withouSign = dec.split("sign")
    withouSign = withouSign[0].encode('utf-8') + b"sign\n"

    #split contents into list
    decList = dec.replace("\r", "").split("\n")

    return withouSign,decList
def validateSignCert(cert):
    withouSign,decList = decodeCsrCert(cert)

    #format the key pair into tuple
    keyPair = decList[2].replace("(", "").replace( ")", "").split(",")
    keyPair = [int(x) for x in keyPair]
    keyPair = tuple(keyPair)

    # hasher le contenu
    hash_object = hashlib.sha256(withouSign)
    hash_digest = hash_object.hexdigest()
    finalHash = int(hash_digest, 16)

    #signature formating and decryption
    signature = int(decList[-1])
    signDec = decrypt(signature,keyPair)

    if(signDec != finalHash):
        return False
    else:
        return True
    
def validateSignDoc(withouSign,key,signature):
    #format the key pair into tuple
    keyPair = key.replace("(", "").replace( ")", "").split(",")
    keyPair = [int(x) for x in keyPair]
    keyPair = tuple(keyPair)


    # hasher le contenu
    hash_object = hashlib.sha256(withouSign)
    hash_digest = hash_object.hexdigest()
    finalHash = int(hash_digest, 16)

    #signature formating and decryption
    signature = int(signature)
    signDec = decrypt(signature,keyPair)


    if(signDec != finalHash):
        return False
    else:
        return True

def validateCert(data, decList,withouSign):
    if(validateSignDoc(withouSign,decList[2],decList[-1])):
        # verify chaine
        answer = sendServer(data,decList[1])
        if(answer == b"valide"):
            # compare end date with both deb date and current date
            datDeb = datetime.strptime(decList[6], '%Y-%m-%d %H:%M:%S.%f')
            datFin = datetime.strptime(decList[7], '%Y-%m-%d %H:%M:%S.%f')
            current_date = datetime.now()
            if(datDeb < datFin ):
                if(current_date < datFin):
                    return True
                else:
                    return "certificate expired"  
            else:
                return "incoherent dates"
        else:
            return answer
    else:
        return"document tampered with"



def validateDoc(data):
    extention = data.split(b"----extention")
    docSplit = extention[1].split(b"\n---sign---\n")
    withouSign,decList = decodeCsrCert(docSplit[2])

    # print(validateSignDoc(docSplit[0],decList[4],docSplit[1]))
    certMessage = validateCert(docSplit[2],decList,withouSign)
    if(certMessage == True):
        # verify the whole doc signature
        if(validateSignDoc(docSplit[0],decList[4],docSplit[1])):
            p = Path(__file__).with_name(f"turt1.{extention[0].decode('utf-8')}")
            # file content
            with p.open( "wb") as f:
                f.write(docSplit[0])
            return True
        else:
            return "document tampered with"
    else:
        return certMessage
    
    # print(validateSignDoc(withouSign))

