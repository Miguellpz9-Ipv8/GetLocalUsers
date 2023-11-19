import scapy.all as scapy
import socket
import ipaddress

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")
        local_ip = None
    finally:
        s.close()
    return local_ip

def get_ip_range(local_ip):
    try:
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        ip_range = str(network)
        return ip_range
    except ValueError as e:
        print(f"Error determining IP range: {e}")
        return None

def get_device_name(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return None

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    devices_list = []

    for device in answered_list:
        ip_address = device[1].psrc
        mac_address = device[1].hwsrc
        device_name = get_device_name(ip_address)

        device_dict = {"ip": ip_address, "mac": mac_address, "name": device_name}
        devices_list.append(device_dict)
    return devices_list

local_ip = get_local_ip()

if local_ip:
    ip_range = get_ip_range(local_ip)

    if ip_range:
        print(f"Scanning IP range: {ip_range}")
        devices = scan(ip_range)

        print("IP Address\t\tMAC Address\t\t\tDevice Name")
        print("-" * 69)
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}\t\t{device['name']}")
    else:
        print("Failed to determine the IP range.")
else:
    print("Failed to determine the local IP address.")
