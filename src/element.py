#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import tkinter as tk

class Element(tk.Frame):

    # internal State
    is_paired = True
    MIN_POWER = 0
    MAX_POWER = 255
    status_old = 1
    
    def __init__(self, master, pos):
        tk.Frame.__init__(self, master)
        self.grid(row=pos)
        
        self.id = tk.StringVar()
        self.id.set("ID")
        self.status = tk.IntVar()
        self.status.set(1)
        self.power = tk.StringVar()
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
                                              command=self.status_cmd,
                                              value=1)
        self.status_on_radio.grid(row=0, column=0)             
        self.status_off_radio = tk.Radiobutton(self.status_frame, text="OFF", 
                                              variable=self.status,
                                              command=self.status_cmd,
                                              value=0)
        self.status_off_radio.grid(row=1, column=0)          
        # Power
        okay_entry = self.register(self.power_entry_cmd)
        self.power_entry = tk.Entry(self, textvariable=self.power, width=3,
                                    validatecommand=(okay_entry, '%P'),
                                    validate='key')
        self.power_entry.grid(row=0, column=2)  
        self.power_entry["state"]=tk.DISABLED      
        self.power_scale = tk.Scale(self, variable=self.power, 
                                    from_=self.MIN_POWER, to=self.MAX_POWER,
                                    orient=tk.HORIZONTAL,
                                    command=self.power_scale_cmd)
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
    
    
    def status_cmd(self):
        if self.status_old and not self.status.get():
            print("switch off")
            self.power_scale["state"]=tk.DISABLED 
        elif not self.status_old and self.status.get():
            print("switch on")  
            self.power_scale["state"]=tk.ACTIVE 
        
        self.status_old = self.status.get()      
        
    def power_entry_cmd(self, value):        
        if value == "":
            value = "0"
        elif not value.isdigit():
            return False
        
        value = str(int(value))
        #Limit verification with power_scale        
        self.power.set(value)
        
        
        return True
        
    def power_scale_cmd(self, value):
        # Fait avec l'entry
        print("  ++", self.power.get(), value)
        pass
        
    def pair_cmd(self):
        if self.is_paired:
            self.unappair()
        else:
            self.appair()
            
    def unappair(self):
        self.status_frame.grid_remove()
        self.power_scale.grid_remove()
        self.power_entry.grid_remove()
        self.posx_label.grid_remove()
        self.posy_label.grid_remove()
        self.date_label.grid_remove()
        self.pair_button["text"] = "appair"
        
        self.is_paired = False
        
    def appair(self):
        self.status_frame.grid()
        self.power_scale.grid()
        self.power_entry.grid()
        self.posx_label.grid()
        self.posy_label.grid()
        self.date_label.grid()
        self.pair_button["text"] = "unappair"
        
        self.is_paired = True
