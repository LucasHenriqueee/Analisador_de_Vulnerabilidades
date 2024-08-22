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
switch_id = str(uuid.uuid4())
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

# Função para criar o roteador MikroTik
def create_mikrotik():
    mikrotik_id = str(uuid.uuid4())
    mikrotik = {
        "compute_id": "local",
        "console": 5000,
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": "",
        "height": 45,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": "MikroTikCHR6.49",
            "x": -47,
            "y": -25
    },
    "locked": False,
        "name": "MikroTikCHR6.49",
        "node_id": mikrotik_id,
        "node_type": "qemu",
        "port_name_format": "ether{port1}",
        "port_segment_size": 0,
        "properties": {
            "adapter_type": "virtio-net-pci",
            "adapters": 8,
            "bios_image": "",
            "bios_image_md5sum": None,
            "boot_priority": "c",
            "cdrom_image": "",
            "cdrom_image_md5sum": None,
            "cpu_throttling": 0,
            "cpus": 1,
            "create_config_disk": False,
            "hda_disk_image": "chr-6.49.10.img",
            "hda_disk_image_md5sum": "49ae1ecfe310aea1df37b824aa13cf84",
            "hda_disk_interface": "virtio",
            "hdb_disk_image": "",
            "hdb_disk_image_md5sum": None,
            "hdb_disk_interface": "none",
            "hdc_disk_image": "",
            "hdc_disk_image_md5sum": None,
            "hdc_disk_interface": "none",
            "hdd_disk_image": "",
            "hdd_disk_image_md5sum": None,
            "hdd_disk_interface": "none",
            "initrd": "",
            "initrd_md5sum": None,
            "kernel_command_line": "",
            "kernel_image": "",
            "kernel_image_md5sum": None,
            "legacy_networking": False,
            "linked_clone": True,
            "mac_address": "0c:5d:ff:d0:00:00",
            "on_close": "power_off",
            "options": "-nographic",
            "platform": "x86_64",
            "process_priority": "normal",
            "qemu_path": "/bin/qemu-system-x86_64",
            "ram": 384,
            "replicate_network_connection_state": True,
            "tpm": False,
            "uefi": False,
            "usage": "If you'd like a different sized main disk, resize the image before booting the VM for the first time.\n\nOn first boot, RouterOS is actually being installed, formatting the whole main virtual disk, before finally rebooting. That whole process may take a minute or so.\n\nThe console will become available after the installation is complete. Most Telnet/SSH clients (certainly SuperPutty) will keep retrying to connect, thus letting you know when installation is done.\n\nFrom that point on, everything about RouterOS is also true about Cloud Hosted Router, including the default credentials: Username \"admin\" and an empty password.\n\nThe primary differences between RouterOS and CHR are in support for virtual devices (this appliance comes with them being selected), and in the different license model, for which you can read more about at http://wiki.mikrotik.com/wiki/Manual:CHR."
        },
        "symbol": ":/symbols/classic/router.svg",
        "template_id": "14dc5dbf-bb52-434a-b9a9-c90868c9b263",
        "width": 66,
        "x": 100,
        "y": -150,
        "z": 1
    }
    return mikrotik, mikrotik_id

# Função para criar um link entre roteador Mikrotik e o switch
def create_router_switch_link(mikrotik_id, switch_id):
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
                    "text": "ether8",
                    "x": 25,
                    "y": 15
                },
                "node_id": mikrotik_id,
                "port_number": 0
            },
            {
                "adapter_number": 0,
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": f"e7",
                    "x": 25,
                    "y": 15
                },
                "node_id": switch_id,
                "port_number": 7
            }
        ],
        "suspend": False
    }
    return link

# Adiciona o switch à topologia
switch = {
    "compute_id": "local",
    "console": None,
    "console_auto_start": False,
    "console_type": None,
    "custom_adapters": [],
    "first_port_name": None,
    "height": 30,
    "label": {
        "rotation": 0,
        "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        "text": "Switch",
        "x": -37,
        "y": -25
    },
    "locked": False,
    "name": "Ethernet switch",
    "node_id": switch_id,
    "node_type": "ethernet_switch",
    "port_name_format": "Ethernet{0}",
    "port_segment_size": 0,
    "properties": {},
    "symbol": ":/symbols/classic/multilayer_switch.svg",
    "template_id": "bb10fb96-00ae-4d3f-8025-c2cfb431e39b",
    "width": 66,
    "x": 100,
    "y": 0,
    "z": 1
}

# Adicionar PCs e links à topologia
for i in range(1, num_pcs + 1):
    pc, pc_id = create_pc(i)
    gns3_data["topology"]["nodes"].append(pc)
    link = create_link(pc_id, switch_id, switch_port)
    gns3_data["topology"]["links"].append(link)
    switch_port += 1

    # Criar diretório para o novo PC
    new_pc_dir = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/vpcs/{pc_id}"
    os.makedirs(new_pc_dir, exist_ok=True)

    #!!!! CONSERTAR -> DEVE ESTÁ DENTRO DO FOR
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

# Adiciona o roteador MikroTik à topologia
mikrotik, mikrotik_id = create_mikrotik()
gns3_data["topology"]["nodes"].append(mikrotik)

# Adiciona o switch à topologia
gns3_data["topology"]["nodes"].append(switch)

# Cria o link entre o roteador MikroTik e o switch
router_switch_link = create_router_switch_link(mikrotik_id, switch_id)
gns3_data["topology"]["links"].append(router_switch_link)

# Escrever as alterações de volta ao arquivo .gns3
with open(gns3_file_path, "w") as file:
    json.dump(gns3_data, file, indent=4)

print(f"{num_pcs} PCs foram adicionados ao projeto GNS3 com sucesso!")