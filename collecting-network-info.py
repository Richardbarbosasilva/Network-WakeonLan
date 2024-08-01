import threading
import queue
import subprocess
from collections import OrderedDict
import ipaddress
import wakeonlan

# L2 ICMP protocol used to make requests (ping) through a range of ips 

def check_ping_response(response):

  fail = "Host de destino"

  # Check for both failure messages separately

  return not (fail in response) # Check for DOWN status

# Make the ICMP request ip per ip sending 32 bytes package

def ping_host(ip_address, result_queue):

    response = subprocess.Popen(f"ping -l 32 {ip_address}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate("")[0].decode("latin-1")

    result_queue.put((ip_address, check_ping_response(response)))

# Loops through the range of ips

def scan_network(cidr_ip):

    #Scans all IPs in the given CIDR range /24 using threads

    ip_list = [f"{cidr_ip}.{i}" for i in range(1, 254)]  # Generate IP addresses

    result_queue = queue.Queue()

    threads = []

    # Create and start threads to speed up the process

    for ip in ip_list:

        thread = threading.Thread(target=ping_host, args=(ip, result_queue))

        threads.append(thread)

        thread.start()

    # Wait for all threads to finish

    for thread in threads:

        thread.join()

    # Process results from the queue and gets status UP or DOWN
    
    results = OrderedDict()

    while not result_queue.empty():

        ip, is_up = result_queue.get()

        results[ip] = "UP" if is_up else "DOWN"    

    return results

# Function to sort in

def generate_ip_list(cidr_ip):
  
  #Generates a list of IP addresses in ascending order (1 to 254) within the CIDR range

  base_ip = ipaddress.ip_interface(cidr_ip).network
  return [str(base_ip + i) for i in range(1, 255)]

if __name__ == "__main__":

    cidr_ip = "172.27.50"  # Replace with your CIDR IP
    results = scan_network(cidr_ip)

# Write on the output the ping results

    for ip, status in results.items():

        print(f"{status} | {ip} Ping done with success! Host is {status.upper()}!")


# Wake on lan feature

# Replace with the MAC address of the target PC (format: XX:XX:XX:XX:XX:XX)
# Send the magic packet

#wakeonlan.send_magic_packet('A4:BB:6D:82:4C:38')

#print(f"Wake-on-LAN magic packet sent to ip")
