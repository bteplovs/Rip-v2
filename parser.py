import sys
import os

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
    input_ports = []
    outputs = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("router-id"):
                router_id = validate_router_id(line)
            elif line.startswith("input-ports"):
                input_ports = validate_input_ports(line)
            elif line.startswith("outputs"):
                outputs = validate_outputs(line)
            else:
                raise Exception("ERROR: Misformed config file")
    
    return router_id, input_ports, outputs

def config_file_exists(file_path):
    return os.path.isfile(file_path)

def validate_router_id(line): #TODO: check duplicate routers
    try:
        _, router_id = line.split()
        if len(line.split()) != 2:
            raise ValueError
        router_id = int(router_id)
        if router_id < 0:
            raise ValueError
        return router_id
    except ValueError:
        raise ValueError("Invalid router-id")

def validate_input_ports(line):
    try:
        _, ports = line.split(" ", 1)
        ports = [int(port.strip()) for port in ports.split(",")]
        for port in ports:
            if port <= 0 or port > 65535:
                raise ValueError
        return ports
    except ValueError:
        raise ValueError("Invalid input ports")

def validate_outputs(line):
    pass

def get_config_path(config_file):
    return os.path.join("config-files", config_file)

