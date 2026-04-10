from socket import *
import routing_table
from constant import *

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs
        self.rt = routing_table.RoutingTable(id)
        self.sockets = self.create_sockets()

    def run(self):

        # enter infinite loop
        routing = True
        while routing:
            pass
            #use select() check for routing packet recieved from peer or timer event
            # handle events atomically!!!!
            # for each rt entry
            # check if entry is valid, check if expired, check if not valid is it garbage day?