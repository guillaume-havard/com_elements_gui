#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""


import tkinter as tk
from element import *

class Application(tk.Frame):
    
    elements = []
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self["height"] = 200
        #self["width"] = 200
        #self.grid_propagate(0)
        self.grid()
        
        self.frame_options = tk.Frame(self)
        self.frame_options.grid(row=0)
        self.frame_elements = tk.Frame(self)
        self.frame_elements.grid(row=1)
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.grid(row=2)
        
        self.createWidgets()
                
    def createWidgets(self):
       
        self.bdd_load = tk.Button(self.frame_options, text="Load BdD", command=self.say_hi)        
        self.bdd_load.grid(row=0, column=0)
        self.bdd_save = tk.Button(self.frame_options, text="Save BdD", command=self.say_goodbye)        
        self.bdd_save.grid(row=0, column=1)
        
        self.add_element()        
        self.add_element()
        self.add_element()
        
        self.elements[0].unappair()
        self.elements[0].appair()
        self.elements[1].unappair()
        
        self.QUIT = tk.Button(self.frame_bottom, text="QUIT", fg="red",
                                            command=self.master.destroy)
        self.QUIT.grid()
                                
    def add_element(self):
        """
        Ajoute un element dans frame_elements.
        Par la suite fera un lien avec un modèle element.
        """
        # Pour le moment ajoute à la fin
        index = self.frame_elements.grid_size()[1]        
        self.elements.append(Element(self.frame_elements, index))
                
    def say_hi(self):
        print("hi there, everyone!")
        print(self.elements[0].power_spin.get())
        print(self.elements[0].power.get())
        
        print(self.elements[0].id.get())
        print(self.elements[0].status.get())
        print(self.elements[0].power.get())
        print(self.elements[0].posx.get())
        print(self.elements[0].posy.get())
        print(self.elements[0].date.get())
        
    def say_goodbye(self):
        print("Goodbye, everyone!")
        print(self.elements[0].power.set("33"))  
        print(self.elements[0].posx.set("33"))       
        
        
        
        
        
        
        
        
