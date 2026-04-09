from socket import *
import routing_table

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs
        self.rt = routing_table.RoutingTable(id)

        self.time_out = None #SOME GLOBAL VAR 180 seconds
        self.garbage_collection = None #SOME GLOBAL VAR 120 seconds

        
        


    def run(self):

        #enter infinite loop
        routing = True
        while routing:
            pass
            #use select() check for routing packet recieved from peer or timer event
            # handle events atomically!!!!
            # 