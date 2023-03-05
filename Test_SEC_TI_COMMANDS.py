from enocean.protocol.packet import RadioPacket, ChainedMSG, Packet, MSGChainer, SECTeachInPacket
from enocean.protocol import security
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET, RORG

try:
    import queue
except ImportError:
    import Queue as queue

SECTI = SECTeachInPacket.create_SECTI_chain(SLF=0x8B, destination=[0x05,0x06,0x06,0x05])

Dat_send = enocean.utils.from_hex_string("8F:00:00:00:15:E0")
Raw1664=RadioPacket.create_raw(rorg=RORG.VLD, Raw_Data=Dat_send, destination = [0x05, 0x03, 0x06, 0x1B])

print(enocean.utils.to_hex_string(SECTI[1].build()))
print(enocean.utils.to_hex_string(SECTI[1].SLF))
print(enocean.utils.to_hex_string(SECTI[1].RLC))
print(enocean.utils.to_hex_string(SECTI[1].KEY))

for packet in SECTI[0]:
    print(enocean.utils.to_hex_string(packet.build()))
    print(packet.IDX,":", packet.CNT,":",packet.PSK,":",packet.TYPE,":",packet.INFO)

# communicator = SerialCommunicator(port=u'COM4')
# communicator.start()
# print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

# communicator.send_list(SECTI)

# # for p in SECTI:
# #     communicator.send(p)
# #     print(enocean.utils.to_hex_string(p.build()))

# while communicator.is_alive():
#             try:
#                 packet = communicator.receive.get(block=True, timeout=0.1)
#                 # We're only interested in responses to the request in question.
#                 if packet.packet_type == PACKET.RESPONSE:
#                     print(enocean.utils.to_hex_string(packet.build()))
#                 # Put other packets back to the Queue.
#             except queue.Empty:
#                 continue
#             except KeyboardInterrupt:
#                 break
#             except Exception:
#                 break


# if communicator.is_alive():
#     communicator.stop()

