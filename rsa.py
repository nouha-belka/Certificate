import hashlib
import random
from typing import Tuple
from tqdm import tqdm
import base64
from pathlib import Path

def is_prime(n, k=5):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for i in range(k):
        x = pow(random.randint(2, n - 1), d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_number(n_bits):
    while True:
        p = random.getrandbits(n_bits)
        p |= (1 << n_bits - 1) | 1
        if is_prime(p):
            return p

def generate_key_pair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)

    d = extended_gcd(e, phi)[1]
    d = d % phi

    return (n, e), (n, d)

def encrypt(plaintext: int, public_key: Tuple[int, int]) -> int:
    n, e = public_key
    return square_and_multiply(plaintext, e, n)

def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    n, d = private_key
    return square_and_multiply(ciphertext, d, n)

def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def square_and_multiply(base: int, exponent: int, modulus: int) -> int:
    binary = bin(exponent)[2:]
    result = 1

    for bit in binary:
        result = (result ** 2) % modulus
        if bit == '1':
            result = (result * base) % modulus

    return result




# generate key pair
p = generate_prime_number(512)
q = generate_prime_number(512)
public_key, private_key = generate_key_pair(p, q)
print(public_key)
print(private_key)




# p = Path(__file__).with_name('example.txt')
# with open(p,'rb') as file :
#         chaine = file.read()
        

# hash_object = hashlib.sha256(chaine)
# hash_digest = hash_object.hexdigest()
# message_int = int(hash_digest, 16)
# # message = "hello world"
# # plaintext = int.from_bytes(hash_digest.encode(), 'big')
# ciphertext = encrypt(message_int, private_key)


# print(message_int,"\n")
# print(ciphertext,"\n")

# dec = decrypt(ciphertext, public_key)
# print(dec,"\n")
# # num_bytes = (dec.bit_length() + 7) // 8
# # dd = dec.to_bytes(num_bytes, byteorder='big')

# # print(dd)





