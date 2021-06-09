from authentication import Authentication

# input by user for the required action
command = input("Do you want to 'add', 'remove' or 'view' configuration?: ")

# input based on a specific selection
if command == 'view':
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
        obj = Authentication(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params
            if command == 'add':
                obj.add()

            elif command == 'remove':
                obj.remove()

            elif command == 'view':
                if host_name == device['host']:
                    obj.view()