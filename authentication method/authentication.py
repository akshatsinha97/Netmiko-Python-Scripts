from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

class Authentication:

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

    def add(self):

        # adding radius server as authentication
        print(f"Connecting to device {self.device['host']}")
        with open('config.txt') as auth:
            self.net_connect.send_config_set(auth.read().splitlines())
        self.net_connect.save_config()
        print('Configuration successfull!')
        print("--------------------------------------------")

    def remove(self):

        # removing radius server as authentication
        print(f"Connecting to device {self.device['host']}")
        self.net_connect.send_config_set('no aaa new-model')
        self.net_connect.save_config()
        print('Deletion successfull!')
        print("--------------------------------------------")

    def view(self):
        
        # viewing authentication on a per device basis mentioned by user
        print(self.net_connect.send_command('show run | include authentication'))