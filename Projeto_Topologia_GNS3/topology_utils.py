"""
    Script responsavel criação de PCs, switches, e links
"""
import uuid
import os
from config_utils import write_interfaces_file

def create_oraculo_container():
    """
    Cria um contêiner especial 'oraculo-1' para a topologia.
    """
    node_id = str(uuid.uuid4())
    container_id = node_id.replace("-", "")
    return {
        "compute_id": "local",
        "console": 5005,
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 59,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": "oraculo-1",
            "x": -5,
            "y": -25
        },
        "locked": False,
        "name": "oraculo-1",
        "node_id": node_id, # UUID completo para o node_id
        "node_type": "docker",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "adapters": 1,
            "aux": 5006,
            "console_http_path": "/",
            "console_http_port": 80,
            "console_resolution": "1024x768",
            "container_id": container_id, # Hexadecimal para o container_id
            "image": "oraculo:latest",
            "start_command": None,
            "usage": ""
        },
        "symbol": ":/symbols/docker_guest.svg",
        "template_id": "7f6da3e9-0dba-423b-82e4-18014b5f2922",
        "width": 65,
        "x": -206,
        "y": -106,
        "z": 1
    }, node_id

def create_pc_container(pc_number, switch_x, switch_y, pc_network, pc_port):
    """
    Cria um contêiner Docker representando um PC.
    """
    node_id = str(uuid.uuid4())
    container_id = node_id.replace("-", "")
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/docker/{node_id}/etc/network"
    os.makedirs(new_pc_dir, exist_ok=True)

    # Criar diretório e configurar rede
    write_interfaces_file(node_id, pc_network['ip'], pc_network['subnet'], pc_network['gateway'])

    return {
        "compute_id": "local",
        "console": pc_port + pc_number,
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 59,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": f"ubuntu-ssh-user-{pc_number}",
            "x": -38,
            "y": -25
        },
        "locked": False,
        "name": f"ubuntu-ssh-user-{pc_number}",
        "node_id": node_id,
        "node_type": "docker",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "adapters": 1,
            "aux": pc_port + 1 + pc_number,
            "console_http_path": "/",
            "console_http_port": 80,
            "console_resolution": "1024x768",
            "container_id": container_id,
            "image": "ubuntu-ssh-user:latest",
            "start_command": None,
            "usage": ""
        },
        "symbol": ":/symbols/docker_guest.svg",
        "template_id": "5f343939-8f35-4f8c-93c4-7676e6419a77",
        "width": 65,
        "x": switch_x + 50 + pc_number * 50,
        "y": switch_y + 100,
        "z": 1
    }, node_id


def create_switch(switch_number):
    """
    Cria um switch e suas propriedades.
    """
    switch_id = str(uuid.uuid4())
    switch_x = -400 + (switch_number * 200)
    switch_y = 100
    return {
        "compute_id": "local",
        "console": 5002 + switch_number,
        "console_auto_start": False,
        "console_type": "none",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 32,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": f"Switch{switch_number}",
            "x": 2,
            "y": -25
        },
        "locked": False,
        "name": f"Switch{switch_number}",
        "node_id": switch_id,
        "node_type": "ethernet_switch",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "ports_mapping": [
                {"name": f"Ethernet{i}", "port_number": i, "type": "access", "vlan": 1} for i in range(8)
            ]
        },
        "symbol": ":/symbols/ethernet_switch.svg",
        "template_id": "1966b864-93e7-32d5-965f-001384eec461",
        "width": 72,
        "x": switch_x,
        "y": switch_y,
        "z": 1
    }, switch_id, switch_x, switch_y

def create_link(node1_id, node1_port, node2_id, node2_port):
    """
    Cria um link entre dois nós.
    """
    link_id = str(uuid.uuid4())
    print(f"Criando link: {node1_id} (porta {node1_port}) <-> {node2_id} (porta {node2_port})")
    return {
        "filters": {},
        "link_id": link_id,
        "link_style": {},
        "nodes": [
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"e{node1_port}",
                    "x": 25,
                    "y": 15
                },
                "node_id": node1_id,
                "port_number": node1_port
            },
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"e{node2_port}",
                    "x": 25,
                    "y": 15
                },
                "node_id": node2_id,
                "port_number": node2_port
            }
        ],
        "suspend": False
    }
