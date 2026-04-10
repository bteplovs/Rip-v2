from constant import *
from enum import Enum

class RouteState(Enum):
    VALID = 1
    INVALID = 2
    GARBAGE = 3

class RoutingEntry:
    def __init__(self, next_hop, metric):
        self.next_hop = next_hop
        self.metric = metric
        self.clock = 0
        self.state = RouteState.VALID

    def reset_clock(self):
        self.clock = 0

    def set_metric(self, metric):
        self.metric = metric
    
    def set_next_hop(self, next_hop):
        self.next_hop = next_hop

    def set_metric_inf(self):
        self.metric = INFINITY

    def set_garbage(self):
        self.state = RouteState.GARBAGE

    def set_invalid(self):
        self.state = RouteState.INVALID

class RoutingTable:
    def __init__(self, router_id):
        self.id = router_id
        self.entries = {}
    
    def add_route(self, destination, routing_entry):
        self.entries[destination] = routing_entry
    
    def delete_route(self, destination):
        self.entries.pop(destination, None)

    def update_routes(self, clock):

        for destination, entry in self.entries:
            #TODO: check state and timer for garbage, and validity
            pass

    def __str__():
        pass