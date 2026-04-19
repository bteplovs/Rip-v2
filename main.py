"""
    main.py
"""

import parser
import router

import sys
import os

def get_config_path(config_file):
    """Retrieves a locally stored config file.

    Args:
        config_file: Name of the config file

    Returns:
        The full file path of the config file
    """
    path = os.path.join("config-files", config_file)
    
    if not os.path.isfile(path):
        print(f"ERROR: Failed to find config file: {config_file}.")
        sys.exit(1)
    
    return path

def main():
    """
    The main entry point to the application.
    """
    if len(sys.argv) != 2:
        print("ERROR: One command-line argument required: config-file.")
        sys.exit(1)
    
    _, config_file = sys.argv

    file_path = get_config_path(config_file)

    try:
        config = parser.Parser()
        config.read_config(file_path)
        RIP_router = router.Router(config.router_id, config.input_ports, config.neighbours, config.timers)
        RIP_router.run()
        print(f"RIP router {parsed_router.router_id} started.")
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()