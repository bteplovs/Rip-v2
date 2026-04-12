from constant import *
from routing_table import RoutingEntry

class RIPHeader:
    def __init__(self, id):
        self.data = bytearray(4)
        self.data[0] = COMMAND_RESPONSE
        self.data[1] = VERSION
        self.data[2:4] = id.to_bytes(2, "big")

class RIPEntry:
    def __init__(self, next_hop, metric):
        self.data = bytearray(4)
        self.data[0] = next_hop
        self.data[1] = metric


def process_packet(data):

    if data[0] != COMMAND_RESPONSE or data[1] != VERSION:
        return None

    sender_id = int.from_bytes(data[2:4], "big")

    routes = []

    entries = data[4:]

    if len(entries) % 4 != 0:
        return None 

    for i in range(0, len(entries), 4):
        chunk = entries[i:i+4]

        next_hop = int.from_bytes(chunk[0:2], "big")
        metric = int.from_bytes(chunk[2:4], "big")

        if metric < 1 or metric > INFINITY:
            continue

        routes.append((next_hop, metric, sender_id))

    return routes

def create_packet(routes, id, neighbour_id):
    packet = RIPHeader(id)

    for route in routes.values():

        metric = apply_poison_reverse(route, neighbour_id)

        entry = RIPEntry(route.next_hop.to_bytes(2, "big"), metric.to_bytes(2, "big"))
        packet.extend(entry)

    return packet

def apply_poison_reverse(route, neighbour_id):
    if route.next_hop == neighbour_id:
        return INFINITY
    return route.metric