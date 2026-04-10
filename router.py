from socket import *
import routing_table
from constant import *
import time
import select

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs
        self.routing_table = routing_table.RoutingTable(id)
        self.timer = 0
        self.sockets = self.create_sockets(inputs)
        self.routing = True

    def create_sockets(self, inputs):
        sockets = []
        for input in inputs:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((LOCALHOST, input))
            sockets.append()
        return sockets

    def run(self):

        now = time.time()

        while self.routing:

            elapsed_time = time.time() - now

            readable, _, exceptional = select.select(self.sockets, [], self.sockets, 1)

            # Readable returns sockets which have data to be processed!

            self.routing_table.update_routes(elapsed_time)

            self.periodic_update()

            continue
            #use select() check for routing packet recieved from peer or timer event
            # handle events atomically!!!!
            # for each rt entry
            # check if entry is valid, check if expired, check if not valid is it garbage day?