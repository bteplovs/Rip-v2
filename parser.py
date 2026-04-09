from dataclasses import dataclass


#TODO: Check router IDs for uniqueness here!


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

                if line.startswith("router-id"):
                    self.router_id = self.validate_router_id(line)
                elif line.startswith("input-ports"):
                    self.input_ports = self.validate_input_ports(line)
                elif line.startswith("outputs"):
                    self.output_ports = self.validate_outputs(line, self.input_ports)
                else:
                    raise Exception("ERROR: Misformed config file")

    def validate_router_id(self, line):
        try:
            _, router_id = line.split()
            if len(line.split()) != 2:
                raise ValueError
            router_id = int(router_id)
            if router_id < 0 or router_id > 64000:
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
                if port < 1024 or port > 64000:
                    raise ValueError
            return ports
        except ValueError:
            raise ValueError("ERROR: Invalid input ports")

    def validate_outputs(self, line, input_ports):
        try:
            _, outputs = line.split(" ", 1)
            outputs_list = []
            for output in outputs.split(','):
                parts = output.strip().split("-")
                if (len(parts)) != 3:
                    raise ValueError
                
                input_port_of_peer, metric, router_id = map(int, parts)
                if router_id < 0 or router_id > 64000:
                    raise ValueError
                if metric < 0:
                    raise ValueError
                if input_port_of_peer < 1024 or input_port_of_peer > 64000:
                    raise ValueError
                if len(input_ports) > 0 and input_port_of_peer in input_ports:
                    raise ValueError

                outputs_list.append(Output(input_port_of_peer, metric, router_id))
            return outputs_list
        except ValueError:
            raise ValueError("ERROR: Invalid outputs")

