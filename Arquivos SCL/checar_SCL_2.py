#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xml.etree.ElementTree as ET

def parse_scl(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the namespace dictionary
    ns = {'scl': 'http://www.iec.ch/61850/2003/SCL'}
    
    # List to hold IED information
    ieds = []
    
    # Iterate through each SubNetwork in the Communication section
    for subnetwork in root.findall('scl:Communication/scl:SubNetwork', ns):
        subnetwork_name = subnetwork.get('name')
        
        # Iterate through each ConnectedAP in the SubNetwork
        for connected_ap in subnetwork.findall('scl:ConnectedAP', ns):
            ied_name = connected_ap.get('iedName')
            ap_name = connected_ap.get('apName')
            address = connected_ap.find('scl:Address', ns)
            
            if address is not None:
                ip = address.find('scl:P[@type="IP"]', ns)
                subnet = address.find('scl:P[@type="IP-SUBNET"]', ns)
                gateway = address.find('scl:P[@type="IP-GATEWAY"]', ns)
                
                # Append the IED information to the list
                ieds.append({
                    'subnetwork': subnetwork_name,
                    'ied_name': ied_name,
                    'ap_name': ap_name,
                    'ip': ip.text if ip is not None else None,
                    'subnet': subnet.text if subnet is not None else None,
                    'gateway': gateway.text if gateway is not None else None
                })
    
    return ieds

# Path to your SCL file
file_path = 'simpleIO_direct_control.cid'
ied_info = parse_scl(file_path)

# Print the extracted information
for ied in ied_info:
    print(f"Subnetwork: {ied['subnetwork']}")
    print(f"IED Name: {ied['ied_name']}")
    print(f"Access Point Name: {ied['ap_name']}")
    print(f"IP Address: {ied['ip']}")
    print(f"Subnet Mask: {ied['subnet']}")
    print(f"Gateway: {ied['gateway']}")
    print("-" * 40)
