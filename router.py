
import routing_table
import constant
import socket
import select
import random
import packet
import time

class Router:
    """A class representing a router.
    
    Attributes:
        id: The id of the router parsed from the config file.
        inputs: The input ports parsed from the config file.
        neighbours: A list of Neighbour objects parsed from the config file.
        routing_table: The router's routing table.
        periodic_timer: The routers periodic timer.
        periodic_clock: The clock tracks the age of the router.
        sockets: The sockets defined over the inputs.
        out_socket: The socket used to transmit packets to neighbours.
        routing: Boolean to check if routing is active.
    """
    def __init__(self, id, inputs, outputs):
        """Initialises a Router object

        Args:
            id: The id of the router parsed from the config file.
            inputs: The input ports parsed from the config file.
            outputs: A list of Neighbour objects parsed from the config file.
        """
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
        """Sets the routers periodic timer.
        
        Returns:
            A value that is uniformly distributed over the range [0.8 · PERIODIC, 1.2 · PERIODIC]
        """
        return constant.PERIODIC * random.uniform(0.8, 1.2)

    def create_sockets(self, inputs):
        """Creates UDP sockets for the router using input ports

        Args:
            inputs: The input ports parsed from the config file.

        Return:
            sockets: A list of socket objects
        """
        sockets = []
        for input in inputs:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((constant.LOCALHOST, input))
            sockets.append(s)
        return sockets
    
    def send_update(self, entries):
        """The main function for sending updates to neighbours. uses .sendto() to send UDP updates
        to all neighbours.
        
        Args:
            entries: A list of tuples (dest, entry)
        """
        for neighbour in self.neighbours:
            packet_to_send = packet.create_packet(entries, self.id, neighbour.id)
            self.out_socket.sendto(packet_to_send, (constant.LOCALHOST, neighbour.port))

    def run(self):
        """
        Starts the router
        """
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
                    data, _ = sock.recvfrom(constant.BUFFER)
                    # Returns RoutingEntry objects
                    update = packet.process_packet(data)
                    if update:
                        changed = self.routing_table.update_routing_table(update, self.neighbours)
                        if changed:
                            self.send_update(changed.items())
                            
            # Returns RoutingEntry objects
            updates = self.routing_table.update_route_status(elapsed_time)
            if updates:
                print("### Triggered update ###".center())
                self.send_update(updates)
                print(self.routing_table)

            if self.periodic_clock >= self.periodic_timer:
                print("### Periodic update ###".center())
                self.send_update(self.routing_table.entries.items())
                self.periodic_clock = 0
                self.periodic_timer = self.set_periodic_timer()
                print(self.routing_table)
            
            if exceptional:
                for sock in exceptional:
                    self.inputs.remove(sock)
                    sock.close()