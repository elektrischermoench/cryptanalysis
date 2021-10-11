import numpy as np 
from boxes import *

########
## Key Expansion
########
def RotWord(bytes):
   return bytes[1: len(bytes)] + bytes[0: 1]

def SubWord(word : bytes):
   return bytes(sbox_en[i] for i in word)
	
def rcon(num):
   return [rcon_lookup[num], 0x00, 0x00, 0x00]

def KeyExpansion(key: bytes):
    exp_key = [key[i : i + len(key) // 4] for i in range(0, len(key), 4)]
        
    for round in range(1,11):
        rotate = RotWord(exp_key[-1])
        sub = SubWord(rotate)
        xored = xor(exp_key[-4], sub)
        firstc = xor(xored, rcon(round))
        exp_key.append(firstc)
        for _ in range(3):
            exp_key.append(xor(exp_key[-1], exp_key[-4]))
    return exp_key

def InvKeyExpansion(key: bytes):
    exp_key = [key[i : i + len(key) // 4] for i in range(0, len(key), 4)]
        
    for round in reversed(range(1,5)):
        for _ in range(3):
            exp_key.insert(0, xor(exp_key[2], exp_key[3]))
        rotate = RotWord(exp_key[2])
        sub = SubWord(rotate)
        xored = xor(exp_key[3], rcon(round))
        firstc = xor(xored, sub)
        exp_key.insert(0, firstc)  
    return b"".join(exp_key[:4])
    #return exp_key
    