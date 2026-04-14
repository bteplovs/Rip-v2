from constant import *

class RIPHeader:
    """A class representing a RIP packet header

    Attributes:
        data: A byte array with the following structure
        +---------------+---------------+-------------------------------+
        |    command    |    version    |           RouterID            |
        +---------------+---------------+-------------------------------+
    """
    def __init__(self, router_id):
        """Initialises a RIP Header object
        
        Args:
            router_id: The id of the router sending the packet
        """
        self.data = bytearray(4)
        self.data[0] = COMMAND_RESPONSE
        self.data[1] = VERSION
        self.data[2:4] = router_id.to_bytes(2, "big")

class RIPEntry:
    """A class representing a RIP packet entry

    Attributes:
        data: A byte array with the following structure
        +-------------------------------+-------------------------------+
        |                          Destination                          |
        +-------------------------------+-------------------------------+
        |                             Metric                            |
        +-------------------------------+-------------------------------+
    """
    def __init__(self, destination, metric):
        """Initialises a RIP Entry object
        
        Args:
            destination: The destination node
            metric: The cost associated with the route.
        """
        self.data = bytearray(4)
        self.data[0:2] = destination.to_bytes(2, "big")
        self.data[2:4] = metric.to_bytes(2, "big")


def process_packet(data):
    """Processes incoming packets by seperating packets into parts, validating
    each part and returning a route tuple 
    
    Args:
        Data: Raw data recieved from sock
    
    Returns:
        routes: All routes received from a neighbour in the form (destination, metric, next_hop)
    """
    if data[0] != COMMAND_RESPONSE or data[1] != VERSION:
        return None

    # The id of the packet, inferred as the next_hop for all its entries
    next_hop = int.from_bytes(data[2:4], "big")

    if next_hop < MIN_ROUTER_ID or next_hop > MAX_ROUTER_ID:
        return None

    entries = data[4:]

    if len(entries) % 4 != 0:
        return None

    routes = []
    for i in range(0, len(entries), 4):
        chunk = entries[i:i + 4]
        destination = int.from_bytes(chunk[0:2], "big")
        metric = int.from_bytes(chunk[2:4], "big")

        if metric < 0 or metric > INFINITY:
            continue
        if destination < MIN_ROUTER_ID or destination > MAX_ROUTER_ID:
            continue

        routes.append((destination, metric, next_hop))

    return routes

def create_packet(routes, router_id, neighbour_id):
    """Constructs a RIP packet.
    
    Args:
        routes: A list of tuples: (dest, entry)
        router_id: The id of the router sending the packet
        neighbour_id: The id of the recieving router

    Returns:
        payload: Raw byte data of RIP Packet
    """
    payload = bytearray()
    payload.extend(RIPHeader(router_id).data)

    # advertise self as metric: zero
    payload.extend(RIPEntry(router_id, 0).data)

    for dest, entry in routes:
        metric = apply_poison_reverse(entry, neighbour_id)
        payload.extend(RIPEntry(dest, metric).data)

    return payload

def apply_poison_reverse(entry, neighbour_id):
    """Applies poison reverse to the metric of an entry
    
    If the route was learned from the neighbour, advertise it back with Invalid metric.

    Returns:
        metric: INFINITY (16) if the entries next hop is its neighbour, else metric
    """
    if entry.next_hop == neighbour_id:
        return INFINITY
    return entry.metric