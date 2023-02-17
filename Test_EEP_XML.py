import os
import logging
from sys import version_info
from collections import OrderedDict
from bs4 import BeautifulSoup

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
Profile_type = telegrams[0xD5][0x00][0x01]

for source in Profile_type.find_all('datafield'):
    print(source.name)
    for data in source:
        
    # value_desc = source.find('item').find('value')
    # print(value_desc)
    # #print(value_desc.find_next('description').string.strip())
    # for data in source.contents:

        if not data.name:
                continue
        if data.name == 'value':
            print(data.name)
            offset = int(data.find('bitoffs'))
        if data.name == 'enum':
            print(data.name)
            print(source.find('shortcut'))
            print(source.find('description').string or [0])
            print(source.find('bitoffs'))
            print(data.find('value', string=str(0)))
            print(data.find('value', string=str(1)).find_next('description'))
            offset = int(source.find('bitoffs').string)
            print(offset)
        if data.name == 'status':
            print(data.name)

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