import json
import uuid
import os
import math

# Caminho do arquivo .gns3
gns3_file_path = "/home/lucasventura/GNS3/projects/Cenario_GNS3/Cenario_GNS3.gns3"

# Ler o arquivo .gns3
with open(gns3_file_path, "r") as file:
    gns3_data = json.load(file)

# Solicitar ao usuário o número de PCs e switches desejados
num_pcs = int(input("Quantos PCs você deseja adicionar? "))
num_switches = int(input("Quantos switches você deseja adicionar? "))

if num_pcs < 1:
    print("Número inválido de PCs. Deve ser pelo menos 1.")
    exit(1)

if num_switches < 1:
    print("Número inválido de switches. Deve ser pelo menos 1.")
    exit(1)

# IDs e contadores
pc_port = 5010  # Porta inicial para PCs

# Função para criar um PC
def create_pc(pc_number, switch_x, switch_y):
    pc_id = str(uuid.uuid4())
    pc = {
        "compute_id": "local",
        "console": pc_port + pc_number,
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
        "x": switch_x + 50 + pc_number * 50,
        "y": switch_y + 100,
        "z": 1
    }
    
    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{pc_id}"
    os.makedirs(new_pc_dir, exist_ok=True)
    
    # Criar arquivo de configuração do novo PC
    startup_vpc_content = f"""# This is the configuration for PC{pc_number}
#
# Uncomment the following line to enable DHCP
# dhcp
# or the line below to manually setup an IP address and subnet mask
# ip 192.168.1.{pc_number} 255.0.0.0
#

set pcname PC{pc_number}
"""
    startup_vpc_path = os.path.join(new_pc_dir, "startup.vpc")
    with open(startup_vpc_path, "w") as file:
        file.write(startup_vpc_content)
    
    return pc, pc_id

# Função para criar um switch
def create_switch(switch_number):
    switch_id = str(uuid.uuid4())
    switch_x = 500 + (switch_number * 200)
    switch_y = 100
    switch = {
        "compute_id": "local",
        "console": 5002 + switch_number,
        "console_auto_start": False,
        "console_type": "none",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 32,
        "label":{
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
        }
    return switch, switch_id, switch_x, switch_y

# Função para criar um link entre dois nodes
def create_link(node1_id, node1_port, node2_id, node2_port):
    link_id = str(uuid.uuid4())
    link = {
        "filters": {},
        "link_id": link_id,
        "link_style":{},
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
    return link

# Adicionar switches à topologia
switch_ids = []
for i in range(1, num_switches + 1):
    switch, switch_id, switch_x, switch_y = create_switch(i)
    gns3_data["topology"]["nodes"].append(switch)
    switch_ids.append((switch_id, switch_x, switch_y))

# Distribuir PCs entre switches
pcs_per_switch = math.ceil(num_pcs / num_switches)
pc_counter = 0

for switch_id, switch_x, switch_y in switch_ids:
    for i in range(pcs_per_switch):
        if pc_counter >= num_pcs:
            break
        pc, pc_id = create_pc(pc_counter + 1, switch_x, switch_y)
        gns3_data["topology"]["nodes"].append(pc)
        link = create_link(pc_id, 0, switch_id, i)
        gns3_data["topology"]["links"].append(link)
        pc_counter += 1

# Conectar os switches entre si (topologia linear)
for i in range(1, len(switch_ids)):
    link = create_link(switch_ids[i-1][0], 6, switch_ids[i][0], 7)
    gns3_data["topology"]["links"].append(link)

# Salvar as mudanças de volta no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"Adicionados {num_pcs} PCs e {num_switches} switches ao projeto.")
