import os
import logging
from sys import version_info
from collections import OrderedDict
from bs4 import BeautifulSoup
from enocean.protocol.packet import RadioPacket

import enocean.utils
from enocean.protocol.constants import RORG


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'eep268.xml'), 'r', encoding='UTF-16LE') as xml_file:
    xml_file.readline()
    EEP_soup = BeautifulSoup(xml_file.read(), features='xml')

Profile = EEP_soup.profile

# for tag in EEP_soup.find_all('type'):
#     if tag.number != None and len(tag.number) != 0 : print("TYPE : " + tag.number.string)

for rorg_xml in Profile.find_all(recursive=False):
    print("RORG : ", rorg_xml.number.string)

    for function in rorg_xml.find_all('func', recursive=False):
        print("FUNCTION : " , function.number.string)

        for type in function.find_all('type', recursive=False):
            print("TYPE : " , type.number.string)

print("******************")

# for tag in EEP_soup.find_all('rorg'):
#     if tag.number != None and len(tag.number) != 0 : print("RORG : " + tag.number.string) 
    
#     for function in tag.find_all('func'):
#         if function.number != None and len(function.number) != 0 : print("FUNC : " + function.number.string)

#     for type in tag.find_all('type'):
#         if type.number != None and len(type.number) != 0 : print("TYPE : " + type.number.string)

print("******************")

telegrams = {
            enocean.utils.from_hex_string(telegram.number.string): {
                enocean.utils.from_hex_string(function.number.string): {
                    enocean.utils.from_hex_string(type.number.string, ): type
                    for type in function.find_all('type', recursive=False)
                }
                for function in telegram.find_all('func', recursive=False)
            }
            for telegram in Profile.find_all(recursive=False)
      }
Profile_type = telegrams[0xD2][0x33][0x00]

Dat_send = enocean.utils.from_hex_string("8F:00:00:00:15:E0")
Raw1664=RadioPacket.create_raw(rorg=RORG.VLD, Raw_Data=Dat_send, destination = [0x05, 0x03, 0x06, 0x1B])

Condit = Profile_type.find_all('condition')

if Condit is not None:
    for option in Condit:
        offset = int(option.find('bitoffs').string)
        size = int(option.find('bitsize').string)
        raw_cond = int(''.join(['1' if digit else '0' for digit in Raw1664._bit_data[offset:offset + size]]), 2)
        cond = option.find('value', string = str(raw_cond))
        if cond is not None:
            Case = cond.find_parent('case')

data_condit = Case.find_all('datafield', recursive = False)

for source in data_condit:
            for data in source:
                if not data.name:
                    continue
                if data.name == 'range':
                    rng = source.find('range')
                    rng_min = float(rng.find('min').string)
                    rng_max = float(rng.find('max').string)
                    print(rng_max, rng_min)

# print(len(Condit))
# print([i.find('value', string = str(8)) for i in Condit])

# for source in Profile_type.find_all('case'):
#     print(source.name)
#     offset = int(source.find('bitoffs').string)
#     size = int(source.find('bitsize').string)
#     raw_cond = int(''.join(['1' if digit else '0' for digit in Raw1664._bit_data[offset:offset + size]]), 2)
#     cond = source.find('value', string = str(raw_cond))
#     if cond is not None:
#         print(cond.find_parent('case'))
    # for data in source:
    #     print(data.name)
    #     if data.name == 'condition':
    #         offset = int(source.find('bitoffs').string)
    #         size = int(source.find('bitsize').string)
    #         print(offset)
    #         print(size)
            
        
    # value_desc = source.find('item').find('value')
    # print(value_desc)
    # #print(value_desc.find_next('description').string.strip())
    # for data in source.contents:

        # if not data.name:
        #         continue
        
        # if data.name == 'condition':
        #     print(data.name)
        # if data.name == 'value':
        #     print(data.name)
            
            # offset = int(data.find('bitoffs'))
        # if data.name == 'enum':
        #     print(data.name)
            # print(source.find('shortcut'))
            # print(source.find('description').string or [0])
            # print(source.find('bitoffs'))
            # print(data.find('value', string=str(0)))
            # print(data.find('value', string=str(1)).find_next('description'))
            # offset = int(source.find('bitoffs').string)
            # print(offset)
        # if data.name == 'status':
        #     print(data.name)

print("******************")

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

# print(telegrams[0xD5])