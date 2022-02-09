from netmiko import ConnectHandler
import pygraphviz as pgv

def console_output()
    #Prints the graph in console.
    G = pgv.AGraph()
    G.add_node("a")
    G.add_edge("b", "c")
    print(G)

def connect()

ips = ['10.100.1.1', '10.100.1.2', '10.100.1.3', '10.100.1.4']
G = pgv.AGraph()
G.add_node("a")
G.add_edge("b", "c")



#Purpose:  
#Using a graph module, given an array i of n ip's, create a topology map of related nodes.
#TODO: pulls ip from Netbox database given a site id
#sts





