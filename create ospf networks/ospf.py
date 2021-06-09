from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

class Ospf:

    # logging into each device one by one
    def __init__(self, device):
        self.device = device

        # try and except block used for error management if login fails
        try:
            self.net_connect = ConnectHandler(**device)
        except (AuthenticationException):
            print("Authentication Failure!!! to " + str(device['host']))
            
        except (NetMikoTimeoutException):
            print("Timeout to " + str(device['host']))
            
        except (SSHException):
            print("Are you sure SSH is enabled on " + str(device['host']) + " ?")
            
        except (EOFError):
            print("End of File while accessing " + str(device['host']))
            
        except Exception as unknown_error:
            print("Unknown Error!!!" + str(unknown_error))

    def create_ospf(self):

        # passing ospf configuration based on configuration file 
        with open("ospf_config.txt", "r") as create:
            print(f"Connecting to device {self.device['host']}")          
            self.net_connect.send_config_set(create.read().splitlines())
        self.net_connect.save_config()
        print("Configuration successfull!")
        print("--------------------------------------------------")

    def delete_ospf(self, p_id):

        # deleting ospf configuration based on process id provided by user
        print(f"Connecting to device {self.device['host']}")
        self.net_connect.send_config_set(f'no router ospf {p_id}')
        self.net_connect.save_config()
        print("Deletion successfull!")
        print("--------------------------------------------------")

    def view(self, view_choice):
        
        # viewing the vlan configuration on a specific device
        if view_choice == '1':
            print(self.net_connect.send_command('show ip route ospf'))

        elif view_choice == '2':
            print(self.net_connect.send_command('show ip ospf'))

        elif view_choice == '3':
            print(self.net_connect.send_command('show ip ospf interface'))

        elif view_choice == '4':
            interface = input('Enter interface name: ')
            print(self.net_connect.send_command(f'show ip ospf interface {interface}'))

        elif view_choice == '5':
            print(self.net_connect.send_command('show ip ospf neighbor'))

        elif view_choice == '6':
            print(self.net_connect.send_command('show ip ospf neighbor detail'))

        elif view_choice == '7':
            print(self.net_connect.send_command('show ip ospf database'))
