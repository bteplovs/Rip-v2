from dataclasses import dataclass
from constant import *
import configparser

@dataclass
class Neighbour:
    port: int
    metric: int
    id: int

class Parser:
    def __init__(self):
        self.router_id = -1
        self.input_ports = []
        self.neighbour = []

    def read_config(self, config_path):
        
        config = configparser.ConfigParser()
        config.read(config_path)

        # TODO: The first three parameters (router-id, input-ports, outputs) are mandatory

        router = config["Router"]
        router_id = int(router["router-id"])
        input_ports = [int(p.strip()) for p in router["input-ports"].split(",")]

        neighbours = self.parse_neighbour(router)

        self.valid_router_id(router_id)
        self.valid_input_ports(input_ports)
        self.valid_neighbours(neighbours)

        self.router_id = router_id
        self.input_ports = input_ports

        self.valid_neighbour_ports(neighbours)

        self.neighbour = neighbours

    def valid_router_id(self, router_id):
        if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
            raise ValueError("ERROR: invalid router ID")

    def valid_input_ports(self, ports): 
        if len(set(ports)) != len(ports):
            raise ValueError("ERROR: duplicate ports")
        for port in ports:
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: invalid port")

    def valid_neighbours(self, neighbours):  
        for neighbour in neighbours:

            port, metric, rid = neighbour.port, neighbour.metric, neighbour.id

            if rid < MIN_ROUTER_ID or rid > MAX_ROUTER_ID:
                raise ValueError
            
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError
            
            if metric < 0:
                raise ValueError

    def valid_neighbour_ports(self, neighbours):
        input_set = set(self.input_ports)
        output_set = set()

        for neighbour in neighbours:
            if neighbour.port in input_set:
                raise ValueError()

            if neighbour.port in output_set:
                raise ValueError()

            output_set.add(neighbour.port)
    
    def parse_neighbour(self, config):
        outputs = []
        for entry in config["outputs"].split(","):
            parts = entry.strip().split("-")
            if len(parts) != 3:
                raise ValueError(f"Invalid output format: {entry}")

            port, metric, id = map(int, parts)
            outputs.append(Neighbour(port, metric, id))
        return outputs

