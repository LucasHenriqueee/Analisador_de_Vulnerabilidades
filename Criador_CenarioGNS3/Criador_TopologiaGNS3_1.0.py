"""
Este script tem como objetivo tentar implementar um algoritimo que possa gerar uma topologia
de rede de computadores dentro do GNS3 de acordo com a preferência do usuário.

Lucas Henrique Ventura Oliveira

1. Distribuição dos PCs entre os switches:
    Determine quantos PCs serão conectados a cada switch. Se o número de PCs não for um múltiplo exato do número de switches, os PCs restantes podem ser distribuídos uniformemente entre os switches.

2. Conexão dos switches:
    Se houver mais de um switch, os switches devem ser conectados entre si. Isso pode ser feito em um esquema linear ou em outro padrão de topologia (como anel ou estrela), dependendo da necessidade.

3. Adicionando os PCs e os switches à topologia:
    Para cada switch, adicione o número correspondente de PCs.
    Conecte os PCs ao switch correspondente.
    Conecte os switches entre si.
"""
import json
import uuid
import os

# Caminho do arquivo .gns3
gns3_file_path = "/home/lucasventura/GNS3/projects/Cenario_GNS3/Cenario_GNS3.gns3"

# Ler o arquivo .gns3
with open(gns3_file_path, "r") as file:
    gns3_data = json.load(file)

# Solicitar ao usuário o número de switches e PCs desejados
num_switches = int(input("Quantos switches você deseja adicionar? "))
num_pcs = int(input("Quantos PCs você deseja adicionar no total? "))

# IDs e contadores
switch_ids = [str(uuid.uuid4()) for _ in range(num_switches)]
pc_port = 5010  # Alterando para evitar conflito com a porta do switch
switch_port_counter = [0] * num_switches  # Contador de portas para cada switch

# Função para criar um PC
def create_pc(pc_number, switch_index):
    pc_id = str(uuid.uuid4())
    switch_port = switch_port_counter[switch_index]
    switch_port_counter[switch_index] += 1
    
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
    
    link = create_link(pc_id, switch_ids[switch_index], switch_port)
    
    return pc, link, pc_id

# Função para criar um link entre um PC e um switch
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

# Função para criar um switch
def create_switch(switch_number):
    switch_id = switch_ids[switch_number]
    switch = {
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
            "text": f"Switch{switch_number+1}",
            "x": 2,
            "y": -25
        },
        "locked": False,
        "name": f"Switch{switch_number+1}",
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
        "x": 500 * (switch_number + 1),
        "y": 100,
        "z": 1
    }
    
    return switch

# Função para criar links entre switches
def create_switch_links():
    switch_links = []
    for i in range(num_switches - 1):
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
                        "text": f"e7",
                        "x": 25,
                        "y": 15
                    },
                    "node_id": switch_ids[i],
                    "port_number": 7
                },
                {
                    "adapter_number": 0,
                    "label": {
                        "rotation": 0,
                        "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                        "text": f"e0",
                        "x": 25,
                        "y": 15
                    },
                    "node_id": switch_ids[i+1],
                    "port_number": 6
                }
            ],
            "suspend": False
        }
        switch_links.append(link)
    return switch_links

# Adicionar switches à topologia
for i in range(num_switches):
    switch = create_switch(i)
    gns3_data["topology"]["nodes"].append(switch)

# Distribuir PCs entre os switches e adicionar à topologia
for i in range(num_pcs):
    switch_index = i % num_switches
    pc, link, pc_id = create_pc(i+1, switch_index)
    gns3_data["topology"]["nodes"].append(pc)
    gns3_data["topology"]["links"].append(link)
    
    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{pc_id}"
    os.makedirs(new_pc_dir, exist_ok=True)
    
    # Criar arquivo de configuração do novo PC
    startup_vpc_content = f"""# This the configuration for PC{i+1}
#
# Uncomment the following line to enable DHCP
# dhcp
# or the line below to manually setup an IP address and subnet mask
# ip 192.168.1.{i+1} 255.0.0.0
#

set pcname PC{i+1}
"""
    startup_vpc_path = os.path.join(new_pc_dir, "startup.vpc")
    with open(startup_vpc_path, "w") as file:
        file.write(startup_vpc_content)

# Adicionar links entre switches
switch_links = create_switch_links()
gns3_data["topology"]["links"].extend(switch_links)

# Salvar as mudanças de volta no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"Rede criada com {num_pcs} PCs e {num_switches} switches.")
