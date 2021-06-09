from vlans import Vlan

# input by user for the required action 
command = input("Do you want to 'create', 'delete' or 'view' vlans? ")

# input based on a specific selection
if command == 'create' or command == 'delete':
    number_of_vlans = int(input("Enter the no. of vlans: "))

# viewing options
elif command == 'view':
    view_choice = input('''WHAT YOU WANT TO VIEW?
                        
                        type '1' to Display vlan information
                        type '2' to Display vlan information in brief
                        type '3' to Display vlan by passing in the id
                        type '4' to Display vlan summary''')
    host_name = input('Enter hostname: ')

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
        obj = Vlan(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params 
            if command == 'create':
                obj.vlan_create(number_of_vlans)

            elif command == 'delete':
                obj.vlan_delete(number_of_vlans)
            
            elif command == 'view':
                if host_name == device['host']:
                    obj.view(view_choice)

            









