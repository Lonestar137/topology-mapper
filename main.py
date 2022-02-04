from Mass_push import Site
from decouple import config
import getpass
import time
import threading
import re
import pygraphviz as pgv



USER=config('USR')
PASSWORD=config('PASS')
SECRET=config('SECRET')

#^[A-Za-z0-9\.-]+
G = pgv.AGraph()
G.node_attr['style'] = 'filled'


device = Site(USER, PASSWORD, SECRET)
#devices = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12]
devices = [2, 3, 4, 5, 6, 7, 8, 10, 11]
output=device.Mass_push(devices, 'sh cdp neighbor detail', '10.40.1')

print(output)
print('\n\n\n\n')
splt = output.split('\n')

for i in splt:
    #first_word_found=bool(re.search('^[A-Za-z0-9\.-]+',i))
    #other_words_found=bool(re.search(' [A-Za-z0-9\.-]+',i))
    if i.find('current: ') != -1:
        curr_host = i.split(' ')[1]
        print('current host', curr_host)
#    if other_words_found == False: #Only want lines with just hostname
    if i.find('IP address: ') != -1:
        ip = i.split(': ')[1]
        if bool(re.search('10\.[0-9]+\.2\.', ip)):
            #AP ip found
            print('enterd')
            G.add_node(ip)
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#701d1c'
        elif bool(re.search('10\.[0-9]+\.1\.', ip)):
            #Switch ip found
            print('enterd')
            G.add_node(ip)
            n = G.get_node(ip)
            n.attr['fillcolor'] = '#2470a6'

        print(ip)
        try:
            #G.add_node(ip)
            G.add_edge(curr_host, ip)
        except:
            pass


G.layout(prog="dot")
G.draw('AlexanderCity.png')
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

