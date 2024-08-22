import json
import uuid
import os

# Caminho do arquivo .gns3
gns3_file_path = "/home/lucasventura/GNS3/projects/Cenario_GNS3/Cenario_GNS3.gns3"

# Ler o arquivo .gns3
with open(gns3_file_path, "r") as file:
    gns3_data = json.load(file)

# Solicitar ao usuário o número de PCs desejados (mámixo 7)
num_pcs = int(input("Quantos PCs você deseja adicionar (máximo 7)? "))
if num_pcs < 1 or num_pcs > 7:
    print("Número inválido, Deve ser entre 1 e 7.")
    exit(1)

# IDs e contadores
switch1_id = str(uuid.uuid4())
switch2_id = str(uuid.uuid4())
switch_port = 0
pc_port = 5010  # Evitar conflito com a porta do switch

# Função para criar um PC
def create_pc(pc_number):
    pc_id = str(uuid.uuid4())
    pc = {
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
            "text": f"PC{pc_number}",
            "x": 14,
            "y": -25
        },
        "locked": False,
        "name": f"PC{pc_number}",
        "node_id": pc_id,
        "node_type": "vpcs",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {},
        "symbol": ":/symbols/vpcs_guest.svg",
        "template_id": "19021f99-e36f-394d-b4a1-8aaa902ab9cc",
        "width": 65,
        "x": 100 + pc_number * 80,
        "y": 150,
        "z": 1
    }
    return pc, pc_id

# Função para criar um link entre PC e switch
def create_link(pc_id, switch_id, switch_port):
    link_id = str(uuid.uuid4())
    link = {
        "filters": {},
        "link_id": link_id,
        "link_style": {},
        "nodes": [
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": "e0",
                    "x": 25,
                    "y": 15
                },
                "node_id": pc_id,
                "port_number": 0
            },
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"e{switch_port}",
                    "x": 25,
                    "y": 15
                },
                "node_id": switch_id,
                "port_number": switch_port
            }
        ],
        "suspend": False
    }
    return link

# Função para criar e conectar dois switches
def create_and_connect_switches():
    switch1 = {
        "compute_id": "local",
        "console": 5002,
        "console_auto_start": False,
        "console_type": "none",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 32,
        "label":{
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": "Switch1",
            "x": 2,
            "y": -25
        },
        "locked": False,
        "name": "Switch1",
        "node_id": switch1_id,
        "node_type": "ethernet_switch",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "ports_mapping":[
                {"name": f"Ethernet{i}", "port_number": i, "type": "access", "vlan": 1} for i in range(8)
            ]
        },
        "symbol": ":/symbols/ethernet_switch.svg",
        "template_id": "1966b864-93e7-32d5-965f-001384eec461",
        "width": 72,
        "x": 500,
        "y": 100,
        "z": 1
    }

    switch2 = {
        "compute_id": "local",
        "console": 5003,
        "console_auto_start": False,
        "console_type": "none",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 32,
        "label":{
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": "Switch2",
            "x": 2,
            "y": -25
        },
        "locked": False,
        "name": "Switch2",
        "node_id": switch2_id,
        "node_type": "ethernet_switch",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "ports_mapping":[
                {"name": f"Ethernet{i}", "port_number": i, "type": "access", "vlan": 1} for i in range(8)
            ]
        },
        "symbol": ":/symbols/ethernet_switch.svg",
        "template_id": "1966b864-93e7-32d5-965f-001384eec461",
        "width": 72,
        "x": 700,
        "y": 100,
        "z": 1
    }

    # Criar link entre Switch1 e Switch2
    link_id = str(uuid.uuid4())
    link = {
        "filters": {},
        "link_id": link_id,
        "link_style": {},
        "nodes": [
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": "e7",
                    "x": 25,
                    "y": 15
                },
                "node_id": switch1_id,
                "port_number": 7
            },
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": "e7",
                    "x": 25,
                    "y": 15
                },
                "node_id": switch2_id,
                "port_number": 7
            }
        ],
        "suspend": False
    }

    return switch1, switch2, link

# Adicionar switches à topologia
switch1, switch2, switch_link = create_and_connect_switches()
gns3_data["topology"]["nodes"].append(switch1)
gns3_data["topology"]["nodes"].append(switch2)
gns3_data["topology"]["links"].append(switch_link)

# Adicionar PCs e links à topologia
for i in range(1, num_pcs + 1):
    pc, pc_id = create_pc(i)
    gns3_data["topology"]["nodes"].append(pc)
    link = create_link(pc_id, switch1_id, switch_port)
    gns3_data["topology"]["links"].append(link)
    switch_port += 1

    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{pc_id}"
    os.makedirs(new_pc_dir, exist_ok=True)

    # Criar arquivo de configuração do novo PC
    startup_vpc_content = f"""# This the configuration for PC{i}
#
# Uncomment the following line to enable DHCP
# dhcp
# or the line below to manually setup an IP address and subnet mask
# ip 192.168.1.{i} 255.255.255.0
#

set pcname PC{i}
"""
    startup_vpc_path = os.path.join(new_pc_dir, "startup.vpc")
    with open(startup_vpc_path, "w") as file:
        file.write(startup_vpc_content)

# Escrever as alterações de volta ao arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"Adicionado {num_pcs} PCs conectados ao Switch1.")
print("Switch1 está conectado ao Switch2.")
print(f"{num_pcs} PCs foram adicionados ao projeto GNS3 com sucesso!")
