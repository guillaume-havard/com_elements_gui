#!/usr/bin/python3

""" 
Copyright (c) 2014 Guillaume Havard - BVS
"""
import tkinter as tk
from tkinter import messagebox


class Element(tk.Frame):
    """
    TODO: Message status
    TODO: Message change power
    TODO: Message pair
    """

    # internal State
    is_paired = True
    MIN_POWER = 0
    MAX_POWER = 255
    status_old = None
    
    def __init__(self, master, pos, lm, slave_id):
        """
        lm LightMaster : reference to the lightMaster
        slave_id : slave this element will be representing
        """
        tk.Frame.__init__(self, master)
        self.grid(row=pos)
        
        self.lm = lm
                
        self.id = tk.IntVar()
        self.id.set(slave_id)
        self.status = tk.IntVar()
        self.status.set(0)
        self.status_old = not self.status.get()
        self.power = tk.IntVar()
        self.power.set(0)
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
        self.power_entry = tk.Entry(self, textvariable=self.power, width=3,
                                    validate='key')
        self.power_entry.grid(row=0, column=2)  
        self.power_entry["state"]=tk.DISABLED      
        self.power_scale = tk.Scale(self, variable=self.power, 
                                    from_=self.MIN_POWER, to=self.MAX_POWER,
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
        self.pair_button = tk.Button(self, text="unappair",
                                     command=self.pair_cmd)
        self.pair_button.grid(row=0, column=7)
    
        self.update_GUI()
        
        self.gui_add_cmd()
    
    def gui_add_cmd(self):
        """
        Add command to widgets
        """
        self.status_on_radio["command"] = self.status_cmd
        self.status_off_radio["command"] = self.status_cmd
        
        okay_entry = self.register(self.power_entry_cmd)
        self.power_entry["validatecommand"] = (okay_entry, '%P')
        #self.power_scale["command"] = self.power_scale_cmd
    
    def status_cmd(self):
         self.status_action()
    
    def status_action(self):
        if self.status_old and not self.status.get():
            print("Element::status_action switch off")
            self.lm.cmd_switch_off(self.id.get())
            self.power_scale["state"]=tk.DISABLED 
        elif not self.status_old and self.status.get():
            print("Element::status_action switch on")
            self.lm.cmd_switch_on(self.id.get())
            self.power_scale["state"]=tk.ACTIVE 
        
        self.status_old = self.status.get()      
        
    def power_entry_cmd(self, value):        
        # Not used for the moment, used as a label        
        self.lm.cmd_change_power(self.id.get(), self.power.get())
        
        return True
        
    def power_scale_cmd(self, value):
        # Fait avec l'entry
        #print("  ++", self.power.get(), value)
        self.lm.cmd_change_power(self.id.get(), self.power.get())
        pass
        
    def pair_cmd(self):
        if self.is_paired:
            ret = messagebox.askokcancel("verification",
                                    "Do you want to unappair this element ?",
                                    default=messagebox.CANCEL)
            if ret:
                self.unappair()
                self.lm.cmd_unappair(self.id.get())
        else:
            self.appair()
            self.lm.cmd_appair(self.id.get())
            
    def unappair(self):
        self.status_frame.grid_remove()
        self.power_scale.grid_remove()
        self.power_entry.grid_remove()
        self.posx_label.grid_remove()
        self.posy_label.grid_remove()
        self.pair_button["text"] = "appair"
        
        self.is_paired = False
        
    def appair(self):
        self.status_frame.grid()
        self.power_scale.grid()
        self.power_entry.grid()
        self.posx_label.grid()
        self.posy_label.grid()
        self.pair_button["text"] = "unappair"
        
        self.is_paired = True
        
    def update_GUI(self):
        """
        Update widgets according to values
        """
        self.status_action()
        
        if self.is_paired:            
            self.appair()
        else:
            self.unappair()
        
        
