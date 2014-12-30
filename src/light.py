#!/usr/bin/python3

""" 
Copyright (c) 2014 Guillaume Havard - BVS
"""

class Light():
        
    def __init__(self, id_l=-1):
        self.id = id_l
        # 0 : Off
        # 1 : On
        # 2 : Unappaired
        self.status = 0
        self.power = 0
        self.posx = -1
        self.posy = -1
        self.time = -1
    
    def __repr__(self):
        text = "Light[%r]: %r, %r/255 last comm %r" % (
                self.id, self.status, self.power, self.time)
        return text
