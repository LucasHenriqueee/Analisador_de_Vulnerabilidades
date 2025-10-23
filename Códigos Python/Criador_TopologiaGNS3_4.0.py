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

#Definir sempre 4 switches fixos
NUM_SWITCHES = 4
pc_port = 5010  # Porta inicial para PCs

# Definir posições fixas para os switches
switch_positions = [
    (40, -163),     # Switch1
    (323, -163),    # Switch2
    (41, 65),       # Switch3
    (325, 65)       # Switch4
]

# Executar o segundo script e capturar a saída
process = subprocess.Popen(['python3', 'checar_SCL_2.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Verificar se o script externo executou com sucesso
if process.returncode != 0:
    print(f"Erro ao executar 'checar_SCL_2.py':\n{error.decode().strip()}")
    exit(1)

# Parsear a saída para capturar as informações de rede
network_info = [] # Lista de dicionários
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

num_pcs = len(network_info)
print(f"Tamanho da lista de redes capturadas: {num_pcs}")

# Validar se há informações de rede suficientes para todos os PCs
if len(network_info) < num_pcs:
    print(f"Erro: O script externo retornou informações de rede insuficientes. "
        f"Esperado: {num_pcs}, Recebido: {len(network_info)}.")
    exit(1)

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
            "text": f"ubuntu-ied-{pc_number}",
            "x": -38,
            "y": -25
        },
        "locked": False,
        "name": f"ubuntu-ied-{pc_number}",
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
            "image": "ubuntu-ied:latest",  # Imagem Docker   >>>>>>>>>!!!! MUDAR AQUI TODA VEZ QUE ATUALIZAR A IMAGEM DOCKER !!!!!<<<<<<<<<<<<<<<<<
            "start_command": None,
            "usage": ""
        },
        "symbol": ":/symbols/docker_guest.svg",
        "template_id": "5f343939-8f35-4f8c-93c4-7676e6419a77",  # ID do template fornecido
        "width": 65,
        "x": switch_x - 100 + pc_number * 50,  # Posicionamento horizontal ajustado
        "y": switch_y - 200,  # Posicionamento vertical ajustado
        "z": 1
    }
    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/docker/{node_id}/etc/network"
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
	up echo nameserver 192.168.1.1 > /etc/resolv.conf

# DHCP config for eth0
#auto eth0
#iface eth0 inet dhcp
#	hostname ubuntu-ied-{pc_number}
"""
    interface_path = os.path.join(new_pc_dir, "interfaces")
    with open(interface_path, "w") as file:
        file.write(interface)
    print(f"Configuração de rede escrita para PC {pc_container['name']} com IP {pc_network['ip']}")

    return pc_container, node_id



# Função para criar um switch
def create_switch(switch_number, x, y):
    node_id = str(uuid.uuid4())
    container_id = node_id.replace("-", "")  # Simplesmente usando parte do UUID como container_id

    switch_config = {
        "compute_id": "local",
        "console": 5000 + switch_number,  # Porta console única para cada switch
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 48,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": f"OpenvSwitch-{switch_number}",
            "x": -33,
            "y": -25
        },
        "locked": False,
        "name": f"OpenvSwitch-{switch_number}",
        "node_id": node_id,
        "node_type": "docker",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "adapters": 16,  # Número de interfaces (pode ser ajustado conforme necessidade)
            "aux": 5000 + switch_number + 1,  # Porta auxiliar única
            "console_http_path": "/",
            "console_http_port": 80,
            "console_resolution": "1024x768",
            "container_id": container_id[:64],  # Limitando a 64 caracteres se necessário
            "environment": None,
            "extra_hosts": None,
            "extra_volumes": [],
            "image": "gns3/openvswitch:latest",
            "start_command": None,
            "usage": "By default all interfaces are connected to the br0"
        },
        "symbol": ":/symbols/classic/multilayer_switch.svg",
        "template_id": "34c4edc6-de68-4ea5-9b26-b597c4846874",  # Template ID para Open vSwitch
        "width": 51,
        "x": x,
        "y": y,
        "z": 1
    }
    
    return switch_config, node_id


# Função para criar um link entre dois nodes
def create_link(node1_id, node1_port, node2_id, node2_port):
    link_id = str(uuid.uuid4())
    return {
        "filters": {},
        "link_id": link_id,
        "link_style":{},
        "nodes": [
            {
                "adapter_number": node1_port,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"eth{node1_port}",
                    "x": 25,
                    "y": 15
                },
                "node_id": node1_id,
                "port_number": 0
            },
            {
                "adapter_number": node2_port,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"eth{node2_port}",
                    "x": 25,
                    "y": 15
                },
                "node_id": node2_id,
                "port_number": 0
            }
        ],
        "suspend": False
    }

# Adicionar switches à topologia
switch_ids = []
for i in range(NUM_SWITCHES):
    switch, switch_id = create_switch(i + 1, *switch_positions[i])
    gns3_data["topology"]["nodes"].append(switch)
    switch_ids.append(switch_id)


# Criar links entre os switches conforme a topologia desejada
gns3_data["topology"]["links"].extend([
    create_link(switch_ids[0], 0, switch_ids[1], 0),    # Switch1 <-> Switch2
    create_link(switch_ids[1], 1, switch_ids[3], 0),    # Switch2 <-> Switch4
    create_link(switch_ids[3], 1, switch_ids[2], 0),    # Switch4 <-> Switch3
    create_link(switch_ids[2], 1, switch_ids[0], 1),    # Switch3 <-> Switch1
    create_link(switch_ids[0], 2, switch_ids[3], 2),    # Switch1 <-> Switch4
    create_link(switch_ids[2], 2, switch_ids[1], 2)     # Switch3 <-> Switch2
])

# Distribuir PCs entre os 4 switches
pcs_per_switch = math.ceil(num_pcs / NUM_SWITCHES)
pc_counter = 0
for switch_id, (switch_x, switch_y) in zip(switch_ids, switch_positions):
    for i in range(pcs_per_switch):
        if pc_counter >= num_pcs:
            break
        pc, pc_id = create_pc_container(pc_counter + 1, switch_x, switch_y)
        gns3_data["topology"]["nodes"].append(pc)
        link = create_link(pc_id, 0, switch_id, i+3)
        gns3_data["topology"]["links"].append(link)
        pc_counter += 1

# Adicionar contêiner Docker e linká-lo ao Switch1 na porta e5
docker_container, docker_id = create_oraculo_container()
gns3_data["topology"]["nodes"].append(docker_container)
link = create_link(docker_id, 0, switch_ids[0], 5)  # Conecta Docker ao Switch1 na porta Ethernet5
gns3_data["topology"]["links"].append(link)

# Salvar mudanças no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"Topologia atualizada com {NUM_SWITCHES} switches e {num_pcs} PCs.")
