import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

# input by user for the required action
user_command = input("Do you want to 'create','delete' or 'view' bgp? ")

# viewing options
if user_command == 'view':
    view_choice = input('''WHAT YOU WANT TO VIEW?

    type '1' to Display the contents of the BGP routing table
    type '2' to Display information about BGP and TCP connections to neighbors
    type '3' to to Display BGP summary including path, prefix and attribute information for all connections to BGP neighbors
    type '4' to Display BGP configuration applied
    ''')
    host = input('Enter hostname: ')

# opening file and extracting data of each device 
with open('data.yaml', 'r') as data:
    all_devices_conf = yaml.load(data, Loader=yaml.FullLoader)

configuration = all_devices_conf['all_devices']

# opening file and extracting login information of each device
with open('targets.yaml','r') as connect:
    targets = yaml.load(connect, Loader=yaml.FullLoader)

# instantiating environment class with the loader
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

def make_template():

    # combining the data and the jinja template together for passing the configuration 
    for device, config in targets['all_devices'].items():
        template = env.get_template('bgp.j2')
        rendered_template = template.render(configuration[device])
        commands = rendered_template.splitlines()

        # logging into each device one by one
        # try and except block used for error management if login fails
        try:
            net_connect = ConnectHandler(**config)

        except (AuthenticationException):
            print("Authentication Failure!!! to " + device)
            continue

        except (NetMikoTimeoutException):
            print("Timeout to " + device)
            continue
        
        except (SSHException):
            print("Are you sure SSH is enabled on " + device + " ?")
            continue

        except (EOFError):
            print("End of File while accessing " + device)
            continue

        except Exception as unknown_error:
            print("Unknown Error!!!" + str(unknown_error)) 
            continue

        send_template(net_connect, device, config, commands) 

def send_template(net_connect, device, config, commands):

    # using specific condition based on the user input to send generated template
    if user_command == 'create':

        # creating bgp configuration
        net_connect.send_config_set(commands)
        net_connect.save_config()
        print(f'Created bgp on {device}')
        print('--------------------------------')

    elif user_command == 'delete':

        # deleting bgp configuration based on as number 
        for device, data in configuration.items():
            net_connect.send_config_set(f"no router bgp {data['as_number']}")
            net_connect.save_config()
            print(f'deleted bgp from {device}')
            print('--------------------------------')

    elif user_command == 'view':

        # viewing the vlan configuration on a specific device
        if host == device:
            if view_choice == '1':
                print(net_connect.send_command('show ip bgp'))

            elif view_choice == '2':
                print(net_connect.send_command('show ip bgp neighbors'))
            
            elif view_choice == '3':
                print(net_connect.send_command('show ip bgp summary'))

            elif view_choice == '4':
                print(net_connect.send_command('show run | section bgp'))
    
make_template()