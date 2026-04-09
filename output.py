from dataclasses import dataclass

@dataclass
class Output:
    input_port: int #the port number on which the peer router will listen to packets from the current instance. TODO can be renamed to output port?
    metric: int # represents the metric value for the link to the peer router
    router_id: int # the router-id of the peer route