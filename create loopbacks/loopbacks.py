from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

class Loopback:

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

    def create_loopback(self, no_of_loopbacks):

        # creating loopbacks based on number provided by user
        print(f"Connecting to device {self.device['host']}")
        for loopback in range(1, no_of_loopbacks + 1):
            print(f"Creating loopback {loopback}")
            print("-------------------------------")
            create = ['interface loopback ' + str(loopback), 
                    f'ip address {loopback}.{loopback}.{loopback}.{loopback} 255.255.255.255', 'no shutdown', 'exit']
            self.net_connect.send_config_set(create)
        self.net_connect.save_config()
            
        print(f'{no_of_loopbacks} loopbacks created!\n')

    def delete_loopback(self, no_of_loopbacks):

        # deleting loopbacks based on number provided by user
        print(f"Connecting to device {self.device['host']}")
        for loopback in range(1, no_of_loopbacks + 1):
            print(f"Deleting loopback {loopback}")
            print("-------------------------------")
            delete = [f'no interface loopback {loopback}']
            self.net_connect.send_config_set(delete)
        self.net_connect.save_config()

        print(f'{no_of_loopbacks} loopbacks deleted!\n')

    def show_loopback(self):

        # viewing loopbacks on a device specified by user
        print(self.net_connect.send_command('show ip int brief | begin Loopback'))