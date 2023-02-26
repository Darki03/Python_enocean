#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket, Packet
from enocean.protocol.constants import PACKET, RORG, DECRYPT_RESULT
from enocean.protocol import security
import sys
import traceback

Key = bytearray.fromhex("869FAB7D296C9E48CEBFF34DF637358A")

try:
    import queue
except ImportError:
    import Queue as queue


def assemble_radio_packet(transmitter_id):
    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
                              sender=transmitter_id,
                              CV=50,
                              TMP=21.5,
                              ES='true')


init_logging()
communicator = SerialCommunicator(port=u'COM4')
communicator.start()
print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

#Initialize RLC
RLC = []

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = Packet(PACKET.RADIO_ERP1, data=[], optional=[])
        packet = communicator.receive.get(block=True, timeout=1)
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.SEC_ENCAPS and ( packet.sender == [0x05, 0x03, 0x06, 0x1B] or packet.destination == [0x05, 0x03, 0x06, 0x1B]):
            Decode_packet = packet.decrypt(Key, RLC, SLF_TI=0x8B)
            print(Decode_packet[1], Decode_packet[2])
            if Decode_packet[1] == DECRYPT_RESULT.OK:
                # print(enocean.utils.to_hex_string(Decode_packet[0].build()))
                RLC = Decode_packet[2]
                Decode_packet[0].select_eep(0x33, 0x00)
                Decode_packet[0].parse_eep()
                for k in Decode_packet[0].parsed:
                    print('%s: %s' % (k, Decode_packet[0].parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
            packet.select_eep(0x05, 0x00)
            packet.parse_eep()
            for k in packet.parsed:
                print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:
            # parse packet with given FUNC and TYPE
            for k in packet.parse_eep(0x02, 0x05):
                print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS1:
            # alternatively you can select FUNC and TYPE explicitely
            packet.select_eep(0x00, 0x01)
            # parse it
            packet.parse_eep()
            for k in packet.parsed:
                print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
            for k in packet.parse_eep(0x02, 0x02):
                print('%s: %s' % (k, packet.parsed[k]))
    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()