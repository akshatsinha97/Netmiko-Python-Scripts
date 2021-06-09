from eigrp import Eigrp

# input by user for the required action
command = input("Do you want to 'configure', 'delete' or 'view' eigrp? ")

# input based on a specific selection
if command == "delete":
    as_number = input('Enter the as number: ')

# viewing options
elif command == "view":
    view_choice = input(
        '''WHAT YOU WANT TO VIEW?

    type '1' to Display the neighbor table in brief 
    type '2' to Display the neighbor table in detail 
    type '3' to Display information about all EIGRP interfaces
    type '4' to Display information about a particular EIGRP interface 
    type '5' to Display information about EIGRP interfaces running a specific AS process  
    type '6' to Displays the topology table
    type '7' to Displays the number and type of packets sent and received 
    type '8' to Display EIGRP route from routing table
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
        obj = Eigrp(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params
            if command == "configure":
                obj.create_eigrp()

            elif command == "delete":
                obj.delete_eigrp(as_number)

            elif command == "view":
                if host_name == device['host']:
                    obj.view(view_choice)



