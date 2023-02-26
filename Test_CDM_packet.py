#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket, ChainedMSG, Packet, MSGChainer
from enocean.protocol import security
from enocean.protocol.eep import EEP
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
from bitstring import BitArray
import ctypes



Dat_send = enocean.utils.from_hex_string("40:40:00:0A:31:CA:7A:F8:67:22:05:1C:9F:86:80")
Option = enocean.utils.from_hex_string("00:05:03:05:06:39:00")

CDMp_1 = ChainedMSG(PACKET.RADIO_ERP1,Dat_send,Option)

chain = MSGChainer()

print(CDMp_1)
print(CDMp_1.rorg, CDMp_1.id, CDMp_1.idx, CDMp_1.chain_len, len(CDMp_1.data))
print(enocean.utils.to_hex_string(CDMp_1.build()))

Dat_send = enocean.utils.from_hex_string("40:41:3A:00:2A:9A:FF:05:1C:9F:86:80")
Option = enocean.utils.from_hex_string("00:05:03:05:06:39:00")

chain.parse_CDM(CDMp_1)

CDMp_2 = ChainedMSG(PACKET.RADIO_ERP1,Dat_send,Option)

print(CDMp_2)
print(CDMp_2.rorg, CDMp_2.id, CDMp_2.idx, CDMp_2.chain_len, len(CDMp_2.data))
print(enocean.utils.to_hex_string(CDMp_2.build()))


print(chain.parse_CDM(CDMp_2))

