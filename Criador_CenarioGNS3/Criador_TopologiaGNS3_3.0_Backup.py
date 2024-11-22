import json
import uuid
import os
import math
import subprocess
import sys

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

# Executar o segundo script e capturar a saída
process = subprocess.Popen(['python3', 'checar_SCL_2.py'], stdout=subprocess.PIPE)
output, _ = process.communicate()

# Parsear a saída para capturar as informações de rede
network_info = []
for line in output.decode().splitlines():
    if "IP Address" in line:
        ip = line.split(": ")[1]
    if "Subnet Mask" in line:
        subnet = line.split(": ")[1]
    if "Gateway" in line:
        gateway = line.split(": ")[1]
        network_info.append({
            "ip": ip,
            "subnet": subnet,
            "gateway": gateway
        })

# IDs e contadores
pc_port = 5010  # Porta inicial para PCs

# Função para criar um contêiner Docker
def create_oraculo_container():
    node_id = str(uuid.uuid4())  # UUID completo com hífens para o node_id
    container_id = node_id.replace("-", "")  # Apenas hexadecimal (sem hífens) para container_id
    docker_container = {
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
        "node_id": node_id,  # UUID completo para o node_id
        "node_type": "docker",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "adapters": 1,
            "aux": 5006,
            "console_http_path": "/",
            "console_http_port": 80,
            "console_resolution": "1024x768",
            "container_id": container_id,  # Hexadecimal para o container_id
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
    }
    return docker_container, node_id

# Função para criar um PC
def create_pc_container(pc_number, switch_x, switch_y):
    node_id = str(uuid.uuid4())  # UUID para node_id
    container_id = node_id.replace("-", "")  # Hexadecimal para container_id
    pc_network = network_info[pc_number - 1]  # Pegar as infos de rede para este PC
    pc_container = {
        "compute_id": "local",
        "console": pc_port + pc_number,  # Porta console baseada no número do PC
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
            "aux": pc_port + pc_number + 1,  # Porta auxiliar baseada no número do PC
            "console_http_path": "/",
            "console_http_port": 80,
            "console_resolution": "1024x768",
            "container_id": container_id,  # Identificador hexadecimal para o contêiner
            "environment": None,
            "extra_hosts": None,
            "extra_volumes": [],
            "image": "ubuntu-ssh-user:latest",  # Imagem Docker
            "start_command": None,
            "usage": ""
        },
        "symbol": ":/symbols/docker_guest.svg",
        "template_id": "5f343939-8f35-4f8c-93c4-7676e6419a77",  # ID do template fornecido
        "width": 65,
        "x": switch_x + 50 + pc_number * 50,  # Posicionamento horizontal ajustado
        "y": switch_y + 100,  # Posicionamento vertical ajustado
        "z": 1
    }
    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/docker/{container_id}/etc/network"
    os.makedirs(new_pc_dir, exist_ok=True)

    # Criar arquivo de configuração do novo PC
    interface = f"""#
# This is a sample network config, please uncomment lines to configure the network
#

# Uncomment this line to load custom interface files
# source /etc/network/interfaces.d/*

# Static config for eth0
auto eth0
iface eth0 inet static
	address {pc_network['ip']}
	netmask {pc_network['subnet']}
	gateway {pc_network['gateway']}
	up echo nameserver 192.168.0.1 > /etc/resolv.conf

# DHCP config for eth0
#auto eth0
#iface eth0 inet dhcp
#	hostname ubuntu-ssh-user-1
"""
    return pc_container, node_id

# Função para criar um switch
def create_switch(switch_number):
    switch_id = str(uuid.uuid4())
    switch_x = -400 + (switch_number * 200)
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
pcs_per_switch = math.ceil(num_pcs/num_switches)
pc_counter = 0

for switch_id, switch_x, switch_y in switch_ids:
    for i in range(pcs_per_switch):
        if pc_counter >= num_pcs:
            break
        pc, pc_id = create_pc_container(pc_counter + 1, switch_x, switch_y)
        gns3_data["topology"]["nodes"].append(pc)
        link = create_link(pc_id, 0, switch_id, i)
        gns3_data["topology"]["links"].append(link)
        pc_counter += 1

# Conectar os switches entre si (topologia linear)
for i in range(1, len(switch_ids)):
    link = create_link(switch_ids[i-1][0], 6, switch_ids[i][0], 7)
    gns3_data["topology"]["links"].append(link)

# Adicionar contêiner Docker e linká-lo ao Switch1 na porta e5
docker_container, docker_id = create_oraculo_container()
gns3_data["topology"]["nodes"].append(docker_container)
link = create_link(docker_id, 0, switch_ids[0][0], 5)  # Conecta Docker ao Switch1 na porta Ethernet5
gns3_data["topology"]["links"].append(link)

# Salvar as mudanças de volta no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"Adicionados {num_pcs} PCs e {num_switches} switches ao projeto.")
