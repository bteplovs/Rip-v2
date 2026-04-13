import socket
import routing_table
import constant
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
        return constant.PERIODIC * random.uniform(0.8, 1.2)

    def create_sockets(self, inputs):
        sockets = []
        for input in inputs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((constant.LOCALHOST, input))
            sockets.append(s)
        return sockets
    
    def send_update(self, entries):
        for neighbour in self.neighbours:
            packet_to_send = packet.create_packet(entries, self.id, neighbour.id)
            self.out_socket.sendto(packet_to_send, (constant.LOCALHOST, neighbour.port))

    def run(self):
        now = time.time()

        for neighbour in self.neighbours:
            self.routing_table.add_route(neighbour.id, neighbour.id, neighbour.metric)

        while self.routing:
            current = time.time()
            elapsed_time = current - now
            now = current

            self.periodic_clock += elapsed_time

            readable, _, exceptional = select.select(self.sockets, [], self.sockets, 1)

            if readable:
                for sock in readable:
                    data, address = sock.recvfrom(constant.BUFFER)
                    # Returns RoutingEntry objects
                    update = packet.process_packet(data)
                    if update:
                        changed = self.routing_table.update_routing_table(update, self.neighbours)
                        if changed:
                            self.send_update(changed.items())
                            
            # Returns RoutingEntry objects
            updates = self.routing_table.update_route_timers(elapsed_time)
            if updates:
                self.send_update(updates)
                print(self.routing_table)

            if self.periodic_clock >= self.periodic_timer:
                self.send_update(self.routing_table.entries.items())
                self.periodic_clock = 0
                self.periodic_timer = self.set_periodic_timer()
                print(self.routing_table)
            
            if exceptional:
                for sock in exceptional:
                    self.inputs.remove(sock)
                    sock.close()