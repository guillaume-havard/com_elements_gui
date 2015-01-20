#!/usr/bin/python3

"""  
Copyright (c) 2014 Guillaume Havard - BVS
"""


import tkinter as tk
from element import *
import lightmaster
import _thread

class Application(tk.Frame):
    
    elements = []
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self["height"] = 200
        #self["width"] = 200
        #self.grid_propagate(0)
        self.grid()
        
        self.lm = lightmaster.LightMaster()
        
        self.frame_options = tk.Frame(self)
        self.frame_options.grid(row=0)
        self.frame_elements = tk.Frame(self)
        self.frame_elements.grid(row=1)
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.grid(row=2)
        
        self.createWidgets()
        
        self.update()
                
    def createWidgets(self):
       
        self.bdd_load = tk.Button(self.frame_options, text="Load BdD",
        command=self.load_BdD)        
        self.bdd_load.grid(row=0, column=0)
        self.bdd_save = tk.Button(self.frame_options, text="Save BdD",
        command=self.save_BdD)        
        self.bdd_save.grid(row=0, column=1)
                
        self.QUIT = tk.Button(self.frame_bottom, text="QUIT", fg="red",
                                            command=self.master.destroy)
        self.QUIT.grid()
        
        _thread.start_new_thread(self.lm.loop,())
                                
    def add_element(self, slave_id):
        """
        Ajoute un element dans frame_elements.
        Par la suite fera un lien avec un modèle element.
        """
        # Pour le moment ajoute à la fin
        index = self.frame_elements.grid_size()[1]        
        self.elements.append(Element(self.frame_elements, index, 
                                     self.lm, slave_id))
                
    def load_BdD(self):
        print("Application::load_BdD")
        
    def save_BdD(self):
        print("Application::save_BdD") 
        
    def update(self):
        """
        Update elements
        Check if there is new element linked with the LightMaster
        """
        if len(self.lm.slaves) != len(self.elements):
            self.add_element(self.lm.slaves[len(self.elements)].id)
            
        self.after(500, self.update)   
        
        
        
        
        
        
        
        
