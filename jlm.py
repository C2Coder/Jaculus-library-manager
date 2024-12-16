# jlm.py

import argparse
import os
import json
import requests
import datetime
import shutil


def save_json(data: dict):
    with open("libs.json", "w") as f:
        json.dump(data, f, indent=2)


def load_json():
    with open("libs.json") as f:
        data = json.load(f)
    return data


def download_library(data: dict, lib_name: str) -> bool:
    # Get manifest from server TODO add response code checking
    req = requests.get(f'{data["server"]}/{lib_name}/manifest.json')
    lib_data = json.loads(req.text)

    # lib data = {'name': 'Colors', 'description': 'Library for handling colors', 'files': ['colors.ts'], 'examples': [{'name': 'Basic usage', 'file': 'examples/basic-usage.ts'}]}

    data["libs"][lib_name]["files"] = lib_data["files"]
    save_json(data)

    for file in lib_data["files"]:
        req = requests.get(f'{data["server"]}/{lib_name}/{file}')
        if req.status_code != 200:
            print("Failed to download " + file + "from " + data["server"])
            return False
        folder = "@types" if lib_name == "@types" else f'src/{data["folder"]}'
        with open(f"{folder}/{file}", "w") as f:
            f.write(req.text)
            print("Downloaded " + file)
    return True


def uninstall_library(lib_name: str):

    data = load_json()

    for file in data["libs"][lib_name]["files"]:
        os.remove(f"{data['folder']}/{file}")
        print("Deleted " + file)

    del data["libs"][lib_name]
    print("Deleted " + lib_name)

    save_json(data)


def install_library(lib_name: str = "", ignore_libs_json: bool = False):

    data = load_json()


    os.makedirs(f'src/{data["folder"]}', exist_ok=True)
    os.makedirs(f'@types', exist_ok=True)


    # Get manifest from server TODO add response code checking
    req = requests.get(data["server"]+"manifest.json")
    server_data = json.loads(req.text)

    manifest = {"libs": []}

    for lib in server_data:
        manifest["libs"].append(lib["folder"])

    # Check if lib exists on server
    if not lib_name in manifest["libs"]:
        print("Library " + lib_name + " not found on the server")
        return

    # Add lib to file
    if lib_name in data["libs"].keys() and not ignore_libs_json:
        print("Library " + lib_name + " already in libs.json file")
        return
    else:
        data["libs"][lib_name] = {
            "last-update": "",
            "server": "default"
        }

    # Download library
    if download_library(data, lib_name):
        # Update last-update time
        data["libs"][lib_name]["last-update"] = str(datetime.datetime.now())

    # Update libs.json
    save_json(data)


def cli():
    """Main command-line interface for Jaculus Library Manager (JLM)."""
    parser = argparse.ArgumentParser(
        description="Jaculus Library Manager (JLM)")

    # Define subcommands
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand to create a new library
    create_parser = subparsers.add_parser(
        'create', help="Create a new library")
    create_parser.add_argument(
        'library_name', help="Name of the library to create")

    # Subcommand to list all libraries
    list_parser = subparsers.add_parser('list', help="List all libraries")

    # Subcommand to install libraries
    install_parser = subparsers.add_parser(
        'install', help="Install a library (or all if no name is given)")
    install_parser.add_argument(
        'lib_name',
        nargs='?',  # Make this argument optional
        help="Name of the library to install"
    )
    install_parser.add_argument(
        '-i', '--ignore',
        action='store_true',  # Set to True if argument is given
        help="Ignore the libs.json file"
    )

    # Subcommand to install libraries
    uninstall_parser = subparsers.add_parser(
        'uninstall', help="Uninstall a library")
    uninstall_parser.add_argument(
        'lib_name',
        help="Name of the library to uninstall"
    )

    # Check if libs.json exists
    if not os.path.isfile("libs.json"):
        print("libs.json file not found, creating one")
        data = {}
        save_json(data)

    # Fill missing keys
    data = load_json()
    if not "libs" in data.keys():
        data["libs"] = {}
    if not "folder" in data.keys():
        data["folder"] = "libs"
    if not "server" in data.keys():
        data["server"] = "https://c2coder.github.io/Jaculus-libraries/data/"
    save_json(data)

    # Parse arguments
    args = parser.parse_args()

    # Handle the logic based on the subcommand
    if args.command == 'create':
        # Create the library
        cwd = os.getcwd()
        library_path = os.path.join(cwd, args.library_name)

        if not os.path.exists(library_path):
            os.makedirs(library_path)
            print(f"Library '{args.library_name}' created at {library_path}")
        else:
            print(f"Library '{args.library_name}' already exists.")

    elif args.command == 'list':
        # List all libraries
        cwd = os.getcwd()
        libraries = [d for d in os.listdir(
            cwd) if os.path.isdir(os.path.join(cwd, d))]
        print("Libraries in current directory:")
        for library in libraries:
            print(f"- {library}")

    elif args.command == 'install':
        # Install the library (or all if no name is provided)
        if args.lib_name:
            print(f"Installing library: {args.lib_name}")
            install_library(args.lib_name, args.ignore)

        else:
            print("Installing all libraries from libs.json")
            for lib in data["libs"]:
                install_library(lib, True)

    elif args.command == 'uninstall':
        # Uninstall the library
        print(f"Uninstalling library: {args.lib_name}")
        uninstall_library(args.lib_name)

    else:
        # If no valid command is provided, print help
        parser.print_help()


if __name__ == "__main__":
    cli()
