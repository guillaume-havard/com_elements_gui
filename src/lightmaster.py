#!/usr/bin/python3

"""

2014/12/19 - Guillaume Havard: bases
    
Copyright (c) 2014 Guillaume Havard - BVS
"""

import light
import usartcomm

class LightMaster():
    """
    Take care off all communication with the slave lights
    """    
    
    def __init__(self):
        self.lights = []
        self.serial = usartcomm.UsartComm()
        
    def loop(self):
        """
        Main loop of the application.
        Will be in charge to retrieve all messages from slaves
        and change the display according to thoses messages.
        """
        pass
        
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



