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


USER=config('USR')
PASSWORD=config('PASS')
SECRET=config('SECRET')

#^[A-Za-z0-9\.-]+
G = pgv.AGraph()
G.node_attr['style'] = 'filled'


#connect to devices
device = Site(USER, PASSWORD, SECRET)
devices = [2,4,5]
output = device.Mass_push(devices, 'sh cdp neighbor detail', '10.52.1')
file_name='Fayette-Topology.png'


#Prepare output
#print(output)
#print('\n\n\n\n')
splt = output.split('\n')

ips_host = ''
ip = ''
for i in splt:
    #first_word_found=bool(re.search('^[A-Za-z0-9\.-]+',i))
    #other_words_found=bool(re.search(' [A-Za-z0-9\.-]+',i))
    if i.find('current: ') != -1:
        curr_host = i.split(' ')[1]+'\n'
        print('current host', curr_host)

    if i.find('IP address: ') != -1:
        #Concatenate IPs until no more ips in cdp neighbor for host
        ip += i.split(': ')[1]+'\n'
        continue
    elif ip != '':
        #Add current node, make it blue only switches are logged into
        G.add_node(curr_host)
        h = G.get_node(curr_host)
        h.attr['fillcolor'] = '#3890E9'
        #No more IPs for the neighbor, then generate the node
        if bool(re.search('10\.[0-9]+\.2\.', ip)):
            #AP ip found
            G.add_node(ip)

            #set node colors
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#C11C1C'
        elif bool(re.search('10\.[0-9]+\.1\.1$', ip)):
            #router ip found
            G.add_node(ip)

            #Set colors for the nodes
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#5DA713'
        elif bool(re.search('10\.[0-9]+\.1\.', ip)):
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


#from netmiko import ConnectHandler
#import pygraphviz as pgv
#
#def console_output()
#    #Prints the graph in console.
#    G = pgv.AGraph()
#    G.add_node("a")
#    G.add_edge("b", "c")
#    print(G)
#
#def connect()
#
#ips = ['10.100.1.1', '10.100.1.2', '10.100.1.3', '10.100.1.4']
#G = pgv.AGraph()
#G.add_node("a")
#G.add_edge("b", "c")

