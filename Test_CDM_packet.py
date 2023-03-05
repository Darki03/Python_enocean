#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket, ChainedMSG, Packet, MSGChainer, SECTeachInPacket
from enocean.protocol import security
from enocean.protocol.eep import EEP
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
from bitstring import BitArray
import ctypes

RLC = []
Key = bytearray.fromhex("869FAB7D296C9E48CEBFF34DF637358A")

Dat_send = enocean.utils.from_hex_string("40:80:00:0A:31:CA:7A:F8:67:22:05:1C:9F:86:80")
Dat_send = enocean.utils.from_hex_string("33:C0:00:0A:BF:48:1C:DC:38:BE:05:1C:9F:86:80")
Option = enocean.utils.from_hex_string("00:05:03:05:06:39:00")

CDMp_1 = ChainedMSG(PACKET.RADIO_ERP1,Dat_send,Option)

chain = MSGChainer()

print(CDMp_1)
print(CDMp_1.rorg, CDMp_1.id, CDMp_1.idx, CDMp_1.chain_len, len(CDMp_1.data))
print(enocean.utils.to_hex_string(CDMp_1.build()))

Dat_send = enocean.utils.from_hex_string("40:81:3A:00:2A:9A:FF:05:1C:9F:86:80")
Dat_send = enocean.utils.from_hex_string("33:C1:0C:39:3C:22:05:1C:9F:86:80")
Option = enocean.utils.from_hex_string("00:05:03:05:06:39:00")

chain.parse_CDM(CDMp_1)

CDMp_2 = ChainedMSG(PACKET.RADIO_ERP1,Dat_send,Option)

print(CDMp_2)
print(CDMp_2.rorg, CDMp_2.id, CDMp_2.idx, CDMp_2.chain_len, len(CDMp_2.data))
print(enocean.utils.to_hex_string(CDMp_2.build()))

vpacket = chain.parse_CDM(CDMp_2)

print(enocean.utils.to_hex_string(vpacket.build()))
print(vpacket.decrypt(Key,RLC,0x8B))


