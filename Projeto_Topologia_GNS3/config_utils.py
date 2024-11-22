"""
    Scrip responsavel pelo processamento de dados de rede
"""

import os

def generate_interfaces_config(ip, subnet, gateway):
    """
    Gera o conteúdo do arquivo de configuração de rede para um contêiner.
    """
    return f"""#
# Configuração de rede estática para o contêiner
#

# Static config for eth0
auto eth0
iface eth0 inet static
    address {ip}
    netmask {subnet}
    gateway {gateway}
    up echo nameserver 192.168.0.1 > /etc/resolv.conf

# Configuração DHCP (comentada por padrão)
# auto eth0
# iface eth0 inet dhcp
#     hostname container
"""

def write_interfaces_file(container_id, ip, subnet, gateway):
    """
    Escreve o arquivo de configuração `interfaces` no diretório do contêiner.
    """
    base_path = f"/home/lucasventura/GNS3/projects/Cenario_GNS3/project-files/docker/{container_id}/etc/network"
    os.makedirs(base_path, exist_ok=True)  # Garante que o diretório existe

    # Gerar conteúdo do arquivo
    interfaces_content = generate_interfaces_config(ip, subnet, gateway)

    # Salvar arquivo no caminho
    interfaces_path = os.path.join(base_path, "interfaces")
    with open(interfaces_path, "w") as file:
        file.write(interfaces_content)

    print(f"Configuração de rede salva em {interfaces_path}")