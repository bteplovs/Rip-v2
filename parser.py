
from constant import *
import configparser

class Neighbour:
    """A class representing a routers neighbour.

    Attributes:
        port: The output port parsed from the config file.
        metric: The cost associated with the route.
        id: The id of the router parsed from the config file.
    """
    def __init__(self, port, metric, id):
        """Initialises a Neighbour object.
        
        Args:
            port: The output port parsed from the config file.
            metric: The cost associated with the route.
            id: The id of the router parsed from the config file.
        """
        self.port = port
        self.metric = metric
        self.id = id

class Parser:
    """A class representing a parser
    
    Attributes:
        router_id: The id of the router parsed from the config file.
        input_ports: The input ports parsed from the config file.
        neighbours: A list of neighbour objects parsed from config outputs
    """
    def __init__(self):
        """Initialises a Parser object"""
        self.router_id = -1
        self.input_ports = []
        self.neighbours = []

    def read_config(self, config_path):
        """Parses the config file and sets Parser attributes.

        Args:
            config_path: The file path to a locally saved config file
        """
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
        """Validates the parsed router id.

        Args:
            router_id: The id of the router parsed from the config file.
        """
        if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
            raise ValueError("ERROR: Invalid router ID")

    def valid_input_ports(self, ports):
        """Validates the parsed input ports.

        Args:
            ports: The input ports parsed from the config file.
        """
        if len(set(ports)) != len(ports):
            raise ValueError("ERROR: Duplicate ports")
        for port in ports:
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: Invalid port")

    def valid_neighbours(self, neighbours):
        """Validates the parsed neighbours.

        Args:
            neighbours: A list of neighbour objects parsed from config outputs
        """
        for neighbour in neighbours:

            port, metric, rid = neighbour.port, neighbour.metric, neighbour.id

            if rid < MIN_ROUTER_ID or rid > MAX_ROUTER_ID:
                raise ValueError("ERROR: Invalid router ID")
            
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: Invalid port")
            
            if metric < 1 or metric > MAX_METRIC:
                raise ValueError("ERROR: Invalid metric")

    def valid_neighbour_ports(self, neighbours):
        """Validates output and input ports are correctly structured.

        Args:
            neighbours: A list of neighbour objects parsed from config outputs
        """
        input_set = set(self.input_ports)
        output_set = set()

        for neighbour in neighbours:
            if neighbour.port in input_set:
                raise ValueError("ERROR: Duplicate ports")

            if neighbour.port in output_set:
                raise ValueError("ERROR: Duplicate ports")

            output_set.add(neighbour.port)
    
    def parse_neighbour(self, config):
        """Parses each output (neighbour)

        Args:
           config: configParser object containing config file

        Returns:
            outputs: A list of neighbour objects parsed from config outputs
        """
        outputs = []
        for entry in config["outputs"].split(","):
            parts = entry.strip().split("-")
            if len(parts) != 3:
                raise ValueError("ERROR: Invalid neighbours")

            port, metric, id = map(int, parts)
            outputs.append(Neighbour(port, metric, id))
        return outputs

