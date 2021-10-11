import numpy as np 
import binascii
from aes import *
from KeySchedule import *
from boxes import *
from square import *

########
## main
## Call some test data: https://www.davidwong.fr/blockbreakers
########
def main():
   print("\nPrepare for Sqare attack: ")
   key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
   #KE = (KeyExpansion(key))
   #for x in range(20):
   #    print(binascii.hexlify(KE[x]))
   print("Original key: \n", print_state(key))
   #print("Original key: ",binascii.hexlify(b"".join(key[:4])))
   # crack key
   print("Cracking the last round key ...")
   c_key = [0x00] * 16
   
   for byte in range(16):
       position = byte
       hits = []
       
       while (len(hits) != 1):
           hits = []
           enc_ds = setup(key,4)
           
           for key_guess in range(0xFF):
               rev_states = reverse_state(key_guess,position, enc_ds)
               if (checkKeyGuess(key_guess, position, rev_states)):
                   hits.append(key_guess)

       c_key[byte] = hits[0]
       print(hex(position), hex(c_key[byte]),end=" ")
   byteArrayObject = bytearray(c_key)
   keybytes = bytes(byteArrayObject)
   crack = InvKeyExpansion(keybytes)
   #print("Key found: ",binascii.hexlify(b"".join(crack[:4])))
   print("Key found: \n", print_state(crack))
      
if __name__ == "__main__":
    main()