from socket import *
import routing_table
from constant import *
import time
import select
import random
import packet

class Router:

    def __init__(self, id, inputs, outputs):
        self.id = id
        self.inputs = inputs
        self.neighbours = outputs
        self.routing_table = routing_table.RoutingTable(id)
        self.periodic_timer = self.set_periodic_timer()
        self.periodic_clock = 0
        self.sockets = self.create_sockets(inputs)
        self.out_socket = self.sockets[0]
        self.routing = True

    def set_periodic_timer(self):
        return PERIODIC * random.uniform(0.8, 1.2)

    def create_sockets(self, inputs):
        sockets = []
        for input in inputs:
            s = socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((LOCALHOST, input))
            sockets.append(s)
        return sockets
    
    def send_update(self, routes):
        for neighbour in self.neighbours:
            packet_to_send = packet.create_packet(routes, self.id, neighbour.id)
            self.out_socket.sendto(neighbour.port, packet_to_send)

    def run(self):
        now = time.time()

        while self.routing:
            current = time.time()
            elapsed_time = current - now
            now = current

            self.periodic_clock += elapsed_time

            readable, _, exceptional = select.select(self.sockets, [], self.sockets, 1)

            for sock in readable:
                data, address = sock.recvfrom(BUFFER)
                update = packet.process_packet(data)
                if update:
                    changed_routes = self.routing_table.update_routing_table(update, address)
                    if changed_routes:
                        self.send_update(changed_routes)
                    
            updates = self.routing_table.update_route_timers(elapsed_time)
            if updates:
                self.send_update(updates)

            if self.periodic_clock >= self.periodic_timer:
                self.send_update(self.routing_table.entries.values())
                self.periodic_clock = 0
                self.periodic_timer = self.set_periodic_timer()
            
            if exceptional:
                for sock in exceptional:
                    self.inputs.remove(sock)
                    sock.close()