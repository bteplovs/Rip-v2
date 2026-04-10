from constant import *
# stores routes
#tracks timers
#updates metrics
#removes stale routes
class RoutingTable:

    def __init__(self, router_id):
        self.id = router_id

        self.time_out = None #SOME GLOBAL VAR 180 seconds
        self.garbage_collection = None #SOME GLOBAL VAR 120 seconds