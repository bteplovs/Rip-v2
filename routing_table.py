from constant import *
from enum import Enum

class RouteState(Enum):
    VALID = 1
    INVALID = 2
    GARBAGE = 3

class RoutingEntry:
    def __init__(self, next_hop, metric, state=RouteState.VALID):
        self.next_hop = next_hop
        self.metric = metric
        self.clock = 0
        self.state = state

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

    def update_route_timers(self, elapsed_time):
        to_delete = []
        triggered = []

        for destination, entry in self.entries.items():
            entry.clock += elapsed_time

            if entry.state == RouteState.VALID and entry.clock > TIMEOUT:
                entry.set_invalid()
                entry.set_metric_inf()
                entry.reset_clock()
                triggered.append((destination, entry))

            elif entry.state == RouteState.INVALID and entry.clock > GARBAGE:
                entry.set_garbage()
                to_delete.append(destination)

            elif entry.state == RouteState.GARBAGE:
                to_delete.append(destination)

        for destination in to_delete:
            self.delete_route(destination)

        return triggered

    def update_routing_table(self, update, neighbours):

        changed_routes = []


        pass

    def __str__(self):
        pass