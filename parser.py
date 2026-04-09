import sys
import os
from output import *

#router-id 1
#input-ports 6110, 6201, 7345
#outputs 5000-1-1, 5002-5-4

def read_config(argv):
    if len(argv) < 2:
        print("ERROR: One command-line argument required: config-file", file=sys.stderr)
        sys.exit(1)
    
    _, config_file = argv

    file_path = get_config_path(config_file)

    if (not config_file_exists(file_path)):
        print("ERROR: invalid file format", file=sys.stderr)
        sys.exit(1)
    
    router_id = None
    input_ports = None
    outputs = None

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("router-id"):
                router_id = validate_router_id(line)
            elif line.startswith("input-ports"):
                input_ports = validate_input_ports(line)
            elif line.startswith("outputs"):
                outputs = validate_outputs(line, input_ports)
            else:
                raise Exception("ERROR: Misformed config file")
    
    return router_id, input_ports, outputs # TODO: Potentitally return a ROuting table object

def config_file_exists(file_path):
    return os.path.isfile(file_path)

def validate_router_id(line): #TODO:  Each router must have its own unique router-id
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

def validate_input_ports(line): 
    try:
        _, ports = line.split(" ", 1)
        ports = [int(port.strip()) for port in ports.split(",")]
        if len(set(ports)) != len(ports): # Each port number occurs at most once 
            raise ValueError
        for port in ports:
            if port < 1024 or port > 64000:
                raise ValueError
        return ports
    except ValueError:
        raise ValueError("ERROR: Invalid input ports")

def validate_outputs(line, input_ports):
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
            if input_port_of_peer < 1024 or input_port_of_peer > 64000:
                raise ValueError
            if input_ports is not None and input_port_of_peer in input_ports:
                raise ValueError

            outputs_list.append(Output(input_port_of_peer, metric, router_id))
        return outputs_list
    except ValueError:
        raise ValueError("ERROR: Invalid outputs")

def get_config_path(config_file):
    return os.path.join("config-files", config_file)

