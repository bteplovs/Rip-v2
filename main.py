
import parser
import router

import sys
import os

def get_config_path(config_file):
        """Retrives a locally stored config file.

        Args: 
            config_file: Name of the config file

        Returns: 
            The full file path of the config file
        """
        return os.path.join("config-files", config_file)

def config_file_exists(file_path):
        """Checks that a file path exists.

        Args: 
            file_path: The path being checked.

        Returns: 
            True, if filepath exists, False otherwise
        """
        return os.path.isfile(file_path)

def main():
    """
    The main entry point to the application.
    """
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
        parsed_router = parser.Parser()
        parsed_router.read_config(file_path)
    except Exception as e:
        print("ERROR:", e)

    try:
        print(f"RIP router {parsed_router.router_id} started")
        RIP_router = router.Router(parsed_router.router_id, parsed_router.input_ports, parsed_router.neighbours)
        RIP_router.run()
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    main()