##############################

# 2 - ROUND FEISTEL CIPHER

##############################

# BOB IS THE RECEIVER
# DECRYPTION IS DONE HERE
# DECRYPTED MESSAGE RECEIVED BY BOB
###############################

# STEPS ARE:
#       1) Open 1st Terminal.
#       2) Enter the Instruction: python .\alice.py.
#       3) In mean time Open 2nd Terminal.
#       4) Enter the Instruction: python .\bob.py

###############################

from _thread import *
import os
import socket
import binascii
import random


def add_string(s1, s2):
    return s1+s2


def keyGenerator(p):

    ret_val = str()
    q = True
    p = int(p)

    while p > 0 and q == True:
        q = False
        num = str(random.randint(0, 1))
        p = p - 1
        ret_val = add_string(ret_val, num)
        q = True

    return ret_val


def bitXOR_Strings(a, b, n):

    pointer = 0
    f1 = False
    bitXOR_Strings = str()

    while (pointer < n):
        f1 = b[pointer] != a[pointer]
        if(f1):
            bitXOR_Strings = add_string(bitXOR_Strings, "1")
        else:
            bitXOR_Strings = add_string(bitXOR_Strings, "0")
        pointer = pointer + 1

    return bitXOR_Strings


def bin2dec(binary):
    return int(binary, 2)


def decrypt(CT, L3, R3, key1, key2, n):
    L4 = L3

    R4 = R3

    f3 = bitXOR_Strings(L4, key2, n)
    L5 = bitXOR_Strings(R4, f3, n)
    R5 = L4

    f4 = bitXOR_Strings(L5, key1, n)
    L6 = bitXOR_Strings(R5, f4, n)
    R6 = L5
    PT1 = add_string(L6, R6)

    PT1 = int(PT1, 2)
    return binascii.unhexlify('%x' % PT1)


ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 9110

print('Taking Server/Alice side approval for Connection...')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))


ct = ClientMultiSocket.recv(1024).decode('utf-8')
L3 = ClientMultiSocket.recv(1024).decode('utf-8')
R3 = ClientMultiSocket.recv(1024).decode('utf-8')
key1 = ClientMultiSocket.recv(1024).decode('utf-8')
key2 = ClientMultiSocket.recv(1024).decode('utf-8')
n = ClientMultiSocket.recv(1024).decode('utf-8')

ClientMultiSocket.close()

print("Decrypting Message...")

txt = decrypt(ct, L3, R3, key1, key2, int(n))

print("TEXT Message gotton -- ", txt)
