#!/usr/bin/python3

"""    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import datetime
import light
import usartcomm

SWITCH_STATE_OFF = 0
SWITCH_STATE_ON = 1
SWITCH_STATE_CHANGE = 2

class LightMaster():
    """
    Take care off all communication with the slave lights
    
    """   
    # Slave in communication with the master.
    # Paired or not.
    slaves = []
    # list of messages to be sent
    messages = []
    # list of pairing messages.
    messages_pairing = []
    # Not used for the moment
    acknowledgment = []
    # State, managed by the switch
    switch_state = SWITCH_STATE_CHANGE
    
    
    def __init__(self, id=102):
        self.id = id
        self.serial = usartcomm.UsartComm()
        self.ok = False
        
    def loop(self):
        """
        Main loop of the application.
        Will be in charge to retrieve all messages from slaves
        and change the display according to thoses messages.
        """        
        self.ok = True
        
        while self.ok:
            print("----")
            self.print_slaves()
            self.print_messages()
            ret = self.serial.read(5)           
            if ret is None:
                print("Pas de message")
                continue
            elif ret == b'':
                print("timeout")
                continue
                                
            if len(ret) == 5:
                self.process_message(ret)
        
    def process_message(self, message):
        """"
        Process a slave's message
        """
        message = self.message_to_int(message)
        print("message :", message)      
        if message[0] != self.id and message[0] != 0xFF:
            print("message pour un autre destinataire")
            return -1        
        
        # Message from the associated switch.
        if message[0] == 0xFF and message[1] == self.id :
            print("Message from the switch:", message[2])
            # Same state
            if message[2] == self.switch_state :
                print(" - Deja dans cet etat")
                message = [0xFF, self.id, 
                           message[2] | usartcomm.ACK | usartcomm.M_NOT_OK,
                           0xFF, 0xFF]
                self.send_message(message)
            
            if message[2] == usartcomm.OFF:
                print(" - Toutes les lumieres : off")
                self.switch_state = SWITCH_STATE_OFF
            elif message[2] == usartcomm.ON:
                print(" - Toutes les lumieres : on")
                self.switch_state = SWITCH_STATE_ON
            elif message[2] == usartcomm.CHANGE:
                print(" - Toutes les lumieres : auto")
                self.switch_state = SWITCH_STATE_CHANGE
                
            return 
                
        id_slave = message[1]
        self.update_light_time(message)
        
        if message[2] == usartcomm.PRESENCE:
            # Présence du luminaire
            self.check_command(id_slave)
        elif message[2] == usartcomm.DEMAND_PAIRING:
            # Demande d'appairage
            self.check_pairing(id_slave)
        elif message[2] & usartcomm.ACK == usartcomm.ACK:
            # Acknowledgment commande
            if message[2] & usartcomm.RES == usartcomm.S_NOT_OK:
                print("There is an error for the last command")
            self.check_command(id_slave)
        else:
            # Unknown type of message
            print("Unknown:", message)
            pass
    
    def slave_index(self, message):
        """
        return the index of the slave in self.slaves
        If the a slave is not found a new one is created with his state
        list(int) : message send by the slave
        """
        id_slave = message[1]
        
        i = self._slave_index(id_slave)
        
        if i == -1:
            print("création du slave {}".format(id_slave))
            self.slaves.append(light.Light(id_slave))
            #must be from a presence or a pairing message
            if message[2] == usartcomm.PRESENCE:            
                self.slaves[i].status = message[3]
                self.slaves[i].power = message[4]
            elif message[2] == usartcomm.DEMAND_PAIRING:
                self.slaves[i].status = 2
            else:
                print("Message not conform, Light not initilised")
            
        return i
        
    def slave_index_sec(self, id_slave):
        """
        return the index of the slave in self.slaves
        If the a slave is not found throw an exeption
        """
        i = self._slave_index(id_slave)
        
        if i == -1:
            raise IndexError("This slave {} do not exist".format(id_slave))
            pass
            
        return i
        
    def _slave_index(self, id_slave):
        """
        return the index of the slave in self.slaves
        If the a slave is not found return -1
        """
        i = 0
        while i < len(self.slaves):            
            if self.slaves[i].id == id_slave:
                break
            i += 1
        
        if i == len(self.slaves):
            return -1
            
        return i
        
    def update_light_time(self, message):
        """
        update light state according to messages send by slaves
        """          
        index = self.slave_index(message)
        self.slaves[index].time = datetime.datetime.now()        

    def message_to_int(self, message):
        
        ret = []
        for i in message:
            ret.append(int(i))
            
        return ret
    
    def check_pairing(self, id_slave):
        """
        Check if there a pairing for the slave
        """
        print("pairing of :", id_slave)
        for i in range(len(self.messages_pairing)):
            if self.messages_pairing[i][0] == id_slave:
                self.send_message(self.messages_pairing[i])
                del self.messages_pairing[i]
                return 1
        
        return -1
        
    def check_command(self, id_slave):
        """
        Check if there is a command demand for the slave
        """
        print("presence of :", id_slave)
        for i in range(len(self.messages)):
            if self.messages[i][0] == id_slave:
                self.f(self.messages[i])
                del self.messages[i]
                return 1
                
        return -1
        
    def is_slave(self, id_slave):
        """
        Indicate if the slave existe"
        """
        try:
            self.slave_index_sec(id_slave)
        except IndexError:
            return False
        
        return True
        
    def is_paired(self, id_slave):
        """
        return True if the slave is paired, false otherwise
        """
        try:
            i = self.slave_index_sec(id_slave)
        except IndexError:
            return False
        
        if self.slaves[i].status == 2:
            return False
        
        return True
        
    def update_status(self, id_slave, value):
        """
        Will update the data in memory
        id_slave int : id of the slave
        value int [0,1,2] : value to set
        """
        index = self.slave_index_sec(id_slave)
        self.slaves[index].status = value
        
    def update_power(self, id_slave, value):
        """
        Will update the data in memory
        id_slave int : id of the slave
        value int [0,1,2] : value to set
        """
        index = self.slave_index_sec(id_slave)
        self.slaves[index].power = value
    
    ## Command that can be sent
                
    def cmd_appair(self, id_slave):
        """
        Send a pairing acknowledgment to the slave
        Add the slave to the slave liste
        id_slave int: id of the slave
        """
        if not self.is_slave(id_slave):
            return -1
        if self.is_paired(id_slave):
            return -1
            
        message = [id_slave, self.id, usartcomm.PAIRING, 0xFF, 0xFF]
        self.messages_pairing.append(message) 
        self.update_status(id_slave, 0)
        print("self.messages_pairing", self.messages_pairing)
    
    def cmd_unappair(self, id_slave):
        """
        Unappair the slave
        id_slave int: id of the slave
        """
        if not self.is_slave(id_slave):
            return -1
        if not self.is_paired(id_slave):
            return -1
            
        message = [id_slave, self.id, usartcomm.UNPAIRING, 0xFF, 0xFF]
        self.add_message(message)
        self.update_status(id_slave, 2)
        
    def cmd_switch_on(self, id_slave, power=0):
        """
        Switch on the slave
        id_slave int: id of the slave
        power int [0;255], power of the light
        """
        if not self.is_slave(id_slave):
            return -1
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.ON, power]
        self.add_message(message)
        self.update_status(id_slave, 1)
    
    def cmd_switch_off(self, id_slave):
        """
        Switch off the slave
        id_slave int: id of the slave        
        """
        if not self.is_slave(id_slave):
            return -1
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.OFF, 0xFF]
        self.add_message(message)
        self.update_status(id_slave, 0)
    
    def cmd_change_power(self, id_slave, power):
        """
        Change the power of a slave
        id_slave int: id of the slave
        power int [0;255], power of the light
        """
        if not self.is_slave(id_slave):
            return -1
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.CHANGE, power]
        self.add_message(message)
        self.update_power(id_slave, power)
        
    ### Private
    def print_slaves(self):
        """
        Print the current states of all slaves
        """
        print("Slave list :")
        for i in self.slaves:
            print(i)
            
    def print_messages(self):
        """
        Print the current states of all slaves
        """
        print("message list :")
        for i in self.messages:
            print(i)
            
        if len(self.messages_pairing) > 0:
            print("pairing message list :")
            for i in self.messages_pairing:
                print(i)
            
    def add_message(self, message):
        """
        Add a message to be send next time a slave send a presence message
        Check if there already a message ? make a FIFO ?
        message : list(int)
        """
        if len(message) != 5:
            return -1
        else:
            print("Ajout du message :", message)
            self.messages.append(message)
            return 0
    
    def send_message(self, message):
        """
        Send the message via USART
        message : list(int)
        """
        for i in range(len(message)):
            message[i] = bytes(message[i].to_bytes(1, byteorder='big'))
                    
        message = b''.join(message)   
        self.serial.write(message)
           
    
"""
**Action modèle <-> vue**

