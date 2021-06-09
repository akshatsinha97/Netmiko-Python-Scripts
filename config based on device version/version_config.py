from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

class Config:

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

    def match(self, version_list):

        # matching the version in vrsion list with device version for sending the specified configuation
        for soft_ver in version_list:

            print("checking for " + soft_ver)
            version = self.net_connect.send_command("Show version")
            int_version = version.find(soft_ver)

            if int_version > 0:
                print("Match found " + soft_ver)
                break

            else:
                print("Match not found " + soft_ver) 

        if soft_ver == 'vios_l2-ADVENTERPRISEK9-M':
            
            # opening switch configuration file and passing the commands
            print("Running " + soft_ver + "commands")
            with open('switch_config_file.txt') as f:
                switch_config = f.read().splitlines()
                self.net_connect.send_config_set(switch_config)
                self.net_connect.save_config()
                print("Successfully added configuration!")
                print('------------------------------------------')

        elif soft_ver == 'VIOS-ADVENTERPRISEK9-M':

            # opening router configuration file and passing the commands
            print("Running " + soft_ver + "commands")
            with open('router_config_file.txt') as f:
                router_config = f.read().splitlines()
                self.net_connect.send_config_set(router_config)
                self.net_connect.save_config()
                print("Successfully added configuration!")
                print('------------------------------------------')
