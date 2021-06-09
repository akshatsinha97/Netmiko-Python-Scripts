from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

class Vlan:

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

    def vlan_create(self, number_of_vlans):

        # creating number of vlans specified by user and saving the configuration
        print(f"Connecting to device {self.device['host']}")
        for vlan_number in range(2,number_of_vlans + 2):

            print(f'Creating vlan {vlan_number}')
            print('-----------------------------')
            create = ['vlan ' + str(vlan_number), 'name vlan ' + str(vlan_number)]
            self.net_connect.send_config_set(create)
        self.net_connect.save_config()

        print(f'{number_of_vlans} vlans created!\n')

    def vlan_delete(self, number_of_vlans):

        # deleting number of vlans specified by user and saving the configuration
        print(f"Connecting to device {self.device['host']}")
        for vlan_number in range(2,number_of_vlans + 2):
            print(f'Deleting vlan {vlan_number}')
            print('-----------------------------')
            delete = ['no vlan ' + str(vlan_number)]
            self.net_connect.send_config_set(delete)
        self.net_connect.save_config()

        print(f'{number_of_vlans} vlans deleted!\n')

    def view(self, view_choice):

        # viewing the vlan configuration on a specific device
        self.view_choice = view_choice
 
        if self.view_choice == "1":
            print(self.net_connect.send_command('show vlan'))

        elif self.view_choice == "2":
            print(self.net_connect.send_command('show vlan brief'))

        elif self.view_choice == "3":
            print(self.net_connect.send_command('show vlan id 1'))

        elif self.view_choice == "4":
            print(self.net_connect.send_command('show vlan summary'))