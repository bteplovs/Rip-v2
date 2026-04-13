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
    
    def set_valid(self):
        self.state = RouteState.VALID

class RoutingTable:
    def __init__(self, router_id):
        self.id = router_id
        self.entries = {}
    
    def add_route(self, destination, next_hop, metric):
        self.entries[destination] = RoutingEntry(next_hop, metric)
    
    def delete_route(self, destination):
        self.entries.pop(destination, None)

    def update_route_timers(self, elapsed_time):
        to_delete = []
        triggered_entries = []

        for destination, entry in self.entries.items():
            entry.clock += elapsed_time

            if entry.state == RouteState.VALID and entry.clock > TIMEOUT:
                entry.set_invalid()
                entry.set_metric_inf()
                entry.reset_clock()
                triggered_entries.append(entry)

            elif entry.state == RouteState.INVALID and entry.clock > GARBAGE:
                entry.set_garbage()
                to_delete.append(destination)

        for destination in to_delete:
            self.delete_route(destination)

        return triggered_entries

    def update_routing_table(self, recieved_routes):

        changed_routes = []

        for destination, metric, sender_id in recieved_routes:

            new_metric = min(metric + 1, INFINITY)

            if destination not in self.entries:
                self.entries[destination] = RoutingEntry(sender_id, new_metric)
                changed_routes.append(destination)
            
            entry = self.entries[destination]

            if new_metric < entry.metric:
                entry.metric = new_metric
                entry.next_hop = sender_id
                entry.reset_clock()
                entry.set_valid()
                changed_routes.append(destination)
            
            elif entry.next_hop == sender_id:
                entry.metric = new_metric
                entry.reset_clock()
                changed_routes.append(destination)
        
        return changed_routes

    def __str__(self):
        header = f"{'Dest':>6} {'Next Hop':>9} {'Metric':>7} {'Clock':>7} {'State':>8}"
        divider = "-" * len(header)
        title = f"# Routing Table (Router {self.id}) #".center(len(header))
        lines = ["", title, divider, header, divider]
        if self.entries.items():
            for dest, e in self.entries.items():
                lines.append(f"{dest:>6} {e.next_hop:>9} {e.metric:>7} {e.clock:>7.1f} {e.state.name:>8}")
        else:
            lines.append("# NO ENTRIES #".center(len(header)))
        lines.append(divider)
        lines.append("")
        return "\n".join(lines)
        