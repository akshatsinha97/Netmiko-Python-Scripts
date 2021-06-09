from ospf import Ospf

# input by user for the required action 
command = input("Do you want to 'configure', 'delete' or 'view' ospf? ")

# input based on a specific selection
if command == 'delete':
    p_id = input('Enter process id: ')

# viewing options
elif command == 'view':
    view_choice = input('''WHAT YOU WANT TO VIEW?
    
    type '1' to Display all routers learned through OSPF from routing table
    type '2' to Display basic information about OSPF
    type '3' to Display information about all OSPF active interfaces
    type '4' to Display OSPF information about specific interface
    type '5' to Display OSPF neighbors with basic info
    type '6' to Display OSPF neighbors with detail info
    type '7' to Display data for OSPF database
                            ''')
    host_name = input('Enter host name: ')

# parsing out details from the devices file for logging
with open("devices.csv", "r") as devices:
    device_info = devices.read().splitlines()
    for device_item in device_info:
        split_data = device_item.split(",")
        
        device = { 
        'device_type': 'cisco_ios', 
        'host': split_data[0], 
        'username': split_data[1], 
        'password': split_data[2], 
        }

        # instantiating class alongwith the required params
        obj = Ospf(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params
            if command == 'configure':
                obj.create_ospf()

            elif command == 'delete':
                obj.delete_ospf(p_id)

            elif command == 'view':
                obj.view(view_choice)