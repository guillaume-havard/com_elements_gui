#!/usr/bin/python3

"""    
Copyright (c) 2014 Guillaume Havard - BVS
"""

import light
import usartcomm

class LightMaster():
    """
    Take care off all communication with the slave lights
    """   
	messages = []
	acknowledgment = []
    
    def __init__(self, id=102):
		self.id = id
        self.lights = []
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
			ret = self.serial.read()
			if len(ret) == 5:
				process_message(ret)
        
	def process_message(self, message):
		""""
		Process a slave's message
		"""
		message = message_to_int(message)
		if message[0] != self.id:
			return -1
		if message[2] == 1: # Faire des "defines"
			# Présence du luminaire
			pass
		elif message[2] == 10
			# Demande d'appairage
			pass
		else
			# Acknowledgment de commande
			pass
		
	def message_to_int(self, message):
		
		ret = []
		for i in message:
			ret.append(int(i))
			
		return ret
	
	def add_message(self, message):
		"""
		Add a message to be send next time a slave send a presence message
		message : list(int)
		"""
		if len(message) != 5:
			return -1
		else
			messages.append(message)
			return 0
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



