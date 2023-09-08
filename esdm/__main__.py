#!/usr/bin/python3

import argparse
import subprocess
import json
import os

def run():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="A tool for managing SSH devices")
    parser.add_argument("-r", "--remote", help="Specify the name of the remote SSH device")
    parser.add_argument("-a", "--add", help="Add a new SSH device", action="store_true")
    parser.add_argument("-l", "--list", help="List all saved SSH devices", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete a saved SSH device")
    parser.add_argument("-cp", "--copy", help="Copy a file using SCP")

    # Parse the arguments
    args = parser.parse_args()

    # Store SSH devices in a JSON file (in the home directory)
    ssh_devices_file = os.path.expanduser("~/.SDM/ssh_devices.json")

    # Read the devices or create an empty dictionary
    try:
        with open(ssh_devices_file, "r") as file:
            ssh_devices = json.load(file)
    except FileNotFoundError:
        ssh_devices = {}

    # List all saved SSH devices
    if args.list:
        if ssh_devices:
            print("Saved SSH devices:")
            for device_name in ssh_devices:
                print(device_name)
        else:
            print("No SSH devices are saved.")

    # Add a new device
    elif args.add:
        device_name = input("Enter the device name: ")
        device_ip = input("Enter the IP address: ")
        device_username = input("Enter the username: ")
        device_password = input("Enter the password: ")

        ssh_devices[device_name] = {
            "ip": device_ip,
            "username": device_username,
            "password": device_password
        }

        # Save the devices to the file (in the home directory)
        os.makedirs(os.path.dirname(ssh_devices_file), exist_ok=True)
        with open(ssh_devices_file, "w") as file:
            json.dump(ssh_devices, file, indent=4)
        print(f"{device_name} has been successfully added.")

    # Delete a saved device
    elif args.delete:
        device_to_delete = args.delete
        if device_to_delete in ssh_devices:
            del ssh_devices[device_to_delete]
            with open(ssh_devices_file, "w") as file:
                json.dump(ssh_devices, file, indent=4)
            print(f"{device_to_delete} has been deleted.")
        else:
            print(f"{device_to_delete} is not a saved device.")

    # Copy a file using SCP
    elif args.copy:
        device_name = args.remote
        if device_name in ssh_devices:
            device_info = ssh_devices[device_name]
            ip = device_info["ip"]
            username = device_info["username"]
            password = device_info["password"]
            source_file = args.copy
            destination = input("Enter the destination directory: ")

            # Create the SCP command
            scp_command = f"sshpass -p {password} scp {source_file} {username}@{ip}:{destination}"

            try:
                subprocess.run(scp_command, shell=True, check=True)
                print(f"File {source_file} copied to {device_name}:{destination}")
            except subprocess.CalledProcessError as e:
                print(f"SCP operation failed: {e}")
        else:
            print(f"{device_name} is not a saved device.")

    # Connect to a remote device
    elif args.remote in ssh_devices:
        device_info = ssh_devices[args.remote]
        ip = device_info["ip"]
        username = device_info["username"]
        password = device_info["password"]

        # Create the SSH connection
        ssh_command = f"sshpass -p {password} ssh {username}@{ip}"
        
        try:
            subprocess.run(ssh_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"SSH connection failed: {e}")
    else:
        print("You entered an undefined device name.")

if __name__ == "__main__":
    run()
