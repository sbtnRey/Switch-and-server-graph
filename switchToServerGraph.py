import paramiko
from getpass import getpass
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import re

# Connect to switch through ssh
ip = input("Please enter your IP address: ")
username = input("Please enter your username: ")
password = getpass()

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)

remote_conn = remote_conn_pre.invoke_shell()

remote_conn.send("show ip arp\n")
time.sleep(.5)
output = remote_conn.recv(65535).decode('utf-8')

pattern = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
ips = [match[0] for match in re.findall(pattern, output)]
print (ips)

# Graph the networks
G=nx.Graph()

pos=nx.circular_layout(G)

# Change switch name 
G.add_node('Switch Name')
G.add_node(ips[0])

x = 0

while (x < len(ips)):
     G.add_node(ips[x])
     G.add_edge('Switch Name', ips[x])
     x += 1



nx.draw(G, node_size=2000, alpha=0.5, node_color="blue", with_labels=True)

plt.show()
