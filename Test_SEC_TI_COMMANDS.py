from enocean.protocol.packet import RadioPacket, ChainedMSG, Packet, MSGChainer, SECTeachInPacket
from enocean.protocol import security
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET, RORG, DECRYPT_RESULT
import sys
import traceback

try:
    import queue
except ImportError:
    import Queue as queue

SECTI = SECTeachInPacket.create_SECTI_chain(SLF=0x8B, destination=[0x05,0x03,0x06,0x1B])

# Dat_send = enocean.utils.from_hex_string("8F:00:00:00:15:E0")
# Raw1664=RadioPacket.create_raw(rorg=RORG.VLD, Raw_Data=Dat_send, destination = [0x05, 0x03, 0x06, 0x1B])

# print(enocean.utils.to_hex_string(SECTI[1].build()))
# print(enocean.utils.to_hex_string(SECTI[1].SLF))
# print(enocean.utils.to_hex_string(SECTI[1].RLC))
# print(enocean.utils.to_hex_string(SECTI[1].KEY))

# for packet in SECTI[0]:
#     print(enocean.utils.to_hex_string(packet.build()))
#     print(packet.IDX,":", packet.CNT,":",packet.PSK,":",packet.TYPE,":",packet.INFO)

#Initialize RLC
RLC = []

communicator = SerialCommunicator(port=u'COM4')
communicator.start()
print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

communicator.send_list(SECTI[0])

# for p in SECTI:
#     communicator.send(p)
#     print(enocean.utils.to_hex_string(p.build()))

while communicator.is_alive():
            try:
                packet = communicator.receive.get(block=True, timeout=0.1)
                # We're only interested in responses to the request in question.
                if packet.packet_type == PACKET.RESPONSE:
                    print(enocean.utils.to_hex_string(packet.build()))
                # Put other packets back to the Queue.
                if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.SEC_ENCAPS and (packet.destination == [0x05, 0x03, 0x06, 0x1B] or packet.sender == [0x05, 0x03, 0x06, 0x1B]):
                    Decode_packet = packet.decrypt(bytearray(SECTI[1].KEY), RLC, SECTI[1].SLF)
                    # print(Decode_packet[1], Decode_packet[2])
                    if Decode_packet[1] == DECRYPT_RESULT.OK:
                        # print(enocean.utils.to_hex_string(Decode_packet[0].build()))
                        RLC = Decode_packet[2]
                        Decode_packet[0].select_eep(0x33, 0x00)
                        Decode_packet[0].parse_eep()
                        for k in Decode_packet[0].parsed:
                            print('%s: %s' % (k, Decode_packet[0].parsed[k]))
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break
            except Exception:
                traceback.print_exc(file=sys.stdout)
                break


if communicator.is_alive():
    communicator.stop()

