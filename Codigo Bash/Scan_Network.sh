#!/usr/bin/env bash

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
ENDCOLOR="\e[0m"

if [ -z "$1" ]; then
    echo -e "${RED}[*] Syntax: <NETWORK/S TO SCAN> Format: 192.168.0 ${ENDCOLOR}"
    exit 1
fi

if [[ $# -eq 1 ]]; then
   hosts=($1)
   echo -e "${GREEN}Lista de Redes: ${ENDCOLOR}${hosts[*]}"
fi

if [[ $# -eq 2 ]]; then
   hosts=($1 $2)
   echo -e "${GREEN}Lista de Redes: ${ENDCOLOR}${hosts[0]}, ${hosts[1]}"
fi

if [[ $# -eq 3 ]]; then
   hosts=($1 $2 $3)
   echo -e "${GREEN}Lista de Redes: ${ENDCOLOR}${hosts[0]}, ${hosts[1]}, ${hosts[2]}"
fi

if [[ $# -eq 4 ]]; then
   hosts=($1 $2 $3 $4)
   echo -e "${GREEN}Lista de Redes: ${ENDCOLOR}${hosts[0]}, ${hosts[1]}, ${hosts[2]}, ${hosts[3]}"
fi

for host in "${hosts[@]}"; do
    echo -e "\n${YELLOW}[*] Enumerando a Rede: $host${ENDCOLOR}\n"
    for i in $(seq 1 254); do
        (
            if timeout 1 bash -c "ping -c 1 $host.$i" &> /dev/null; then
                ttl=$(ping -c 1 $host.$i | grep 'ttl=' | awk -F 'ttl=' '{print $2}' | awk '{print $1}')
                if [[ $ttl -ge 0 ]]; then
                    os="INATIVO"
                    if [[ $ttl -le 64 ]]; then
                        os="Linux"
                    elif [[ $ttl -le 128 ]]; then
                        os="Windows"
                    fi
                    echo "[+] HOST $host.$i ATIVO [OS=$os]"
                else
                    echo "[+] HOST $host.$i ATIVO [OS=UNDETECTED]"
                fi
            fi
        ) &
    done
    wait
done

: << 'COMMENT'
for host in "${hosts[@]}"; do
    echo -e "\n${YELLOW}[*] Enumerando as redes: $host${ENDCOLOR}\n"
    for i in $(seq 1 254); do
        if timeout 1 bash -c "ping -c 1 $host.$i" &> /dev/null; then
            b=$(ping -c 1 $host.$i | grep 'ttl' | awk '{print $(NF - 2), $NF}' | cut -c 5-7)
            if [[ $b =~ 64 ]] || [[ $b =~ 63 ]] || [[ $b =~ 62 ]]; then
                echo "[+] HOST $host.$i ACTIVE [OS=Linux]"
            elif [[ $b =~ 128 ]] || [[ $b =~ 127 ]] || [[ $b =~ 126 ]]; then
                echo "[+] HOST $host.$i ACTIVE [OS=Windows]"
            else
                echo "[+] HOST $host.$i ACTIVE [OS=UNDETECTED]"
            fi
        fi
    done
    wait
done



MANEIRA MAIS RÁPIDA
for host in "${hosts[@]}"; do
    echo -e "\n${YELLOW}[*] Enumerando a Rede: $host${ENDCOLOR}\n"
    for i in $(seq 1 254); do
        (
            if timeout 1 bash -c "ping -c 1 $host.$i" &> /dev/null; then
                ttl=$(ping -c 1 $host.$i | grep 'ttl=' | awk -F 'ttl=' '{print $2}' | awk '{print $1}')
                if [[ $ttl -ge 0 ]]; then
                    os="UNDETECTED"
                    if [[ $ttl -le 64 ]]; then
                        os="Linux"
                    elif [[ $ttl -le 128 ]]; then
                        os="Windows"
                    fi
                    echo "[+] HOST $host.$i ACTIVE [OS=$os]"
                else
                    echo "[+] HOST $host.$i ACTIVE [OS=UNDETECTED]"
                fi
            fi
        ) &
    done
    wait
done
COMMENT


