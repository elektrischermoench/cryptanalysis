import numpy as np 
from boxes import *

########
## AES
########
def SubBytes(state):
    subState = bytearray()
    for x in state:
        for z in x:
            subState.append(sbox_en[z])
    return np.reshape(subState, newshape=(4, 4))

def ShiftRows(state):
    shiftState = np.copy(state)
    for x in range(1,4):
        shiftState[x] = (np.roll(state[x], len(state)-x))
    return np.reshape(shiftState, newshape=(4, 4))
    
def InvShiftRows(state):
    shiftState = np.copy(state)
    for x in range(1,4):
        shiftState[x] = (np.roll(state[x], x))
    return np.reshape(shiftState, newshape=(4, 4))
    
def MixColumns(state): # MixColumns the lazy lookup way ;D
    mixedState = np.copy(state)
    for x in range(4):
        a0, a1, a2, a3 = state[:, x]
        mixedState[0, x] = multiplication_by_2[a0] ^ multiplication_by_3[a1] ^ a2 ^ a3
        mixedState[1, x] = a0 ^ multiplication_by_2[a1] ^ multiplication_by_3[a2] ^ a3
        mixedState[2, x] = a0 ^ a1 ^ multiplication_by_2[a2] ^ multiplication_by_3[a3]
        mixedState[3, x] = multiplication_by_3[a0] ^ a1 ^ a2 ^ multiplication_by_2[a3]
    return mixedState
    
def MixColumnsInverse(state):
    mixedState = np.copy(state)
    for x in range(4):
        a0, a1, a2, a3 = state[:, x]
        mixedState[0, x] = multiplication_by_14[a0] ^ multiplication_by_11[a1] ^ multiplication_by_13[a2] ^ multiplication_by_9[a3]
        mixedState[1, x] = multiplication_by_9[a0] ^ multiplication_by_14[a1] ^ multiplication_by_11[a2] ^ multiplication_by_13[a3]
        mixedState[2, x] = multiplication_by_13[a0] ^ multiplication_by_9[a1] ^ multiplication_by_14[a2] ^ multiplication_by_11[a3]
        mixedState[3, x] = multiplication_by_11[a0] ^ multiplication_by_13[a1] ^ multiplication_by_9[a2] ^ multiplication_by_14[a3]
    return mixedState
    
def AddRoundKey(state, key):
    newState = bytearray()
    for x in range(4):
            newState += bytearray((xor(bytes(state[x]), bytes(key[x]))))
    return np.reshape(newState, newshape=(4, 4))
    
def encrypt(plaintext, key):
    pt = print_state(plaintext)
    #KeyExpansion
    key_state = KeyExpansion(key) #, rounds=rounds + 1)
    round_key = key_state[0:4]
    round_key = b''.join(round_key)
    round_key = print_state(round_key)
    # pre withenting
    state = AddRoundKey(pt, round_key) 
    
    for round in range(1,10):
    #LOOP(rounds-1)
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        #get round key
        round_key = key_state[4 * round : 4 * (round+1)]
        round_key = b''.join(round_key)
        round_key = print_state(round_key)
        #AddRoundKey
        state = AddRoundKey(state, round_key)

    state = SubBytes(state)
    state = ShiftRows(state)
    #get round key
    round_key = key_state[4 * 10 : 4 * (10+1)]
    round_key = b''.join(round_key)
    round_key = print_state(round_key)
    state = AddRoundKey(state, round_key)
                         
    return state