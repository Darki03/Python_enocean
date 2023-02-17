from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
import bitstring
import math


def CMAC_calc(K, Message, RLC, CMAC_size):
    
    #Constants
    Const_zero = bytearray.fromhex("00000000000000000000000000000000")
    Const_Rb   = bytearray.fromhex("00000000000000000000000000000087")
    Const_BlSize = 16
    
    #Concatenate Rolling Code
    Message = Message + RLC
    
    #*************** Generate subkeys**************************************#
    cipher = AES.new(K, AES.MODE_ECB)
    L = cipher.encrypt(Const_zero) #AES128 on Const_Zero with Key

    #Compute K1
    if bitstring.BitArray(L)[0] == 0: #if MSBit(L) = 0
        K1 = bitstring.BitArray(L) << 1
    else:
        K1 = (bitstring.BitArray(L) << 1) ^ bitstring.BitArray(Const_Rb)

    #Compute K2
    if K1[0] == 0:
        K2 = bitstring.BitArray(K1) << 1
    else:
        K2 = (bitstring.BitArray(K1) << 1) ^ bitstring.BitArray(Const_Rb)
    #*********************************************************************#
    
    #Blocks management and CMAC computation
    N = math.ceil(len(Message)/Const_BlSize)
    
    if N == 0:
        N = 1
        Flag = 0
    else:
        if len(Message)%16 ==0:
            Flag = 1
        else:
            Flag = 0
    
    Start = len(Message) - (len(Message)%16)
    M_last = Message[Start:len(Message)]
    if Flag == 1:
        for i in range(len(M_last)):
            M_last[i] = M_last[i] ^ K1.tobytes()[i]
    else:
        M_last = M_last + bitstring.BitArray(bin=str(pow(10 ,(128-8*(len(Message)%16)-1)))).tobytes()
        for i in range(len(M_last)):
            M_last[i] = M_last[i] ^ K2.tobytes()[i]
    
    X = Const_zero
    Y = Const_zero
    for i in range(N-1):
        M_i = Message[i*16:i*16+16]
        for i in range(len(M)):
            Y[i] = M_i[i] ^ X[i]
        X = cipher.encrypt(M)
    
    for i in range(len(M_last)):
        Y[i] = M_last[i] ^ X[i]
    T = cipher.encrypt(Y)

    return T[0:CMAC_size]        



IV = bytearray.fromhex("3410de8f1aba3eff9f5a117172eacabd")
RLC = bytearray.fromhex("000002")
key = bytearray.fromhex("42877D3B087BC978708C672F6C33F175")
Data_enc = bytearray.fromhex("E4E31AF0E4C921")
M   = bytearray.fromhex("31E4E31AF0E4C921")
CMAC_received = bytearray.fromhex("B2DEB7")
Const_zero = bytearray.fromhex("00000000000000000000000000000000")
Const_Rb = bytearray.fromhex("00000000000000000000000000000087")

print(CMAC_calc(key, M, RLC, 3).hex())

# INIT_KEY XOR RLC
for i in range(len(RLC)):
    IV[i] = IV[i] ^ RLC[i]


#Encrypt IV XOR RLC
cipher = AES.new(key, AES.MODE_ECB)
ENC = cipher.encrypt(IV)

#ENC XOR Data_enc
for i in range(len(Data_enc)):
    Data_enc[i] = Data_enc[i] ^ ENC[i]

print("Decrypt Data = " + bytes(Data_enc).hex())



    


# file_out = open("encrypted.bin", "wb")
# file_out.write(IV)
# file_out.write(ENC)
# file_out.write(Data_enc)
# [ file_out.write(x) for x in (ciphertext) ]
# file_out.close()