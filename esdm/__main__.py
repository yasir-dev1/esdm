#!/usr/bin/python3
from getpass import getpass
import argparse
import subprocess
import json
import os
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

def run():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="A tool for managing SSH devices")
    parser.add_argument("-r", "--remote", help="Specify the name of the remote SSH device")
    parser.add_argument("-a", "--add", help="Add a new SSH device", action="store_true")
    parser.add_argument("-l", "--list", help="List all saved SSH devices", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete a saved SSH device")
    parser.add_argument("-s", "--sftp", help="Open SFTP protocol")
    parser.add_argument("-e","--edit", help="Edit a saved SSH device")

    # Parse the arguments
    args = parser.parse_args()

    # Store SSH devices in a JSON file (in the home directory)
    ssh_devices_file = os.path.expanduser("~/.esdm/.ssh_devices.json")

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
        device_password = getpass("Enter the password: ")

        hashed_password = hash_password(device_password)

        ssh_devices[device_name] = {
            "ip": device_ip,
            "username": device_username,
            "password": hashed_password.decode()  # Save the hash as a string
        }

        # Save the devices to the file (in the home directory)
        os.makedirs(os.path.dirname(ssh_devices_file), exist_ok=True)
        with open(ssh_devices_file, "w") as file:
            json.dump(ssh_devices, file, indent=4)
        print(f"{device_name} has been successfully added.")

    # Edit a saved device
    elif args.edit:
        device_to_edit = args.edit
        if device_to_edit in ssh_devices:
            print(f"Editing device: {device_to_edit}")
            device_info = ssh_devices[device_to_edit]
            device_info["ip"] = input("Enter the new IP address (leave empty to keep existing): ") or device_info["ip"]
            device_info["username"] = input("Enter the new username (leave empty to keep existing): ") or device_info["username"]
            new_password = getpass("Enter the new password (leave empty to keep existing): ")
            if new_password:
                device_info["password"] = hash_password(new_password).decode()
            with open(ssh_devices_file, "w") as file:
                json.dump(ssh_devices, file, indent=4)
            print(f"{device_to_edit} has been updated.")
        else:
            print(f"{device_to_edit} is not a saved device.")

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
    elif args.sftp:
        device_name = args.sftp
        if device_name in ssh_devices:
            device_info = ssh_devices[device_name]
            ip = device_info["ip"]
            username = device_info["username"]
            password = getpass("Enter the password: ")

            if check_password(device_info["password"].encode(), password):
                # Create the SCP command
                scp_command = f"sshpass -p {password} sftp {username}@{ip}"

                try:
                    subprocess.run(scp_command, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"There was a problem : {e}")
            else:
                print("Incorrect password.")
        else:
            print(f"{device_name} is not a saved device.")

    # Connect to a remote device
    elif args.remote in ssh_devices:
        device_info = ssh_devices[args.remote]
        ip = device_info["ip"]
        username = device_info["username"]
        password = getpass("Enter the password: ")

        if check_password(device_info["password"].encode(), password):
            # Create the SSH connection
            ssh_command = f"sshpass -p {password} ssh {username}@{ip}"
            
            try:
                subprocess.run(ssh_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"SSH connection failed: {e}")
        else:
            print("Incorrect password.")
    else:
        print("You entered an undefined device name.")

if __name__ == "__main__":
    run()
