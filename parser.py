from constant import *
import configparser

class Neighbour:
    def __init__(self, port, metric, id):
        self.port = port
        self.metric = metric
        self.id = id

class Parser:
    def __init__(self):
        self.router_id = -1
        self.input_ports = []
        self.neighbours = []

    def read_config(self, config_path):
        
        config = configparser.ConfigParser()
        config.read(config_path)

        router = config["Router"]
        router_id = int(router["router-id"])
        input_ports = [int(p.strip()) for p in router["input-ports"].split(",")]

        router_neighbours = self.parse_neighbour(router)

        self.valid_router_id(router_id)
        self.valid_input_ports(input_ports)
        self.valid_neighbours(router_neighbours)

        self.router_id = router_id
        self.input_ports = input_ports

        self.valid_neighbour_ports(router_neighbours)

        self.neighbours = router_neighbours

    def valid_router_id(self, router_id):
        if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
            raise ValueError("ERROR: Invalid router ID")

    def valid_input_ports(self, ports): 
        if len(set(ports)) != len(ports):
            raise ValueError("ERROR: Duplicate ports")
        for port in ports:
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: Invalid port")

    def valid_neighbours(self, neighbours):  
        for neighbour in neighbours:

            port, metric, rid = neighbour.port, neighbour.metric, neighbour.id

            if rid < MIN_ROUTER_ID or rid > MAX_ROUTER_ID:
                raise ValueError("ERROR: Invalid router ID")
            
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: Invalid port")
            
            if metric < 0:
                raise ValueError("ERROR: Invalid metric")

    def valid_neighbour_ports(self, neighbours):
        input_set = set(self.input_ports)
        output_set = set()

        for neighbour in neighbours:
            if neighbour.port in input_set:
                raise ValueError("ERROR: Duplicate ports")

            if neighbour.port in output_set:
                raise ValueError("ERROR: Duplicate ports")

            output_set.add(neighbour.port)
    
    def parse_neighbour(self, config):
        outputs = []
        for entry in config["outputs"].split(","):
            parts = entry.strip().split("-")
            if len(parts) != 3:
                raise ValueError("ERROR: Invalid neighbours")

            port, metric, id = map(int, parts)
            outputs.append(Neighbour(port, metric, id))
        return outputs

