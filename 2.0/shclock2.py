# Example Python script using Netmiko to connect to different lists of Cisco devices and return sh clock output
from __future__ import print_function
import time
import netmiko

# Prompt user to search either Denver or Dallas
choice = input('Enter your choice 1-Denver or 2-Dallas [1-2] : ')
choice = int(choice)

# Define hosts list based on location

denver1 = {'hostname': 'denverswitch1',
           'ip': '192.168.1.1'}
denver2 = {'hostname': 'denverswitch2',
           'ip': '192.168.1.2'}

denver = [denver1, denver2]

dallas1 = {'hostname': 'dallasswitch1',
           'ip': '192.168.2.1'}
dallas2 = {'hostname': 'dallasswitch2',
           'ip': '192.168.2.2'}

dallas = [dallas1, dallas2]

# Define which device list to use based on user selection

if choice == 1:
    devices = denver
elif choice == 2:
    devices = dallas

# Define file to log all output to
logmyscript = open("datetime-audit" + time.strftime('%b%d%Y') + ".txt", "w")

# Document the start time of the script process
print("*****" + time.strftime("%I:%M%p %Z on %b %d, %Y") + "*****\n")
logmyscript.write("*****" + time.strftime("%I:%M%p %Z on %b %d, %Y") + " *****\n")

# SSH to device

for device in devices:
    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                          netmiko.ssh_exception.NetMikoAuthenticationException)

    try:
        print('~'*79)
        logmyscript.write("~"*79 + "\n")
        print('Connecting to ', device['hostname'])
        logmyscript.write("Connecting to device" + " at IP Address: " + device['hostname'] + "\n")
        ssh_connection = netmiko.ConnectHandler(device_type="cisco_nxos", ip=device['ip'], username="Admin",
                                                password="CiscoCisco", global_delay_factor=2)
        ssh_connection.enable()
        result = ssh_connection.find_prompt() + "\n"
        shclock = ssh_connection.send_command("sh clock")
        print(shclock)
        logmyscript.write(shclock)
        updateclock = ssh_connection.send_command("clock set " + time.strftime("%I:%M:%S %d %B %Y"))
        print(updateclock)
        logmyscript.write(updateclock)

        # Disconnect from the device
        ssh_connection.disconnect()
    except netmiko_exceptions as e:
        print ('Failed to ', device, e)
        logmyscript.write("Failed to " + device)

print('~'*79)
print("Finished DATE TIME AUDIT")
print('~'*79)
logmyscript.write("~"*79 + "\n")
logmyscript.write("Finished DATE TIME AUDIT" + "\n")
logmyscript.write("~"*79 + "\n")
print(" ")
logmyscript.write(" " + "\n")
