import os
import logging
from sys import version_info
from collections import OrderedDict
from bs4 import BeautifulSoup
from enocean.protocol.packet import RadioPacket

import enocean.utils
from enocean.protocol.constants import RORG

#*** Test for packet creation from EEP
# Test_packet = RadioPacket.create(RORG.BS1,0x00,0x01,CO=0, LRN=0)
# print(enocean.utils.to_hex_string(Test_packet.build()))

Test_packet = RadioPacket.create(RORG.VLD,0x33,0x00, destination=[0x05, 0x06, 0x30, 0x1B], mid=2, MID=2, TSP=9)
print(enocean.utils.to_hex_string(Test_packet.build()))




#Load eep268.xml file get from http://tools.enocean-alliance.org/EEPViewer/#2
# with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'eep268.xml'), 'r', encoding='UTF-16LE') as xml_file:
#     xml_file.readline()
#     EEP_soup = BeautifulSoup(xml_file.read(), features='xml')

# #Profile tag
# Profile = EEP_soup.profile


# print("******************")

#Load XML [RORG][FUNC][TYPE] : Type contents
# telegrams = {
#             enocean.utils.from_hex_string(telegram.number.string): {
#                 enocean.utils.from_hex_string(function.number.string): {
#                     enocean.utils.from_hex_string(type.number.string, ): type
#                     for type in function.find_all('type', recursive=False)
#                 }
#                 for function in telegram.find_all('func', recursive=False)
#             }
#             for telegram in Profile.find_all(recursive=False)
#       }

#Get [RORG][FUNC][TYPE] contents for tests
# Profile_type = telegrams[0xD5][0x00][0x01]
# Profile_type = telegrams[0xD2][0x33][0x00]
# Profile_type = telegrams[0xF6][0x02][0x02]

# Dat_send = enocean.utils.from_hex_string("8F:00:00:00:15:E0")
# Raw1664=RadioPacket.create_raw(rorg=RORG.VLD, Raw_Data=Dat_send, destination = [0x05, 0x03, 0x06, 0x1B])

# Dat_send = [enocean.utils.from_hex_string("30")]
# Raw1664=RadioPacket.create_raw(rorg=RORG.RPS, Raw_Data=Dat_send, status=0x30)
# print(enocean.utils.to_hex_string(Raw1664.build()))

# Dat_send = [enocean.utils.from_hex_string("08")]
# Raw1664=RadioPacket.create_raw(rorg=RORG.BS1, Raw_Data=Dat_send)
# print(enocean.utils.to_hex_string(Raw1664.build()))


#*********** Test for condition type contents find (bidirectionnal or status)
# Condit = Profile_type.find_all('condition')
# Case = Profile_type.find('case')
# if Condit is not None:
#      cond = []
     
#      for option in Condit:
#         for cond_i in option:
#             if cond_i.name == 'datafield':
                
#                 offset = int(option.find('bitoffs').string)
#                 size = int(option.find('bitsize').string)
#                 raw_cond = int(''.join(['1' if digit else '0' for digit in Raw1664._bit_data[offset:offset + size]]), 2)
#                 val = option.find('value', string = str(raw_cond))
#                 cond.append(val.string if val is not None else None)

#             if cond_i.name == 'statusfield':
#                 offset = int(cond_i.find('bitoffs').string)
#                 size = int(cond_i.find('bitsize').string)
#                 raw_cond = int(''.join(['1' if digit else '0' for digit in Raw1664._bit_status[offset:offset + size]]), 2)
#                 # cond.append(option.find('value', string = str(raw_cond)).string or 0)
#                 val = option.find('value', string = str(raw_cond))
#                 cond.append(val.string if val is not None else None)

#         print(cond)
#         print("******####******")          
#         if None in cond:
#             cond.clear()
#         else:
#              Case = option.find_parent('case')
#              break
# data_condit = Case.find_all(['datafield', 'statusfield'], recursive = False)
# print("**************")
# data_size = 0
# for offs in Case.find_all('bitsize'):
#     if offs.find_parent('condition') is None:
#         print(int(offs.string))
#         data_size += int(offs.string)
# print(data_size)
# # print(data_condit)

# for source in data_condit:
#             if source.name == 'statusfield':
#                  print(source.find('data').string.strip())

#             if source.name == 'datafield':
    
#                  for data in source:
 
#                     if not data.name:
#                         continue
#                     if data.name == 'range':
#                         rng = source.find('range')
#                         rng_min = float(rng.find('min').string)
#                         rng_max = float(rng.find('max').string)
#                         print(rng_max, rng_min)

#                     if data.name == 'enum':
#                         # print(data.name)
#                         value_desc = source.find('value', string = str(0))
#                         # print(repr(i) for i in value_desc.find_next('description').strings or None)
#                         if value_desc is not None: 
#                             for st in value_desc.find_next('description').stripped_strings: print(st)
#**********************************************************#

#********** Tests with original EEP.xml file *************#

# with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'EEP.xml'), 'r', encoding='UTF-8') as xml_file:
#     xml_file.readline()
#     EEP_old_soup = BeautifulSoup(xml_file.read(), features='xml')

# telegrams = {
#             enocean.utils.from_hex_string(telegram['rorg']): {
#                 enocean.utils.from_hex_string(function['func']): {
#                     enocean.utils.from_hex_string(type['type'], ): type
#                     for type in function.find_all('profile')
#                 }
#                 for function in telegram.find_all('profiles')
#             }
#             for telegram in EEP_old_soup.find_all('telegram')
#       }

# Profile_type = telegrams[0xD2][0x01][0x01]

# print(Profile_type)

# print(Profile_type.get('bits', '1'))
#**********************************************************#


