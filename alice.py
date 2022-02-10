##############################

# 2 - ROUND FEISTEL CIPHER

##############################

# ALICE IS THE SENDER
# ENCRYPTION IS DONE HERE
# ENCRYPTED MESSAGE SEND TO BOB
# SOCKET PROGRAMMING IS USED HERE
# MESSAGE STORED IN input.txt FILE

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


def encryptionAlgo(PT):
    PT_Ascii = [ord(x) for x in PT]

    PT_Bin = [format(y, '08b') for y in PT_Ascii]
    PT_Bin = "".join(PT_Bin)

    lenn = len(PT_Bin)//2
    n = int(lenn)
    L1 = PT_Bin[0:n]

    key1 = 0
    key2 = 0
    R1 = PT_Bin[n::]
    m = 1+len(R1)-1

    key1 = keyGenerator(m)

    f1 = bitXOR_Strings(R1, key1, n)
    R2 = bitXOR_Strings(f1, L1, n)

    key2 = keyGenerator(m)

    R2 = bitXOR_Strings(f1, L1, n)
    f2 = bitXOR_Strings(R2, key2, n)
    L2 = R1

    R3 = bitXOR_Strings(f2, L2, n)
    L3 = R2

    bin_data = add_string(L3, R3)
    str_data = ' '

    maxx = len(bin_data)
    spacing = 7
    for j in range(0, maxx, spacing):

        start = j
        end = j+spacing

        temp_data = bin_data[start:end]
        decimal_data = bin2dec(temp_data)

        str_data = str_data + chr(decimal_data)

    return str_data, L3, R3, key1, key2, n


f = open('input.txt', 'r')

pt = f.read()

print("TEXT from Input File -- ", pt)

ct, L3, R3, key1, key2, n = encryptionAlgo(pt)
print("Cipher Text -- ", ct)


ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 9110
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Ready for Client/Bob to Connect..')
ServerSideSocket.listen(5)

Client, address = ServerSideSocket.accept()
print('Client/Bob Connection Info -- ' + address[0] + ':' + str(address[1]))

print("Cipher Text -- ", ct)
Client.send(str.encode(ct))
Client.send(str.encode(L3))
Client.send(str.encode(R3))
Client.send(str.encode(key1))
Client.send(str.encode(key2))
Client.send(str.encode(str(n)))

print("Cipher Text Send to Bob...")

ServerSideSocket.close()
