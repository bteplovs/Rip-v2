from constant import *
import routing_entry

class RoutingTable:
    def __init__(self, router_id):
        self.id = router_id
        self.entries = {}

    def add_route(self, destination, next_hop, metric):
        self.entries[destination] = routing_entry.RoutingEntry(next_hop, metric)

    def delete_route(self, destination):
        self.entries.pop(destination, None)

    def update_route_timers(self, elapsed_time):
        to_delete = []
        triggered_entries = []

        for destination, entry in self.entries.items():

            entry.clock += elapsed_time

            if entry.state == routing_entry.RouteState.VALID and entry.clock > TIMEOUT:
                entry.set_invalid()
                entry.set_metric_inf()
                entry.reset_clock()
                triggered_entries.append((destination, entry))

            elif entry.state == routing_entry.RouteState.INVALID and entry.clock > GARBAGE:
                to_delete.append(destination) 

        for destination in to_delete:
            self.delete_route(destination)

        return triggered_entries

    def update_routing_table(self, received_routes, neighbours):
        changed_routes = {}

        for dest, metric, sender_id in received_routes:
            
            if sender_id not in self.entries:
                neighbour = next((n for n in neighbours if n.id == sender_id), None)
                if neighbour is None:
                    continue
                self.entries[sender_id] = routing_entry.RoutingEntry(sender_id, neighbour.metric)

            cost_to_sender = self.entries[sender_id].metric
            new_metric = min(metric + cost_to_sender, INFINITY)

            
            if dest == sender_id:
                if dest in self.entries:
                    self.entries[dest].reset_clock()
                    self.entries[dest].set_valid()
                continue

            
            if dest not in self.entries:
                if new_metric < INFINITY:
                    self.entries[dest] = routing_entry.RoutingEntry(sender_id, new_metric)
                    changed_routes[dest] = self.entries[dest]
                continue

            entry = self.entries[dest]

            
            if entry.next_hop == sender_id:
                entry.reset_clock()
                if new_metric >= INFINITY:
                    entry.set_invalid()
                    entry.set_metric_inf()
                    changed_routes[dest] = entry
                elif entry.metric != new_metric:
                    entry.metric = new_metric
                    entry.set_valid()
                    changed_routes[dest] = entry
                else:
                    entry.set_valid()

            elif new_metric < entry.metric:
                entry.metric = new_metric
                entry.next_hop = sender_id
                entry.reset_clock()
                entry.set_valid()
                changed_routes[dest] = entry

        return changed_routes

    def __str__(self):
        header = f"{'Dest':>6} {'Next Hop':>9} {'Metric':>7} {'Clock':>7} {'State':>8}"
        divider = "-" * len(header)
        title = f"# Routing Table (Router {self.id}) #".center(len(header))
        lines = ["", title, divider, header, divider]

        if self.entries:
            for dest, e in self.entries.items():
                lines.append(f"{dest:>6} {e.next_hop:>9} {e.metric:>7} {e.clock:>7.1f} {e.state.name:>8}")
        else:
            lines.append("# NO ENTRIES #".center(len(header)))

        lines.append(divider)
        lines.append("")
        return "\n".join(lines)