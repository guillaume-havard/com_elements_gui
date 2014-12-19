#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import sys
import os
import time
import serial

bdd_light_status = [[1, 1, 45], [3, 0, 0], [4, 1, 23]]

def get_connected_ID():

#	Return ID of all the connected slaves
#	return : integer, list; ID of all the connectedslaves

	list_ID = []
	for element in bdd_light_status:
		list_ID.append(element[0])
	return list_ID

print("nb slave", len(get_connected_ID()))


port = serial.Serial("/dev/ttyAMA0", 
                         baudrate=115200, 
                         timeout=2,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,)

ID_MAITRE = 0x66
PROTOCOL_PRESENCE = 0x01
PROTOCOL_ACK = 0x08

def print_message(buff):
    """
    Affiche un message
    """
    for b in buff:
        print(b, end=" ")
    print()
    

def send_message(dest, cmd):
    """
    Send a message
    dest [in] int : 
    cmd [in] int : 
    """
    buff = b''
    
    buff += bytes(dest.to_bytes(1, byteorder='big'))
    buff += bytes(ID_MAITRE.to_bytes(1, byteorder='big'))
    buff += bytes(cmd.to_bytes(1, byteorder='big'))
    buff += bytes(0xFF.to_bytes(1, byteorder='big'))
    buff += bytes(0xFF.to_bytes(1, byteorder='big'))

    print("Envoie de", buff)
    print_message(buff)
    port.write(buff)
    return
    
def traitement_message(buff):
    """
    Récupere les informations et les traite comme un maitre Lucibel.
    
    buff [in] list(int) : 5 octets 
    """
    ### Attention taille
    if buff[0] != ID_MAITRE:
        print("Le message n'est pas pour le maitre")
        return
    if buff[2] == PROTOCOL_PRESENCE:
        print("l'esclave {} signifie sa presence".format(buff[1]))
        print("Nous acknowledgons sa presence")
        send_message(buff[1], PROTOCOL_PRESENCE | PROTOCOL_ACK)
    
    
if __name__ == "__main__":   
    
    buff = []
    
    while(1):    
        ## RECEPTION    
        rcv = port.read(5)
        if len(rcv) != 0:            
            for b in rcv:
                buff.append(int(b))
            
        if len(buff) != 0:
            print(buff)
            traitement_message(buff)
            del buff[:]
        
            
            
