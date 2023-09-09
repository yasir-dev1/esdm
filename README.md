# ESDM  Easy-SSH-Device-Manager
A tool for managing SSH devices.

## Download
    sudo apt install sshpass

    pip install esdm


## Usage

Options:

* -r, --remote Specify the name of the remote SSH device
* -a, --add Add a new SSH device
* -l, --list List all saved SSH devices
* -d, --delete Delete a saved SSH devicedd+
* -e, --edit Edit a saved SSH device
* -s, --sftp Open SFTP protocol


## Examples

List all saved SSH devices

    esdm -l
Add a new SSH device

    esdm -a
    Enter the device name: my_device
    Enter the IP address: ip
    Enter the username: usernam
    Enter the password: password

Connect to a remote device

    esdm -r my_device
Eddit a  SSH device

    esdm -e mydevice 
    Enter the new IP address (leave empty to keep existing):new ip
    Enter the new username (leave empty to keep existing): new user name
    Enter the new password (leave empty to keep existing): new password

Open Sftp Protocol
    esdm -s mydevice

How it works

esdm uses a JSON file to store the SSH devices. The file is located in the home directory of the user who runs the tool. The file is named ~/.SDM/ssh_devices.json.

The JSON file is a dictionary where the keys are the device names and the values are the device information. The device information includes the IP address, username, and password.

When the user runs the esdm tool, it first checks if the JSON file exists. If it does not exist, the tool creates a new empty file.

The tool then parses the command-line arguments. If the user specifies the -r option, the tool connects to the remote device. To do this, the tool uses the device information from the JSON file.

If the user specifies the -a option, the tool adds a new SSH device to the JSON file. The tool prompts the user for the device name, IP address, username, and password.

If the user specifies the -l option, the tool lists all of the saved SSH devices.

If the user specifies the -d option, the tool deletes a saved SSH device from the JSON file.
License

esdm is licensed under the MIT License.
