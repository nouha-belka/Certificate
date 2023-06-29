from pathlib import Path
from datetime import datetime, timedelta
import os 
import socket
from rsa import *
from keys import *

char = b"""-----BEGIN CERTIFICATE REQUEST-----
bm91aGEvYmVsa2Evbm91aGFiZWxrYTIwMDFAZ21haWwuY29tDQooODk0MjQ1NjI5
MDIyNTAxNDQ5ODM3NDMwMzc5OTUwMDIwNjYwNjk3MDY0MzYyMjM5ODY4NjgzNzEx
MDI1MDgxMDc1MzE3MDYyODY4MjU0OTA1NDY2MjE0NTI5MjA1MDA5MDk4MDM3NzE1
MjcyNDc5Njc0NTc5NjEzOTM2MDg4ODk2NTUzOTg4ODY1NTIwNzI3MzgzOTQ2NTEz
MzUyNzY2OTAxMDI4MDg1NTExMzkzNjQxMDAxOTk3NzM0MTczOTEyNzI0MzkxNzUx
NjUxNjg4MzY3NDk4MzUxMDAyMTc2NTA3ODQyNjQyODAzNTc1Njc3ODIzMjgwNjY5
NDUyMzcyOTEyMjkyNTg3NDA3NjQ0MjYzNDI4MTkzOTQyMDUxOTIwMDAwNjI3MzUz
MjMyMzE5MzA2NTMsIDY1NTM3KQ0Kc2hhMjU2DQpzaWduDQo4Mjg0ODQ2OTI2MDE2
NTI3NTU2NjcwNTAyMjQ2MDQwOTQ3NzM1OTE1NjU0NTM1ODU5MzUyMDM5Mjg1MzU3
OTkyNjI0ODY0MjM3MzU3NDMxNjczODMwNTQ4ODU5NDk1MzkxMzQwNzU1OTk4MDc4
MDg0MzIwMzA2NzkwMzk0NDAxNTUzNDUxODc5MDg3MzkyOTkzMjg0NDg0OTU5OTY1
NDE5NzM1MTc5MjgwNTc4Mjk4OTIzOTQwMjE2MjAxNTM4MDYzMTk2MjQxNDkwMjI4
MjI0ODkwOTMzMjU0MzU2MTMxODMyNjIxNDM4MDQ4NjIzNjUzMjc5NjUzODM2MDgy
MzU0NTUxMTc3NzcxMTk0MzUzODU4MjcyNTMxNzY3MzE1ODcwMjc5MzcwMDgxNjkz
OTgzNzE2MA==
-----END CERTIFICATE REQUEST-----<END>"""

def decodeCsrCert(file_bytes):
    # pem decode
    dec = pem_decode(file_bytes[:-5].decode('utf-8')).decode('utf-8')

    # print(dec)
    #split content and signature
    withouSign = dec.split("sign")
    withouSign = withouSign[0].encode('utf-8') + b"sign\r\n"



    #split contents into list
    decList = dec.replace("\r", "").split("\n")
    # print(decList)

    return withouSign,decList
# decodeCsrCert(char)

def validateCsr(file_bytes):
    withouSign,decList = decodeCsrCert(file_bytes)
    # separate info and the rest
    infoList = decList[0]
    decList = decList[1:]

    # hash content of the file
    if(decList[1] == "sha256"):
        hash_object = hashlib.sha256(withouSign)
        hash_digest = hash_object.hexdigest()
        finalHash = int(hash_digest, 16)
    else:
        pass

    #format the key pair into tuple
    keyPair = decList[0].replace("(", "").replace( ")", "").split(",")
    keyPair = [int(x) for x in keyPair]
    keyPair = tuple(keyPair)

    #signature formating and decryption
    signature = int(decList[-1])
    signDec = decrypt(signature,keyPair)

    
    
    if(signDec != finalHash):
        return False
    else:
        return True


def formatCert(file_bytes,certnum):
    withouSign,decList = decodeCsrCert(file_bytes)
    # separate info and the rest
    infoList = decList[0]
    decList = decList[1:]

    # get current date and time
    current_date = datetime.now()

    # add one year to current date
    one_year_later = current_date + timedelta(days=365)

    # CA name
    nameCA = name

    # serial number
    serial = certnum

    # public key CA
    keyCA = public


    cerString = f"{nameCA}\n{serial}\n{keyCA}\n{infoList}\n{decList[0]}\n{decList[1]}\n{current_date}\n{one_year_later}\nsign\n"

    fileContent = hash_crypt(cerString.encode('utf-8'),private)

    return fileContent
    # print(cerString.encode('utf-8'))



