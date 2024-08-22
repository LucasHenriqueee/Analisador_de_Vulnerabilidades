import json
import uuid
import os

# Caminho do arquivo .gns3
gns3_file_path = "/home/lucasventura/GNS3/projects/Cenario_GNS3/Cenario_GNS3.gns3"

# Ler o arquivo .gns3
with open(gns3_file_path, "r") as file:
    gns3_data = json.load(file)

# Solicitar ao usuário o número de PCs desejados (mámixo 8)
num_pcs = int(input("Quantos PCs você deseja adicionar (máximo 8)? "))
if num_pcs < 1 or num_pcs > 8:
    print("Número inválido, Deve ser entre 1 e 8.")
    exit(1)

# IDs e contadores
switch_id = str(uuid.uuid4())
switch_port = 0
pc_port = 5002

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

# Criar novo switch com a mesma configuração do Switch1
new_switch = {
    "compute_id": "local",
    "console": 5002,
    "console_auto_start": False,
    "console_type": "none",
    "custom_adapters": [],
    "first_port_name": None,
    "height": 32,
    "label": {
        "rotation": 0,
        "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        "text": "Switch2",
        "x": -37,
        "y": -31
    },
    "locked": False,
    "name": "Switch2",
    "node_id": switch_id,
    "node_type": "ethernet_switch",
    "port_name_format": "Ethernet{0}",
    "port_segment_size": 0,
    "properties": {
        "ports_mapping": [
            {"name": "Ethernet0", "port_number": 0, "type": "access", "vlan": 1},
            {"name": "Ethernet1", "port_number": 1, "type": "access", "vlan": 1},
            {"name": "Ethernet2", "port_number": 2, "type": "access", "vlan": 1},
            {"name": "Ethernet3", "port_number": 3, "type": "access", "vlan": 1},
            {"name": "Ethernet4", "port_number": 4, "type": "access", "vlan": 1},
            {"name": "Ethernet5", "port_number": 5, "type": "access", "vlan": 1},
            {"name": "Ethernet6", "port_number": 6, "type": "access", "vlan": 1},
            {"name": "Ethernet7", "port_number": 7, "type": "access", "vlan": 1}
        ]
    },
    "symbol": ":/symbols/ethernet_switch.svg",
    "template_id": "1966b864-93e7-32d5-965f-001384eec461",
    "width": 72,
    "x": 100,
    "y": 100,
    "z": 1
}

# Adicionar switch à topologia
gns3_data["topology"]["nodes"].append(new_switch)

# Adicionar PCs e links à topologia
for i in range(1, num_pcs + 1):
    pc, pc_id = create_pc(i)
    link = create_link(pc_id, switch_id, i - 1)
    gns3_data["topology"]["nodes"].append(pc)
    gns3_data["topology"]["links"].append(link)

    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{pc_id}"
    os.makedirs(new_pc_dir, exist_ok=True)

    # Criar arquivo de configuração do novo PC
    startup_vpc_content = f"""
    # This the configuration for PC{i}
    #
    # Uncomment the following line to enable DHCP
    # dhcp
    # or the line below to manually setup an IP address and subnet mask
    # ip 192.168.1.{i} 255.0.0.0
    #

    set pcname PC{i}
    """
    startup_vpc_path = os.path.join(new_pc_dir, "startup.vpc")
    with open(startup_vpc_path, "w") as file:
        file.write(startup_vpc_content)

# Salvar as mudanças de volta no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"{num_pcs} PCs adicionados com sucesso ao Switch2 com ID {switch_id}")

