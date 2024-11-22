import json
import math
from network_utils import execute_network_script, parse_network_output
from topology_utils import create_oraculo_container, create_pc_container, create_switch, create_link

def main():
    # IDs e contadores
    pc_port = 5010  # Porta inicial para PCs

    gns3_file_path = "/home/lucasventura/GNS3/projects/Cenario_GNS3/Cenario_GNS3.gns3"

    with open(gns3_file_path, "r") as file:
        gns3_data = json.load(file)

    num_pcs = int(input("Quantos PCs você deseja adicionar? "))
    num_switches = int(input("Quantos switches você deseja adicionar? "))

    if num_pcs < 1 or num_switches < 1:
        print("Número inválido de PCs ou switches.")
        return

    output = execute_network_script('checar_SCL_2.py')
    network_info = parse_network_output(output)

    if len(network_info) < num_pcs:
        print("Erro: Informações de rede insuficientes.")
        return

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
            pc, pc_id = create_pc_container(pc_counter + 1, switch_x, switch_y, network_info[pc_counter], pc_port)
            gns3_data["topology"]["nodes"].append(pc)
            link = create_link(pc_id, 0, switch_id, i)
            gns3_data["topology"]["links"].append(link)
            pc_counter += 1
    
    # Conectar os switches entre si (topologia linear)
    for i in range(1, len(switch_ids)):
        prev_switch_id, _, _ = switch_ids[i - 1]
        current_switch_id, _, _ = switch_ids[i]

        # Conectar porta 6 de um switch à porta 7 do próximo
        link = create_link(prev_switch_id, 6, current_switch_id, 7)
        gns3_data["topology"]["links"].append(link)
        print(f"Conectado Switch {i} ao Switch {i + 1}.")
    
    # Validar se os links foram criados corretamente
    if not gns3_data["topology"]["links"]:
        print("Erro: Nenhum link foi criado na topologia.")
    else:
        print(f"Total de links criados: {len(gns3_data['topology']['links'])}")
    
    # Adicionar contêiner Docker e linká-lo ao Switch1 na porta e5
    docker_container, docker_id = create_oraculo_container()
    gns3_data["topology"]["nodes"].append(docker_container)
    link = create_link(docker_id, 0, switch_ids[0][0], 5) # Conecta Docker ao Switch1 na porta Ethernet5
    gns3_data["topology"]["links"].append(link)

    # Salvar as mudanças de volta no arquivo .gns3
    with open(gns3_file_path, "w") as file:
        json.dump(gns3_data, file, indent=4)

    print(f"Adicionados {num_pcs} PCs e {num_switches} switches ao projeto.")

if __name__ == "__main__":
    main()
