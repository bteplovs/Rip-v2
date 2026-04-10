from dataclasses import dataclass
from constant import *
import configparser

@dataclass
class Output:
    port: int
    metric: int
    router_id: int

class Parser:
    def __init__(self):
        self.router_id = -1
        self.input_ports = []
        self.output_ports = []

    def read_config(self, config_path):
        
        config = configparser.ConfigParser()
        config.read(config_path)

        router = config["Router"]
        router_id = int(router["router-id"])
        input_ports = [int(p.strip()) for p in router["input-ports"].split(",")]
        outputs = self.parse_output(router)

        self.valid_router_id(router_id)
        self.valid_input_ports(input_ports)
        self.valid_outputs(outputs)

        self.router_id = router_id
        self.input_ports = input_ports

        self.valid_output_ports(outputs)

        self.output_ports = outputs

    def valid_router_id(self, router_id):
        if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
            raise ValueError("ERROR: invalid router ID")

    def valid_input_ports(self, ports): 
        if len(set(ports)) != len(ports):
            raise ValueError("ERROR: duplicate ports")
        for port in ports:
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError("ERROR: invalid port")

    def valid_outputs(self, outputs):  
        for output in outputs:

            port, metric, rid = output.port, output.metric, output.router_id

            if rid < MIN_ROUTER_ID or rid > MAX_ROUTER_ID:
                raise ValueError
            
            if port < MIN_PORT or port > MAX_PORT:
                raise ValueError
            
            if metric < 0:
                raise ValueError

    def valid_output_ports(self, outputs):
        input_set = set(self.input_ports)
        output_set = set()

        for output in outputs:
            if output.port in input_set:
                raise ValueError()

            if output.port in output_set:
                raise ValueError()

            output_set.add(output.port)
    
    def parse_output(self, config):
        outputs = []
        for entry in config["outputs"].split(","):
            parts = entry.strip().split("-")
            if len(parts) != 3:
                raise ValueError(f"Invalid output format: {entry}")

            port, metric, rid = map(int, parts)
            outputs.append(Output(port, metric, rid))
        return outputs

