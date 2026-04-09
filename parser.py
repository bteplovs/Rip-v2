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


def config_file_exists(file_path):
    return os.path.isfile(file_path)

def validate_router_id():
    pass

def validate_input_ports():
    pass

def validate_outputs():
    pass

def get_config_path(config_file):
    return os.path.join("config-files", config_file)