* la vue change :
message est envoyé
[reception de la réponse]
le modèle est changé

* Un message slave :
-présence
temps mis à jour
vérifie que bien connecté ?
-demande d'appairage
temps mis à jour
vérifie que bien non connecté
-->
temps mis à jour
vérifie type connection


**Données**
lights = list de :

Faire en sorte que LightMaster fonctionne sans interface graphique

Puis lié la GUI.

"""
if __name__ == "__main__":
    import _thread
    lm = LightMaster()
    _thread.start_new_thread(lm.loop,())
    print("coucou")
    while(1):
        print("entrez une commande : dest(11) etat(0/1) [puissance](0-255)")
        cmd = input()
        cmds = cmd.split(' ')
        if len(cmd) == 0:
            cmds = [b'1', b'2',b'3',b'4',b'5']       
        elif len(cmds) == 1:
            if cmds[0] == "1":
                print("ON")
                lm.cmd_switch_on(11)
            elif cmds[0] == "2":
                print("OFF")
                lm.cmd_switch_off(11)
            elif cmds[0] == "3":
                print("CHANGE 255")
                lm.cmd_change_power(11, 255)
            elif cmds[0] == "4":
                print("CHANGE 0")
                lm.cmd_change_power(11, 0)
            elif cmds[0] == "8":
                print("APPAIR")
                lm.cmd_appair(11)
            elif cmds[0] == "9":
                print("UNAPPAIR")
                lm.cmd_unappair(11)
       
        



