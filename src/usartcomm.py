#!/usr/bin/python3

"""
Copyright (c) 2014 Guillaume Havard - BVS
"""
import serial

PRESENCE = 0x01
ON = 0x02
OFF = 0x03
CHANGE = 0x04
DEMAND_PAIRING = 0x0A
PAIRING = 0x0B
UNPAIRING = 0x0C

ACK = 0x10

RES = 0xC0
S_OK = 0x00
S_NOT_OK = 0x40
M_NOT_OK = 0x80

##
ACK_PRES = ACK | PRESENCE

class UsartComm():
    NB_BYTES = 5;
    
    def __init__(self):        
        self.port = serial.Serial("/dev/ttyAMA0", 
                         baudrate=115200, 
                         timeout=5, #0: no timeout, None: blocking mode
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,)
        
    def read(self, nb=None):
        return self.port.read(nb)
    
    def write(self, message):
        self.port.write(message)
        
        
        
        
        
        
        
        
