
from constant import *
import routing_entry

class RoutingTable:
    """A class representing a router's routing table.
    
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
        and the clock is reset. If the entry is invalid and the the entries internal clock is older than the GARBAGE timer then
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
        For each route, checks if the entry exists currently or was a neighbour. Computes 
        a new metric. Then checks incoming entries, using dest, metric, sender_id (next_hop)
        and updates the routing table accordingly
        
        Args:
            received_routes: Routes recieved from recieved from other RIP routers
            neighbours: The peer-routers as defined by the routers config file
        
        Returns:
            invalid_routes: invalid routes are returned as part of a triggered update
        """
        invalid_routes = {}

        for dest, metric, next_hop in received_routes:
            
            # Handle deleted nieghbours
            if next_hop not in self.entries:
                neighbour = next((n for n in neighbours if n.id == next_hop), None)
                if neighbour is None:
                    continue
                self.entries[next_hop] = routing_entry.RoutingEntry(next_hop, neighbour.metric)

            cost_to_sender = self.entries[next_hop].metric
            new_metric = min(metric + cost_to_sender, INFINITY)

            # advertises self, recieved, keep alive
            if dest == next_hop:
                if dest in self.entries:
                    self.entries[dest].reset_clock()
                    self.entries[dest].set_valid()
                continue

            if dest not in self.entries:
                if new_metric < INFINITY:
                    self.entries[dest] = routing_entry.RoutingEntry(next_hop, new_metric)
                continue

            entry = self.entries[dest]

            # if sender is next_hop
            if entry.next_hop == next_hop:
                entry.reset_clock()

                if new_metric >= INFINITY:
                    entry.set_invalid()
                    entry.set_metric_inf()
                    # As per spec, trigger only if metric is set to INF
                    invalid_routes[dest] = entry 

                elif entry.metric != new_metric:
                    entry.metric = new_metric
                    entry.set_valid()

                else:
                    entry.set_valid()

            elif new_metric < entry.metric:
                entry.metric = new_metric
                entry.next_hop = next_hop
                entry.reset_clock()
                entry.set_valid()

        return invalid_routes

    def __str__(self):
        """Returns a human-readable representation of the routing table."""
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