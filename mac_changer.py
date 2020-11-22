#!usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
	parser = optparse.OptionParser()
	# dest= is how to get to the argument provided by user
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC")
	parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
	(options, arguments) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify the Interface, use --help for more info")
	elif not options.new_mac:
		parser.error("[-] Please specify the MAC, use --help for more info")
	return options


def change_mac(interface, new_mac):
	print("[+] Changing the MAC Address for " + interface + " to " + new_mac)

	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not find MAC Address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC is: " + str(current_mac))
change_mac(options.interface, options.new_mac)


current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("[+] The MAC was successfully changed to " + str(current_mac))
else:
	print("[-] There was a problem changing MAC")
