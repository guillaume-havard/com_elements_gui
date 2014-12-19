#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import tkinter as tk

class Element(tk.Frame):

    def __init__(self, master, pos):
        tk.Frame.__init__(self, master)
        self.grid(row=pos)
        
        self.id = tk.StringVar()
        self.id.set("ID")
        self.status = tk.IntVar()
        self.status.set(1)
        self.power = tk.IntVar()
        self.power.set(1)
        self.posx = tk.StringVar()
        self.posx.set("X")
        self.posy = tk.StringVar()
        self.posy.set("Y")
        self.date = tk.StringVar()
        self.date.set("temps")
        
        # Id
        self.id_label = tk.Label(self, textvariable=self.id)
        self.id_label.grid(row=0, column=0)
        # Status
        self.status_frame = tk.Frame(self)
        self.status_frame.grid(row=0, column=1)
        self.status_on_radio = tk.Radiobutton(self.status_frame, text="ON", 
                                              variable=self.status,
                                              value=1)
        self.status_on_radio.grid(row=0, column=0)             
        self.status_off_radio = tk.Radiobutton(self.status_frame, text="OFF", 
                                              variable=self.status,
                                              value=0)
        self.status_off_radio.grid(row=1, column=0)          
        # Power
        self.power_entry = tk.Entry(self, textvariable=self.power, width=3)
        self.power_entry.grid(row=0, column=2)        
        self.power_scale = tk.Scale(self, variable=self.power, from_=0, to=255,
                                    orient=tk.HORIZONTAL)
        self.power_scale.grid(row=0, column=3)        
        # Posx
        self.posx_label = tk.Label(self, textvariable=self.posx)
        self.posx_label.grid(row=0, column=4)
        # Posy
        self.posy_label = tk.Label(self, textvariable=self.posy)
        self.posy_label.grid(row=0, column=5)
        # Date
        self.date_label = tk.Label(self, textvariable=self.date)
        self.date_label.grid(row=0, column=6)
        # Pairing button 
        self.pair_button = tk.Button(self, text="unappair")
        self.pair_button.grid(row=0, column=7)
        
    def unappair(self):
        self.status_frame.grid_remove()
        self.power_scale.grid_remove()
        self.power_entry.grid_remove()
        self.posx_label.grid_remove()
        self.posy_label.grid_remove()
        self.date_label.grid_remove()
        self.pair_button["text"] = "appair"
        
    def appair(self):
        self.status_frame.grid()
        self.power_scale.grid()
        self.power_entry.grid()
        self.posx_label.grid()
        self.posy_label.grid()
        self.date_label.grid()
        self.pair_button["text"] = "unappair"
