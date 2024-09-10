#!/bin/bash

#Obter o nome do usuário atual
user=$(whoami)

#Verificar a entrada do usuário no arquivo /etc/shadow
password_entry=$(sudo grep "^$user:" /etc/shadow | cut -d: -f2)

#Verificar se o campo de senha está vazio ou contém caracteres que indicam a ausência de senha
if [ -z "$password_entry" ] || [[ "$password_entry" == "!"* ]] || [[ "$password_entry" == "*"* ]];
then
	echo "[*] O usuário '$user' não tem uma senha definda ou senha está bloqueada."
else
	echo "[*] O usuário '$user' tem uma senha definida."
fi
