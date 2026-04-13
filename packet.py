from constant import *

class RIPHeader:
    def __init__(self, router_id):
        self.data = bytearray(4)
        self.data[0] = COMMAND_RESPONSE
        self.data[1] = VERSION
        self.data[2:4] = router_id.to_bytes(2, "big")

class RIPEntry:
    def __init__(self, destination, metric):
        self.data = bytearray(4)
        self.data[0:2] = destination.to_bytes(2, "big")
        self.data[2:4] = metric.to_bytes(2, "big")


def process_packet(data):
    if data[0] != COMMAND_RESPONSE or data[1] != VERSION:
        return None

    sender_id = int.from_bytes(data[2:4], "big")
    entries = data[4:]

    if len(entries) % 4 != 0:
        return None

    routes = []
    for i in range(0, len(entries), 4):
        chunk = entries[i:i + 4]
        destination = int.from_bytes(chunk[0:2], "big")
        metric = int.from_bytes(chunk[2:4], "big")

        if metric < 1 or metric > INFINITY:
            continue

        routes.append((destination, metric, sender_id))

    return routes

def create_packet(routes, router_id, neighbour_id):
    payload = bytearray()
    payload.extend(RIPHeader(router_id).data)
    payload.extend(RIPEntry(router_id, 1).data)
    for dest, entry in routes:
        metric = apply_poison_reverse(entry, neighbour_id)
        payload.extend(RIPEntry(dest, metric).data)

    return payload

def apply_poison_reverse(entry, neighbour_id):
    if entry.next_hop == neighbour_id:
        return INFINITY
    return entry.metric