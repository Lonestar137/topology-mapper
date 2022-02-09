from netmiko import ConnectHandler
#from dotenv import load_dotenv
#from dotenv import dotenv_values
import getpass
import time
from rich.console import Console


class Site:
    
    def __init__(self, username, password, secret):
        #Initialize connection
        self.username = username
        self.password = password
        self.secret = secret
        self.ip=''
        self.console = Console()

    def Connect(self):
        #Connect to a device.
        if self.ip == '':
            self.ip = input('Enter an IP to connect: ')

        self.Device = {
                "ip": self.ip,
                "username": self.username,
                "password": self.password,
                "secret": self.secret,
                "device_type": "cisco_ios"
                }
        return ConnectHandler(**self.Device)
        

    def Enter_cli(self, ip=None):
        if ip != None:
            self.ip == ip

        if self.ip == '':
            self.ip = input('Enter an ip to connect:')
        
        ssh = self.Connect()
        ssh.enable()
        while True:
            self.cmd = input(ssh.find_prompt())
            if self.cmd == 'exit':
                ssh.disconnect()
                print('Session ended')
                break
            elif self.cmd == '':
                pass
            elif self.cmd.find('sh') != -1 and ssh.check_enable_mode() == True:
                print('send_cmd')
                print(ssh.send_command(self.cmd))
            else:
                print('write_channel')
                ssh.write_channel(self.cmd)

    def Mass_push(self, devices: list, cmds: str, network_ip=None):
        #List of device IP's is passed
        self.devices = devices
        self.cmds = cmds
        counter=0
        if network_ip == None:
            network_ip = input('Enter the network IP for the site: ')

        #Detect if no devices were passed.
        if self.devices == []:
            ask = input('No device IPs were specified.  Provision devices by range?')
            if ask[0:1] == 'y' or ask[0:1] == 'Y':
                # if yes do this
                self.ask_range = input('From ip: ')
                while type(self.ask_range) != int:
                    try:
                        self.ask_range=int(self.ask_range)
                    except:
                        print('Must be an integer.  Example: 2 to start at [NetworkIP].2')
                        self.ask_range = input('From ip: ')

                self.ask_range_end = input('End ip: ')
                while type(self.ask_range_end) != int:
                    try:
                        self.ask_range_end = int(self.ask_range_end)
                    except:
                        print('Must be an integer.  Example: 10 to end on the [NetworkIP].10')
                        self.ask_range_end = input('End ip: ')
                
                counter = self.ask_range
                while counter <= self.ask_range_end:
                    self.devices.append(counter)
                    counter+=1

                for i in self.devices:
                    print(network_ip + '.' +str(i) + '\n')
                ask = input('The above devices will be provisioned.  Continue? (y/n)')
                if ask[0:1] == 'y' or ask[0:1] == 'Y':
                    pass
                elif ask[0:1] == 'n' or ask[0:1] == 'N':
                    print('Option No selected.  Exiting session.')
                    exit()
                else:
                    counter = 0
                    while counter <= 5:
                        print('Response must be yes or no. (y/n, Y/N)')
                        ask = input('Continue to provision the above devices? (Y/N)')
                        counter+=1
                        if counter == 5:
                            print('Maximum number of tries exceeded.  Exiting session. . .')
                            exit()

                        if ask[0:1] == 'Y' or ask[0:1] == 'y':
                            break
                        elif ask[0:1] == 'n' or ask[0:1] == 'N':
                            print('Option No selected.  Exiting session.')
                            exit()
                        else:
                            pass

            else:
                #When option no is selected.
                print('Option No selected.  Exiting session.')
                exit()

        total_output=''
        #Actually pushes the CMDs.
        for i in self.devices:
            self.ip = network_ip+'.'+str(i)
            self.console.print('Connecting to ' + self.ip, style='green')
            try:
                ssh = self.Connect()
            except:
                #If fail to connect, then skip
                self.console.print(self.ip+' failed to connect.', style='red')
                continue

            ssh.enable()
            if self.cmds.find('sh') != -1 and ssh.check_enable_mode() == True:
                #TODO: Split the line with the sh command to prevent errors, i.e. enter conf mode before the show command it won't show.
                self.response=str(ssh.send_command(self.cmds))
                print(self.response)#Necessary for unit test
                total_output+='\ncurrent: '+self.ip+'\n'+self.response
            else: 
                ssh.write_channel(self.cmds)


            ssh.disconnect()
        return total_output
        

