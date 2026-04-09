from dataclasses import dataclass
from constant import *

@dataclass
class Output:
    output_port: int
    metric: int
    router_id: int

class Parser:
    def __init__(self):
        self.router_id = -1
        self.input_ports = []
        self.output_ports = []

    def read_config(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("router-id"):
                    self.router_id = self.validate_router_id(line)

                elif line.startswith("input-ports"):
                    self.input_ports = self.validate_input_ports(line)

                elif line.startswith("outputs"):
                    self.output_ports = self.validate_outputs(line)
                else:
                    raise ValueError("ERROR: Malformed config file")
        
        self.validate_ports()

    def validate_router_id(self, line):
        try:
            _, router_id = line.split()

            if len(line.split()) != 2:
                raise ValueError
            router_id = int(router_id)

            if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
                raise ValueError
            return router_id
        except ValueError:
            raise ValueError("ERROR: Invalid router-id")

    def validate_input_ports(self, line): 
        try:
            _, ports = line.split(" ", 1)
            ports = [int(port.strip()) for port in ports.split(",")]

            if len(set(ports)) != len(ports):
                raise ValueError
            for port in ports:

                if port < MIN_PORT or port > MAX_PORT:
                    raise ValueError
            return ports
        except ValueError:
            raise ValueError("ERROR: Invalid input ports")

    def validate_outputs(self, line):
        try:
            _, outputs_str = line.split(" ", 1)
            outputs = []
            for entry in outputs_str.split(','):
                parts = entry.strip().split("-")

                if (len(parts)) != 3:
                    raise ValueError
                
                port, metric, router_id = map(int, parts)

                if router_id < MIN_ROUTER_ID or router_id > MAX_ROUTER_ID:
                    raise ValueError
                
                if port < MIN_PORT or port > MAX_PORT:
                    raise ValueError
                
                if metric < 0:
                    raise ValueError

                outputs.append(Output(port, metric, router_id))
            return outputs
        except ValueError:
            raise ValueError("ERROR: Invalid outputs")

    def validate_ports(self):
        input_set = set(self.input_ports)
        output_set = set()

        for output in self.output_ports:
            if output.output_port in input_set:
                raise ValueError()

            if output.output_port in output_set:
                raise ValueError()

            output_set.add(output.output_port)


