from constant import *
import routing_entry

class RoutingTable:
    """A class representing a routers routing table.
    
    Attributes:
        id: The id of the router parsed from the config file
        entries: The individual entry for each route in the table
    """
    def __init__(self, router_id):
        """Initialises an Routing Table object.
        
        Args:
            router_id: The id of the router parsed from the config file.
        
        """
        self.id = router_id
        self.entries = {}

    def add_route(self, destination, next_hop, metric):
        """Adds or updates an individual route to the routing table.
        Creates a routing entry object per destination
        
        Args: 
            destination: The destination node
            next_hop: The next hop used to reach the destination.
            metric: The cost associated with the route.
        """
        self.entries[destination] = routing_entry.RoutingEntry(next_hop, metric)

    def delete_route(self, destination):
        """Deletes an individual route from the routing table.
        
        Args: 
            destination: The destination node
        """
        self.entries.pop(destination, None)

    def update_route_status(self, elapsed_time):
        """Updates the status of router entries. for each entry, if the entry 
        is valid and the the entries internal clock is older than the TIMEOUT then
        the status of the entry is set to INVALID, metric is set to INFINITY (16)
        and the clock is reset

        if the entry is invalid and the the entries internal clock is older than the GARBAGE timer then
        the entry is queued for deletion
        
        Args:
            elapsed_time: The routers elapsed time. Used to update route clocks

        Returns:
            triggered_entries: If an entry is marked as Invalid a triggered update occurs and shares the
            metric of triggered entries
        """
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
        """Updates the routing table using recieved routes from other RIP routers.
        For each route, check if the entry exists, if not, try find it in neighbours (previous neighbour may have crashed).
        If neighbour, create entry

        Calculates new metric

        Checks:

        If a route advertises itself, then reset clock, and set valid.

        If a route is newly discovered, then create a new entry

        If an entry was originally learned from the same sender that sent the current sender, keep the route alive.

            If the metric is invalid (INF), then change the state of the entry to invalid

            Elif a new metric is advertised, change the metric and set valid

            Else set the entry valid
        
        If a better metric is advertised then update the entry, set valid, and reset clock
        
        Args:
            received_routes: Routes recieved from recieved from other RIP routers
            neighbours: The peer-routers as defined by the routers config file
        
        Returns:
            changed_routes: Changed routes are returned as part of a triggered update
        
        """
        changed_routes = {}

        for dest, metric, sender_id in received_routes:
            
            # Check removed route
            if sender_id not in self.entries:
                neighbour = next((n for n in neighbours if n.id == sender_id), None)
                if neighbour is None:
                    continue
                self.entries[sender_id] = routing_entry.RoutingEntry(sender_id, neighbour.metric)

            # calculate new metric
            cost_to_sender = self.entries[sender_id].metric
            new_metric = min(metric + cost_to_sender, INFINITY)

            # If a route advertises itself, reset timer, set valid
            if dest == sender_id:
                if dest in self.entries:
                    self.entries[dest].reset_clock()
                    self.entries[dest].set_valid()
                continue

            # If a route is newly discovered
            if dest not in self.entries:
                if new_metric < INFINITY:
                    self.entries[dest] = routing_entry.RoutingEntry(sender_id, new_metric)
                    changed_routes[dest] = self.entries[dest]
                continue

            entry = self.entries[dest]

            # If entry was learned from same sender, keep alive
            if entry.next_hop == sender_id:
                entry.reset_clock()
                # If metric is invalid (Unreachable)
                if new_metric >= INFINITY:
                    entry.set_invalid()
                    entry.set_metric_inf()
                    changed_routes[dest] = entry
                # if neighbour advertises new metric, trust neighbour
                elif entry.metric != new_metric:
                    entry.metric = new_metric
                    entry.set_valid()
                    changed_routes[dest] = entry
                # Metric stayed the same, reset validity
                else:
                    entry.set_valid()

            # If new metric improved on previous, update the entry 
            elif new_metric < entry.metric:
                entry.metric = new_metric
                entry.next_hop = sender_id
                entry.reset_clock()
                entry.set_valid()
                changed_routes[dest] = entry

        return changed_routes

    def __str__(self):
        """
        Returns a human-readable representation of the routing table.
        """
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