"""
# Gerar novos IDs
new_pc_id = str(uuid.uuid4())
new_switch_id = str(uuid.uuid4())
new_link_id_pc_switch = str(uuid.uuid4())
new_link_id_switch_switch = str(uuid.uuid4())

# Adicionar novo PC
new_pc = {
    "compute_id": "local",
    "console": 5010,
    "console_auto_start": False,
    "console_type": "telnet",
    "custom_adapters": [],
    "first_port_name": None,
    "height": 59,
    "label": {
        "rotation": 0,
        "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        "text": "PC2",
        "x": 14,
        "y": -25
    },
    "locked": False,
    "name": "PC2",
    "node_id": new_pc_id,
    "node_type": "vpcs",
    "port_name_format": "Ethernet{0}",
    "port_segment_size": 0,
    "properties": {},
    "symbol": ":/symbols/vpcs_guest.svg",
    "template_id": "19021f99-e36f-394d-b4a1-8aaa902ab9cc",
    "width": 65,
    "x": 100,
    "y": 150,
    "z": 1
}

# Adicionar novo switch com a mesma configuração do Switch1
new_switch = {
    "compute_id": "local",
    "console": 5002,
    "console_auto_start": False,
    "console_type": "none",
    "custom_adapters": [],
    "first_port_name": None,
    "height": 32,
    "label": {
        "rotation": 0,
        "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        "text": "Switch2",
        "x": -37,
        "y": -31
    },
    "locked": False,
    "name": "Switch2",
    "node_id": new_switch_id,
    "node_type": "ethernet_switch",
    "port_name_format": "Ethernet{0}",
    "port_segment_size": 0,
    "properties": {
        "ports_mapping": [
            {"name": "Ethernet0", "port_number": 0, "type": "access", "vlan": 1},
            {"name": "Ethernet1", "port_number": 1, "type": "access", "vlan": 1},
            {"name": "Ethernet2", "port_number": 2, "type": "access", "vlan": 1},
            {"name": "Ethernet3", "port_number": 3, "type": "access", "vlan": 1},
            {"name": "Ethernet4", "port_number": 4, "type": "access", "vlan": 1},
            {"name": "Ethernet5", "port_number": 5, "type": "access", "vlan": 1},
            {"name": "Ethernet6", "port_number": 6, "type": "access", "vlan": 1},
            {"name": "Ethernet7", "port_number": 7, "type": "access", "vlan": 1}
        ]
    },
    "symbol": ":/symbols/ethernet_switch.svg",
    "template_id": "1966b864-93e7-32d5-965f-001384eec461",
    "width": 72,
    "x": 100,
    "y": 100,
    "z": 1
}

# Adicionar novo link entre PC2 e o novo switch
new_link_pc_switch = {
    "filters": {},
    "link_id": new_link_id_pc_switch,
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
            "node_id": new_pc_id,
            "port_number": 0
        },
        {
            "adapter_number": 0,
            "label": {
                "rotation": 0,
                "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                "text": "eth0",
                "x": 25,
                "y": 15
            },
            "node_id": new_switch_id,
            "port_number": 0
        }
    ],
    "suspend": False
}

# Adicionar novo link entre o novo switch e o Switch1
new_link_switch_switch = {
    "filters": {},
    "link_id": new_link_id_switch_switch,
    "link_style": {},
    "nodes": [
        {
            "adapter_number": 1,
            "label": {
                "rotation": 0,
                "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                "text": "eth1",
                "x": 25,
                "y": 15
            },
            "node_id": new_switch_id,
            "port_number": 1
        },
        {
            "adapter_number": 4,
            "label": {
                "rotation": 0,
                "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                "text": "e4",
                "x": 25,
                "y": 15
            },
            "node_id": "584975d2-6f16-4999-b11d-ffb97675bbe6",  # ID do Switch1 existente
            "port_number": 4
        }
    ],
    "suspend": False
}

# Adicionar novo PC e switch à topologia
gns3_data["topology"]["nodes"].append(new_pc)
gns3_data["topology"]["nodes"].append(new_switch)
gns3_data["topology"]["links"].append(new_link_pc_switch)
gns3_data["topology"]["links"].append(new_link_switch_switch)

# Salvar as mudanças de volta no arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

# Criar diretório para o novo PC2
new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{new_pc_id}"
os.makedirs(new_pc_dir, exist_ok=True)

# Criar arquivo de configuração do novo PC2
startup_vpc_content = f
# This the configuration for PC2
#
# Uncomment the following line to enable DHCP
# dhcp
# or the line below to manually setup an IP address and subnet mask
# ip 192.168.1.1 255.0.0.0
#

set pcname PC2


startup_vpc_path = os.path.join(new_pc_dir, "startup.vpc")
with open(startup_vpc_path, "w") as file:
    file.write(startup_vpc_content)

print(f"Novo PC2 adicionado com sucesso com ID {new_pc_id}")
print(f"Novo Switch2 adicionado com sucesso com ID {new_switch_id}")
"""