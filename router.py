from socket import *
import routing_table
from constant import *
import time
import select
import random

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.neighbours = outputs
        self.routing_table = routing_table.RoutingTable(id)
        self.periodic_timer = PERIODIC * random.randint(0.8, 1.2)
        self.sockets = self.create_sockets(inputs)
        self.out_socket = self.sockets[0]
        self.routing = True

    def create_sockets(self, inputs):
        sockets = []
        for input in inputs:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((LOCALHOST, input))
            sockets.append(sock)
        return sockets
    
    def periodic_update(self):
        pass
        # Regarding periodic updates: You need to find out how to generate periodic timer
        # events and how to write own handlers for this event. It could also be useful to
        # introduce some randomness to the periodic updates, for example by setting the
        # timer in question randomly to a value that is uniformly distributed over the range
        # [0.8 · period, 1.2 · period]. Why could such a randomization be useful?

        # basicallyt send full routing table to neighbors!
        

    def run(self):
        now = time.time()

        while self.routing:
            current = time.time()
            elapsed_time = current - now
            now = current

            elapsed_time = time.time() - now

            readable, _, exceptional = select.select(self.sockets, [], self.sockets, 1)

            # Readable returns sockets which have data to be processed!

            update_triggered = self.routing_table.update_routes(elapsed_time)

            if update_triggered:
                pass
                # basicallyt send full routing table to neighbors!

            self.periodic_update()

            continue

            # if readable update routing table and send a response back!


            #use select() check for routing packet recieved from peer or timer event
            # handle events atomically!!!!
            # for each rt entry
            # check if entry is valid, check if expired, check if not valid is it garbage day?