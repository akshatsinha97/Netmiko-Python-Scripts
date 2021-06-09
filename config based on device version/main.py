from version_config import Config

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

        version_list = ['vios_l2-ADVENTERPRISEK9-M', 'VIOS-ADVENTERPRISEK9-M']

        # instantiating class alongwith the required params
        obj = Config(device)

        # checking for successful login into device
        if hasattr(obj, 'net_connect'):

            # using specific method from the class based on the user input with required params
            obj.match(version_list)