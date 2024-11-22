"""
    Script resonsavel pelo processamento de dados de rede
"""

import subprocess

def execute_network_script(script_name):
    """
    Executa um script externo e retorna a saída como string.
    """
    shell_comando = 'python3 checar_SCL_2.py'
    process = subprocess.Popen(['python3', script_name], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"Erro ao executar {script_name}: código {process.returncode}")
    
    return output.decode()

def parse_network_output(output):
    """
    Processa a saída do script externo e retorna uma lista com informações de rede.
    """
    network_info = []
    ip, subnet, gateway = None, None, None
    for line in output.splitlines():
        if "IP Address" in line:
            ip = line.split(": ")[1]
        if "Subnet Mask" in line:
            subnet = line.split(": ")[1]
        if "Gateway" in line:
            gateway = line.split(": ")[1]
            network_info.append({"ip": ip, "subnet": subnet, "gateway": gateway})

    return network_info