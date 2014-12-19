#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import serial


class UsartComm():
    NB_BYTES = 5;
    
    def __init__(self):
        #open port
        self.port = None
        
    def read(self):
        #port.read()
        pass
    
    def write(self, message):
        #port.write(message)
        pass
