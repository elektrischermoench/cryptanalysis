import random
import numpy as np 
import binascii
from boxes import *
from KeySchedule import *
from aes import *

####
# Square-Attack
####
def encryptWithRounds(plaintext, key, rounds):
    pt = print_state(plaintext)
    #KeyExpansion
    key_state = KeyExpansion(key) #, rounds=rounds + 1)
    round_key = key_state[0:4]
    round_key = b''.join(round_key)
    round_key = print_state(round_key)
    # pre withenting
    state = AddRoundKey(pt, round_key) 
    #print("AddRoundKey: \n",state)
    for round in range(1,rounds):
    #LOOP(rounds-1)
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        #get round key
        round_key = key_state[4 * round : 4 * (round+1)]
        round_key = b''.join(round_key)
        round_key = print_state(round_key)
        #print("RoundKey: \n", round_key)
        #AddRoundKey
        state = AddRoundKey(state, round_key)
        #print("Runde: ",round)
        #print(state)

    state = SubBytes(state)
    state = ShiftRows(state)
    #get round key
    round_key = key_state[4 * rounds : 4 * (rounds+1)]
    round_key = b''.join(round_key)
    round_key = print_state(round_key)
    state = AddRoundKey(state, round_key)
                         
    return state
    
def setup(key, rounds):
    #create delta set
    delta_set = []
    r = random.randint(0x00, 0xFF)
    for i in range(256):
        matrix = [r] * 16
        matrix[0] = i
        byteArrayObject = bytearray(matrix)
        by =  (bytes(byteArrayObject))
        delta_set.append(by)
        #print(print_state(delta_set[i]))
     
    # encrypt the delta set with AES-3Round
    result_set = []
    for i in range(256):
        #print("Plaintext: \n",print_state(delta_set[i]))
        result_set.append(encryptWithRounds( delta_set[i], key, rounds ))
        #print("Ciphertext: \n",print_state(result_set[i]))
    return result_set
    
def reverse_state(key_guess, position, enc_ds):
    position_in_state = (position % 4, position // 4)
    r = []
    i, j = position_in_state
    for s in enc_ds:
        #before_add_round_key = s[i, j] ^ key_guess
        # not sure if ShiftRows is needed for the attack, because it will
        #print(s)
        #before_shift_rows = InvShiftRows(s)
        before_add_round_key = s[i, j] ^ key_guess
        before_sub_byte = sbox_en.index(before_add_round_key)
        r.append(before_sub_byte)  
    #print(r, len(r))
    #print("statepos: ",position_in_state)
    return r

def checkKeyGuess(key_guess, position, reverse_states):
    #position_in_state = (position % 4, position // 4)
    xored = 0x00
    for x in range(len(reverse_states)):
        #print (reverse_states[x])
        #print (hex(reverse_states[x][0][0]))
        xored ^= reverse_states[x]
    #print ('XORED ', xored)
    return xored == 0