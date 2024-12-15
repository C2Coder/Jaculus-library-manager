# jlm.py

import argparse
import os

def create_library(library_name):
    """Simulate creating a new library."""
    cwd = os.getcwd()
    library_path = os.path.join(cwd, library_name)
    
    if not os.path.exists(library_path):
        os.makedirs(library_path)
        print(f"Library '{library_name}' created at {library_path}")
    else:
        print(f"Library '{library_name}' already exists.")

def list_libraries():
    """List all libraries in the current working directory."""
    cwd = os.getcwd()
    libraries = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]
    print("Libraries in current directory:")
    for library in libraries:
        print(f"- {library}")

def main():
    """Main function to parse arguments and call appropriate functions."""
    parser = argparse.ArgumentParser(description="Jaculus Library Manager (JLM)")
    subparsers = parser.add_subparsers(help="Commands")

    # Command: Create a new library
    create_parser = subparsers.add_parser('create', help="Create a new library")
    create_parser.add_argument('library_name', help="Name of the library to create")
    create_parser.set_defaults(func=lambda args: create_library(args.library_name))

    # Command: List all libraries
    list_parser = subparsers.add_parser('list', help="List all libraries")
    list_parser.set_defaults(func=lambda args: list_libraries())

    # Parse the arguments and execute the appropriate function
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
