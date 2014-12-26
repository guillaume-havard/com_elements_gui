#!/usr/bin/python3

"""
Copyright (c) 2014 Guillaume Havard - BVS
"""

import sys
import os
import time
import serial

import signal

port = serial.Serial("/dev/ttyAMA0", 
                         baudrate=115200, 
                         timeout=0,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,)

bdd_light_status = [[1, 1, 45], [3, 0, 0], [4, 1, 23]]

def get_connected_ID():

#	Return ID of all the connected slaves
#	return : integer, list; ID of all the connectedslaves

	list_ID = []
	for element in bdd_light_status:
		list_ID.append(element[0])
	return list_ID

print("nb slave", len(get_connected_ID()))

ID_MAITRE = 0x66

	
def signal_handler(signal, frame):
    print('Fermeture du programme')
    port.close()
    sys.exit(0)

def print_message(buff):
    """
    Affiche un message
    """
    for b in buff:
        print(b, end=" ")
    print()
    
if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)
    
    buff = []
    
    
    
    while(1):
        ## ENVOIE  
        print()        
        print("entrez une commande : dest(11) etat(0/1) [puissance](0-255)")
        cmd = input()
        cmds = cmd.split(' ')
        print(len(cmds))
        if len(cmd) == 0:
            cmds = [b'1', b'2',b'3',b'4',b'5']        
        # Appairage
        elif len(cmds) == 2:
            cmds = [cmds[0], 
                    ID_MAITRE, cmds[1],
                    0xFF, 0xFF]        
        # Commande          
        elif len(cmds) == 3:
            cmds = [cmds[0], 
                    ID_MAITRE, 0x09,
                    cmds[1], cmds[2]]       
        else:
            print("Mauvais message")
            continue  
            
        for i in range(len(cmds)):
            cmds[i] = int(cmds[i])
            cmds[i] = bytes(cmds[i].to_bytes(1, byteorder='big'))
                    
        cmd = b''.join(cmds)        
        print_message(cmd)
        port.write(cmd)
    
        time.sleep(0.2)
        ## RECEPTION    
        rcv = b''
        rcv_tmp = port.read(5)        
        while (len(rcv_tmp) != 0):
            rcv = rcv_tmp
            rcv_tmp = port.read(5)
            print(rcv_tmp)
                     
        if len(rcv) != 0:            
            for b in rcv:
                buff.append(b)
            
        if len(buff) != 0:
            print("reponse :", buff)
            del buff[:]
        else:
            print("Pas de reponse")
