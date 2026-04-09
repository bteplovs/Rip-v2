import sys
from config import *

from socket import *



# Runs the main loop
# hands over packets to rip.py

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs

        self.time_out = None #SOME GLOBAL VAR 180 seconds
        self.garbage_collection = None #SOME GLOBAL VAR 120 seconds


    def run(self):
        
        print(f"RIP router {self.id} successfully initilised")

        #create routing table
        # Routing
        # create sockets

        #enter infinite loop
        routing = True
        while routing:
            pass
            #use select() check for routing packet recieved from peer or timer event
            # handle events atomically!!!!
            # 