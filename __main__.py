import sys
import os

import config

def main():

    if len(sys.argv) != 2:
        print("ERROR: One command-line argument required: config-file")
        sys.exit(1)
    
    config_file = sys.argv[1]

    file_path = get_config_path(config_file)

    if (not config_file_exists(file_path)):
            print("ERROR: invalid file format")
            sys.exit(1)
    
    try:
        print(f"Reading {config_file}...")
        parser = config.Config()
        parser.read_config_file(config_file)
        print(f"{config_file} successfully read")
    except:
        print("ERROR: Failed to read config file")
        sys.exit(1)

    try:
        print(f"initilising RIP router: {parser.router_id}...")
        router = router.Router(parser.router_id, parser.input_ports, parser.output_ports)
        router.run()
    except:
        print("ERROR: Failed to start RIP Router")
        sys.exit(1)

if __name__ == "__main__":
    main()


def get_config_path(config_file):
        return os.path.join("config-files", config_file)

def config_file_exists(file_path):
        return os.path.isfile(file_path)