from loopbacks import Loopback

# input by user for the required action 
command = input("Do you want to 'create', 'delete' or 'view' loopbacks? ")

# input based on a specific selection
if command == 'create' or command == 'delete':
    no_of_loopbacks = int(input("number of loopbacks: ")) 
elif command == 'view':
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
        obj  = Loopback(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params
            if command == 'create':
                obj.create_loopback(no_of_loopbacks)
            
            elif command == 'delete':
                obj.delete_loopback(no_of_loopbacks)

            elif command == 'view':
                if host_name == device['host']:
                    obj.show_loopback()