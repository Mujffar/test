from flask import Flask
import subprocess
import os
import json
import psutil
import socket

app = Flask(__name__)

@app.route('/')
def get_machine_id():
    with open('/etc/machine-id', 'r') as f:
        return {'machine_id': f.read().strip()}

machine_id_json = json.dumps(get_machine_id())


    #Get Machine ID



#Get Information of Ram


# Get total RAM in bytes
total_ram = psutil.virtual_memory().total

# Convert bytes to GB
gb_ram = total_ram / (1024 * 1024 * 1024)

# Create a dictionary with RAM information
ram_info = {
    "Total_RAM": round(gb_ram, 2)
}

# Convert dictionary to JSON
ram_json = json.dumps(ram_info)





#Default Route

def check_default_route():
    output = subprocess.check_output(["ip", "route", "show"]).decode("utf-8")
    for line in output.splitlines():
        if "default via" in line:
            return line.split()[2]

default_route = check_default_route()

# Create a dictionary with default route information
default_route_info = {
    "default_route": default_route if default_route else "No default route found."
}

# Convert dictionary to JSON
default_route_json = json.dumps(default_route_info)



# Default Route Matric

def get_default_route_metric():
    output = subprocess.check_output(['ip', 'route', 'show'])
    for line in output.decode('utf-8').split('\n'):
        if 'default' in line:
            fields = line.split()
            for i in range(len(fields)):
                if fields[i] == 'metric':
                    return int(fields[i+1])

default_metric = get_default_route_metric()

# Create a dictionary with default route metric information
default_metric_info = {
    "default_route_metric": default_metric if default_metric else "No default route found."
}

# Convert dictionary to JSON
default_metric_json = json.dumps(default_metric_info)







#Get kernel IO Module information


# Check if the /proc/modules file exists
if not os.path.exists('/proc/modules'):
    print('Error: /proc/modules file not found')
else:
    # Open the /proc/modules file and read its contents
    with open('/proc/modules', 'r') as f:
        modules = f.readlines()

    # Loop through the modules and check if any I/O modules are loaded
    io_modules = ['ata_piix', 'ahci', 'nvme', 'nvme-core', 'nvme-ns']
    io_loaded = []
    for module in modules:
        name = module.split()[0]
        if name in io_modules:
            io_loaded.append(name)
    
    # Create a dictionary with the loaded I/O modules information
    io_modules_info = {
        "io_modules_loaded": io_loaded if io_loaded else "No I/O modules are loaded."
    }

    # Convert dictionary to JSON
    kernel_io_module_json = json.dumps(io_modules_info)



# Get Interfaces

def get_interfaces():
    cmd = "ifconfig -a"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

    interfaces = {}

    current_interface = None
    for line in output.splitlines():
        if line.startswith(' '):
            # We are in the middle of a block of information about the current interface
            if current_interface:
                parts = line.strip().split()
                if parts:
                    key = parts[0].strip(':')
                    value = ' '.join(parts[1:])
                    interfaces[current_interface][key] = value
        else:
            # This is a new interface block
            parts = line.strip().split()
            if parts:
                current_interface = parts[0].strip(':')
                interfaces[current_interface] = {}

    # Convert dictionary to JSON
    interface_json = json.dumps(interfaces)


if __name__ == "__main__":
    get_interfaces()
	
	
	
#Get Network Card
def get_network_cards():
    # Run the "lspci" command to get the PCI devices information
    output = os.popen('lspci -nn').read()

    # Parse the output to get the network devices
    network_devices = []
    for line in output.splitlines():
        if 'Network controller' in line or 'Ethernet controller' in line:
            network_devices.append(line.strip())

    # Create a dictionary to store the network devices information
    devices_dict = {}
    for device in network_devices:
        # Extract the device ID and vendor ID from the line
        device_id = device.split()[0]
        vendor_id = device.split()[2]

        # Add the device information to the dictionary
        devices_dict[device_id] = {
            'vendor_id': vendor_id,
            'device_type': 'Network controller' if 'Network controller' in device else 'Ethernet controller'
        }

    # Convert dictionary to JSON
    network_card_json = json.dumps(devices_dict)


if __name__ == '__main__':
    get_network_cards()
	
	
	
	
	
# Has SSE SUPPORT

def has_sse42_support():
    if os.cpu_count() == 1:
        # If there is only one logical processor, assume SSE 4.2 is supported
        return True
    try:
        import cpuid
    except ImportError:
        # If cpuid module is not available, assume SSE 4.2 is not supported
        return False
    features = cpuid.CPUID().get_feature_info()
    return features.sse4_2

sse42_info = {"has_sse42_support": has_sse42_support()}
sse42_json = json.dumps(sse42_info)
	
	
	
	
	
#Has two Logical CPUID
def has_two_logical_cpus():
    if os.cpu_count() >= 2:
        return True
    return False

# Create a dictionary with the CPU information
cpu_info = {
    "has_two_logical_cpus": has_two_logical_cpus()
}

# Convert dictionary to JSON
cpu_json = json.dumps(cpu_info)

	
	
	
	
# Check Wifi Connectivity

def check_wifi_connectivity():
    # Try to connect to a well-known hostname or IP address on the Internet
    try:
        socket.create_connection(("8.8.8.8", 53))
        return {"wifi_connectivity": True}
    except OSError:
        return {"wifi_connectivity": False}

if __name__ == '__main__':
    wifi_json = json.dumps(check_wifi_connectivity())
	
# Add all JSON data to a dictionary
data = {
    "machine_id": json.loads(machine_id_json),
    "ram_info": json.loads(ram_json),
    "default_route": json.loads(default_route_json),
    "default_metric": json.loads(default_metric_json),
    "kernel_io_module": json.loads(kernel_io_module_json),
    "network_card": json.loads(network_card_json),
    "sse42_json": json.loads(sse42_json),
    "cpu_json": json.loads(cpu_json),
    "wifi_json": json.loads(wifi_json)
}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
