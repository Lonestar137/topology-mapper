from Mass_push import Site
from decouple import config
import getpass
import time
import threading
import re
import pygraphviz as pgv
import rich


def get_netbox_sites():
    pass

#Gather config options for connecting to devices, graph plotting, and ip ranges for polling.
USER=config('USR')
PASSWORD=config('PASS')
SECRET=config('SECRET')

G = pgv.AGraph()
G.node_attr['style'] = 'filled'

command = config('COMMAND', default='sh cdp neighbor detail')
file_name=config('OUTPUT_FILENAME', cast=str)


network_ip = config('NETWORK_IP', cast=str) # First 2 or 3 octets
try:
    device_ip = config('DEVICE_IPs', cast=lambda v: [int(s.strip()) for s in v.split(' ')])
except ValueError:
    device_ip = config('DEVICE_IPs', cast=lambda v: [float(s.strip()) for s in v.split(' ')])

#connect to devices
device = Site(USER, PASSWORD, SECRET)
output = device.Mass_push(device_ip, command, network_ip)


splt = output.split('\n')

temp = []
for i in splt:
    if i.find('current: ') != -1:
        temp.append(i)
    elif i.find('Device ID') != -1:
        temp.append(i)
    elif i.find('IP address: ') != -1:
        temp.append(i)
    elif i.find('Total cdp entries') != -1:
        temp.append(i)
    elif i.find('------') != -1:
        temp.append(i)



splt=temp

ips_host = ''
ip = ''
for i in splt:

    if i.find('current: ') != -1:
        curr_host = i.split(' ')[1]+'\n'
        print('current host', curr_host)

    if i.find('IP address: ') != -1:
        #Concatenate IPs until no more ips in cdp neighbor for host
        if ip.find(i.split(': ')[1]) == -1:
            #If not in ip, then add it.
            ip += i.split(': ')[1]+'\n'
        continue
    elif ip != '':
        #Add current node, make it blue only switches are logged into
        G.add_node(curr_host)
        h = G.get_node(curr_host)
        h.attr['fillcolor'] = '#3890E9'
        #No more IPs for the neighbor, then generate the node
        if bool(re.search('10\.[0-9][0-9]+\.2\.', ip)):
            #AP ip found
            G.add_node(ip)

            #set node colors
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#C11C1C'
        elif bool(re.search('10\.[0-9][0-9]+\.1\.1$', ip)):
            #router ip found
            G.add_node(ip)

            #Set colors for the nodes
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#5DA713'
        elif bool(re.search('10\.[0-9][0-9]+\.1\.', ip)):
            #Switch ip found
            G.add_node(ip)

            #set colors
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#3890E9'

        print(ip)
        try:
            #G.add_node(ip)
            G.add_edge(curr_host, ip)
        except:
            pass
    ip=''


G.layout(prog="dot")
G.draw(file_name)
#print(G)



#thread1 = threading.Thread(target=device.Mass_push, args=([48], 'sh run | i hostname', '10.251.11'))
#thread1.start()

