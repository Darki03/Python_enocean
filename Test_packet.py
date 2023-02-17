#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol import security
from enocean.protocol.eep import EEP
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
from bitstring import BitArray
import ctypes


def assemble_radio_packet(transmitter_id):
    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
                              sender=transmitter_id,
                              CV=50,
                              TMP=21.5,
                              ES='true')




# communicator = SerialCommunicator(port=u'COM10', callback=None)
# communicator.start()
# print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))


# #print(enocean.utils.to_hex_string(assemble_radio_packet(communicator.base_id).build()))

#Key = [0x35, 0x10, 0xDE, 0x8F, 0x1A, 0xBA, 0x3E, 0xFF, 0x9F, 0x77, 0x11, 0x71, 0x72, 0xEA, 0xCA, 0xBD]

#Key = bytearray.fromhex("42877D3B087BC978708C672F6C33F175")

Key = bytearray.fromhex("869FAB7D296C9E48CEBFF34DF637358A")

Dat_send = enocean.utils.from_hex_string("8F:00:00:00:15:E0")
Raw1664=RadioPacket.create_raw(rorg=RORG.VLD, Raw_Data=Dat_send)

print(enocean.utils.to_hex_string(Raw1664.data[:-5]))
print(enocean.utils.to_hex_string(Raw1664.build()))

print("************************************")
Raw1664_enc = security.encdec_tlgrm(Key, Raw1664, [0x00, 0x00, 0x93], 0x8B)
print(enocean.utils.to_hex_string(Raw1664_enc.data[:-8]))
print(enocean.utils.to_hex_string(Raw1664_enc.data[-8:-5]))
RLC_find = security.find_RLC(Key, Raw1664_enc.data[:-8], Raw1664_enc.data[-8:-5], [0x00, 0x00, 0x00], 255)
print(enocean.utils.to_hex_string(RLC_find))
print(enocean.utils.to_hex_string(Raw1664_enc.data))
print(enocean.utils.to_hex_string(Raw1664_enc.build()))
#print(len(Raw1664_enc.build()))

print("************************************")
Raw1664_dec = security.encdec_tlgrm(Key, Raw1664_enc, [0x00, 0x00, 0x93], 0x8B)


print(enocean.utils.to_hex_string(Raw1664_dec.data))
print(enocean.utils.to_hex_string(Raw1664_dec.build()))
#print(enocean.utils.to_hex_string(Raw1664_dec.build()))
#print(len(Raw1664_dec.build()))
# communicator.send(Raw1664)


# communicator.stop()

# c_uint8 = ctypes.c_uint8

# class SLF_FIELDS(ctypes.BigEndianStructure):
#     _fields_ = [
#             ("RLC_ALGO", c_uint8, 2),
#             ("RLC_TX", c_uint8, 1),
#             ("MAC_ALGO", c_uint8, 2),
#             ("DATA_ENC", c_uint8, 3),
#         ]

# class SLF_FIELDS_U(ctypes.Union):
#     _fields_ = [("b", SLF_FIELDS),
#                 ("asbyte", c_uint8)]

# SLF = SLF_FIELDS_U()
# SLF.asbyte = 0x8B

# print(SLF.b.RLC_ALGO)
# print(SLF.b.RLC_TX)
# print(SLF.b.MAC_ALGO)
# print(SLF.b.DATA_ENC)
