#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Esse script propõe realizar uma leitura que colet informações disponibilizadas
    pelo IEDs, e partir disso, construa a topologia da rede e realizar a análise de segurança seguindo
    uma base de atques
"""

import xml.etree.ElementTree as ET

# Caminho para o arquivo SCL
file_path = 'simpleIO_direct_control.cid'

# Função para carregar e parsear o arquivo XML
def parse_scl_file(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Erro ao parsear o arquivo XML: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return None
    
# Função para depurar a estrutura do XML
def print_xml_structure(root, level=0):
    indent = "  " * level
    print(f"{indent}<{root.tag}>")
    for child in root:
        print_xml_structure(child, level + 1)

####################################################################################
# Função para extrair informações de rede dos IEDs
"""
DESCRIÇÃO DA FUNÇÃO:
    A função extract_network_info percorre a estrutura XML 
    para encontrar os elementos relevantes (IED, AccessPoint, Server, 
    LDevice, LN0, LN, ConnectedAP, Address).

    Dentro de Address, busca pelos elementos P que contêm os parâmetros de rede
    (como IP, sub-rede, etc.).

    As informações extraídas são armazenadas em um dicionário que é adicionado a
    uma lista ied_info.
"""
####################################################################################

def extrair_network_info(root):
    namespace = {'iec': 'http://www.iec.ch/61850/2003/SCL'}
    ied_info = []

    # Buscar informações dentro da tag <Communication>
    for communication in root.findall('iec:Communication', namespace):
        for subnetwork in communication.findall('iec:SubNetwork', namespace):
            for connected_ap in subnetwork.findall('iec:ConnectedAP', namespace):
                ap_name = connected_ap.get('apName')
                ied_name_in_ap = connected_ap.get('iedName')
                for address in connected_ap.findall('iec:Address', namespace):
                    network_info = {}
                    for p in address.findall('iec:P', namespace):
                        network_info[p.get('type')] = p.text
                    ied_info.append({
                        'AP Name': ap_name,
                        'IED Name in AP': ied_name_in_ap,
                        'Network Info': network_info
                    })
    return ied_info

########################################################################
## Função para imprimir as informações de rede
"""
DESCRIÇÃO DA FUNÇÃO:
    A função print_network_info percorre a lista de informações
    de rede e imprime cada conjunto de informações de forma estruturada.
"""
########################################################################

def print_network_info(network_info):
    if not network_info:
        print("Nenhuma informação de rede encontrada.")
        return

    for info in network_info:
        print(f"AP Name: {info['AP Name']}")
        print(f"IED Name in AP: {info['IED Name in AP']}")
        for key, value in info['Network Info'].items():
            print(f"  {key}: {value}")
        print("\n")

# Carregar e parsear o arquivo SCL
root = parse_scl_file(file_path)

if root is not None:
    # Extrair as informações de rede
    network_info = extrair_network_info(root)

    # Imprimir as informações de rede
    print_network_info(network_info)
else:
    print("Não foi possível carregar o arquivo SCL.")