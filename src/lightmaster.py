#!/usr/bin/python3

"""    
Copyright (c) 2014 Guillaume Havard - BVS
"""
import datetime
import light
import usartcomm

# TODO: change status when cmd.
# TODO: finish is_paired (alwas True for the moment)

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
            print("---")
            self.print_slaves()
            self.print_messages()
            ret = self.serial.read(5)            
            if ret is None:
                continue
            if len(ret) == 5:
                self.process_message(ret)
        
    def process_message(self, message):
        """"
        Process a slave's message
        """
        message = self.message_to_int(message)
        if message[0] != self.id and message[0] != 0xFF:
            return -1        
           
        id_slave = message[1]
        self.update_light_time(message)
        
        if message[2] == usartcomm.PRESENCE:
            # Présence du luminaire
            if not self.is_paired(id_slave):
                return -1
            self.check_command(id_slave)
        elif message[2] == usartcomm.DEMAND_PAIRING:
            # Demande d'appairage
            # TODO: enlever le not
            if not self.is_paired(id_slave):
                return -1
            self.check_pairing(id_slave)
        elif message[2] & usartcomm.ACK == usartcomm.ACK:
            # Acknowledgment commande
            print("ACKNOLEDGMENT")
        else:
            # Unknown type of message
            print("Unknown:", message)
            pass
    
    def slave_index(self, id_slave):
        """
        return the index of the slave in self.slavec
        If the a slave is not found a new one is created
        """
        i = 0
        while i < len(self.slaves):            
            if self.slaves[i].id == id_slave:
                break
            i += 1
        
        if i == len(self.slaves):
            self.slaves.append(light.Light(id_slave))
            
        return i
        
    def update_light_time(self, message):
        """
        update light state according to messages send by slaves
        """                
        index = self.slave_index(message[1])
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
                self.send_message(self.messages[i])
                del self.messages[i]
                return 1
                
        return -1
        
    def is_paired(self, id_slave):
        """
        return True if the slave is paired, false otherwise
        """
        return True
    
    ## Command that can be sent
                
    def cmd_appair(self, id_slave):
        """
        Send a pairing acknowledgment to the slave
        Add the slave to the slave liste
        id_slave int: id of the slave
        """
        if not self.is_paired(id_slave):
            return -1
            
        message = [id_slave, self.id, usartcomm.PAIRING, 0xFF, 0xFF]
        self.messages_pairing.append(message)
    
    def cmd_unappair(self, id_slave):
        """
        Unappair the slave
        id_slave int: id of the slave
        """
        if not self.is_paired(id_slave):
            return -1
            
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.UNPAIRING, 0xFF]
        self.add_message(message)
        
    def cmd_switch_on(self, id_slave, power=0):
        """
        Switch on the slave
        id_slave int: id of the slave
        power int [0;255], power of the light
        """
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.ON, power]
        self.add_message(message)
    
    def cmd_switch_off(self, id_slave):
        """
        Switch off the slave
        id_slave int: id of the slave        
        """
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.OFF, 0xFF]
        self.add_message(message)
    
    def cmd_change_power(self, id_slave, power):
        """
        Change the power of a slave
        id_slave int: id of the slave
        power int [0;255], power of the light
        """
        if not self.is_paired(id_slave):
            return -1
        
        message = [id_slave, self.id, usartcomm.ACK_PRES,
                   usartcomm.CHANGE, power]
        self.add_message(message)
        
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
        # Appairage
        elif len(cmds) == 2:
            cmds = [cmds[0], 
                    lm.id, cmds[1],
                    0xFF, 0xFF]        
        # Commande          
        elif len(cmds) == 3:
            cmds = [cmds[0], 
                    lm.id, 0x09,
                    cmds[1], cmds[2]]       
        else:
            print("Mauvais message")
            continue  
            
        for i in range(len(cmds)):
            cmds[i] = int(cmds[i])
            #cmds[i] = bytes(cmds[i].to_bytes(1, byteorder='big'))
                    
        #cmd = b''.join(cmds) 
        #port.write(cmd)
        lm.add_message(cmds)
        



