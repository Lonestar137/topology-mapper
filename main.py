from Mass_push import Site
from decouple import config
import getpass
import time
import threading
import re
import pygraphviz as pgv
from rich.console import Console


def get_netbox_sites():
    pass

def singlemode(USER, PASSWORD, SECRET, cmd):
    network_ip = config('NETWORK_IP', cast=str) # First 2 or 3 octets
    device_ip = config('DEVICE_IPs', cast=lambda v: [s.strip() for s in v.split(' ')])

    console = Console()
    console.print('Generate topology map? (y/n)', style='bold green')
    if input() == 'y':
        console.print('Generating...', style='bold yellow')
        #Connect to devices
        device = Site(USER, PASSWORD, SECRET)
        device_output = device.Mass_push(device_ip, cmd, network_ip)
        return device_output

    else:
        console.print('Aborting...', style='bold red') 
        return ''
        exit()




def multimode(USER, PASSWORD, SECRET, cmd):
    device_output=''
    device = Site(USER, PASSWORD, SECRET)

    network_ip = config('NETWORK_IP')
    device_ip = config('DEVICE_IPs', cast=lambda v: [s.strip() for s in v.split(' ')])

    console = Console()
    console.print('Generate topology map? (y/n)', style='bold green')
    if input() == 'y':
        console.print('Generating...', style='bold yellow')
        device = Site(USER, PASSWORD, SECRET)
        device.pool(device_ip, cmd, network_ip)

        # Wait for all threads to finish before proceeding.
        while device.future.done() == False:
            time.sleep(1)
        time.sleep(2)

        # loop through device outputs and append to string.
        for i in device.output_array:
            device_output += str(i)
        print(device_output)
    else:
        console.print('Aborting...', style='bold red') 
        exit()
    return device_output


#Gather config options for connecting to devices, graph plotting, and ip ranges for polling.
USER=config('USR')
PASSWORD=config('PASS')
SECRET=config('SECRET')

G = pgv.AGraph()
G.node_attr['style'] = 'filled'

command = config('COMMAND', default='sh cdp neighbor detail')
file_name=config('OUTPUT_FILENAME', cast=str)


if config('MODE') == 'multimode': 
    output=multimode(USER, PASSWORD, SECRET, command)
elif config('MODE') == 'singlemode':
    output=singlemode(USER, PASSWORD, SECRET, command)
else:
    print('Please set the env variable MODE equal to multimode or singlemode.')


splt = output.split('\n')


#Filter out unwanted lines.
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

#Create nodes, assign color
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
        elif bool(re.search('10\.[0-9][0-9]+\.1\.1$', ip)) or ip.find('10.251.1.36') != -1 or ip.find('10.251.1.35') != -1:
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


#Graph layout type.  Default uses dot
G.layout(prog="dot")

#Draw to .png file.
G.draw(file_name)
#print(G)



#thread1 = threading.Thread(target=device.Mass_push, args=([48], 'sh run | i hostname', '10.251.11'))
#thread1.start()

