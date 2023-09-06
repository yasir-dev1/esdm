# SDM  SSH-Device-Manger
A tool for managing SSH devices.

## Usage

Options:

* -r, --remote Specify the name of the remote SSH device
* -a, --add Add a new SSH device
* -l, --list List all saved SSH devices
* -d, --delete Delete a saved SSH device


## Examples

List all saved SSH devices

    Main.py -l
Add a new SSH device

    Main.py -a
    Enter the device name: my_device
    Enter the IP address: ip
    Enter the username: usernam
    Enter the password: password

Connect to a remote device

    Main.py -r my_device

How it works

SDM uses a JSON file to store the SSH devices. The file is located in the home directory of the user who runs the tool. The file is named ~/.SDM/ssh_devices.json.

The JSON file is a dictionary where the keys are the device names and the values are the device information. The device information includes the IP address, username, and password.

When the user runs the SDM tool, it first checks if the JSON file exists. If it does not exist, the tool creates a new empty file.

The tool then parses the command-line arguments. If the user specifies the -r option, the tool connects to the remote device. To do this, the tool uses the device information from the JSON file.

If the user specifies the -a option, the tool adds a new SSH device to the JSON file. The tool prompts the user for the device name, IP address, username, and password.

If the user specifies the -l option, the tool lists all of the saved SSH devices.

If the user specifies the -d option, the tool deletes a saved SSH device from the JSON file.
License

SDM is licensed under the MIT License.
