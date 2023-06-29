from rsa import *
from keys import *


# # generate key pair
public_key, private_key = public, private

# get the file in bytes
fileToBeEnc = Path(__file__).with_name(f'{name}.txt')
with open(fileToBeEnc,'rb') as file :
        chaine = file.read()

file.close()     

# print(chaine)
fileContent = hash_crypt(chaine,private_key)

fileToBeEnc = Path(__file__).with_name(f'{name}.csr')
with open(fileToBeEnc,'w') as file :
        file.write(fileContent)



# deciphertext = decrypt(ciphertext, public_key)
# print(deciphertext,"\n")
# print(deciphertext == finalHash)




