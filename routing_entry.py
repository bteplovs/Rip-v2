from enum import Enum
from constant import *

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