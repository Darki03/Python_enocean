from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
import bitstring

#K          = bytearray.fromhex("456E4F6365616E20476D62482E313300")
# AE8E1E5BE4A311DB18833C1E66E47556
K          = bytearray.fromhex("AE8E1E5BE4A311DB18833C1E66E47556")
Const_zero = bytearray.fromhex("00000000000000000000000000000000")
Const_Rb   = bytearray.fromhex("00000000000000000000000000000087")
M          = bytearray.fromhex("31508F78CF0000038000000000000000")
#93E592


#*********** Sub-key derivation from Key******************************#
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


#*********** CMAC computation******************************#
#Compute padded (if necessary) message XOR K2
for i in range(len(M)):
    M[i] = M[i] ^ K2.tobytes()[i]
#AES128 with K on previous vector
cipher = AES.new(K, AES.MODE_ECB)
CMAC_out = cipher.encrypt(M)
#*********************************************************************#

#***********************Display****************************#
print("L        = " + bytes(L).hex())
print("K1       = " + K1.tobytes().hex())
print("K2       = " + K2.tobytes().hex())
print("CMAC_in  = " + bytes(M).hex())
print("CMAC_out = " + bytes(CMAC_out[0:3]).hex())
#*********************************************************************#

K          = bytearray.fromhex("00000000000000000000000000000000")
IV         = bytearray.fromhex("0000000000000000000000000000450C")
cipher = AES.new(K, AES.MODE_ECB)
CMAC_out = cipher.encrypt(IV)
print("CMAC_out = " + bytes(CMAC_out).hex())
# L    = b891cec1aa2f0bd5a166e53c6f86bbe6
# K1   = 71239d83545e17ab42cdca78df0d774b
# K2   = e2473b06a8bc2f56859b94f1be1aee96
#        d317b47e67bc2f55059b94f1be1aee96
# CMAC = 93e592c4d0c3bc7712be5dd4a2c6d753