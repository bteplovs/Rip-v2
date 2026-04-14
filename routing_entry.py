from enum import Enum
from constant import *

class RouteState(Enum):
    """Route status enum"""

    VALID = 1
    """Route is valid and metric is healthy"""

    INVALID = 2
    """Route is invalid due to INF metric or clock expiring"""

class RoutingEntry:
    """A class representing a routing table entry.

    Attributes:
        next_hop: The next hop used to reach the destination.
        metric: The cost associated with the route.
        clock: The clock tracks the age of the entry, 0 upon init
        state: The state of an entry as defined in [VALID, INVALID]
    """
    def __init__(self, next_hop, metric, state=RouteState.VALID):
        """Initialises a Routing Entry object
        
        Args:
            next_hop: The next hop used to reach the destination.
            metric: The cost associated with the route.
            state: The state of an entry, VALID by default
        """
        self.next_hop = next_hop
        self.metric = metric
        self.clock = 0
        self.state = state

    def reset_clock(self):
        """Resets a routes internal clock"""
        self.clock = 0

    def set_metric(self, metric):
        """Sets a routes metric.
        
        Args:
            metric: The updated cost associated with the route.
        """
        self.metric = metric

    def set_next_hop(self, next_hop):
        """Sets a routes next hop"""
        self.next_hop = next_hop

    def set_metric_inf(self):
        """Sets a routes metric to INFINITY"""
        self.metric = INFINITY

    def set_invalid(self):
        """Sets a routes status to INVALID"""
        self.state = RouteState.INVALID

    def set_valid(self):
        """Sets a routes status to VALID"""
        self.state = RouteState.VALID