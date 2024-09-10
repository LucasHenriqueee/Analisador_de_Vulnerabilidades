#!/usr/bin/env bash

# Esse script é responsável por comparar a senha do usuário atual
# com uma senha inserida e verificar se são iguais
# Lucas Ventura 06/06/2024

# Definindo variáveis
xcorrect=0
xwrong=1
enouser=2
enodata=3
esyntax=4
ehash=5
IFS=$'\n'

# Obter o nome do usuário atual
user=$(whoami)

# Função die para imprimir mensagem de erro e sair
die() {
    printf '%s: %s\n' "$0" "$2" >&2
    exit $1
}

# Função report para relatar o resultado da verificação da senha
report() {
    if (($1 == xcorrect)); then
        echo '[*] Senha correta.'
    else
        echo '[*] Senha incorreta.'
    fi
    exit $1
}

# Verificar se o número de argumentos é 1
if (($# != 1)); then
    die $esyntax "Usage: $(basename "$0") <username>"
fi

# Verificar se o usuário existe
case "$(getent passwd "$1" | awk -F: '{print $2}')" in
    x) ;;
    '') die $enouser "[*] error: user '$1' não encontrado";;
    *) die $enodata "[*] error: $1's senha está unshadowed!";;
esac

# Ler a senha do usuário
if [ -t 0 ]; then
    IFS= read -rsp "[$(basename "$0")] senha para $1: " pass
    printf '\n'
else
    IFS= read -r pass
fi

# Obter a entrada do shadow para o usuário
set -f
IFS=':' read -r -a ent <<< "$(getent shadow "$1")"
set +f

# Verificar o tipo de hash da senha
hash_prefix="${ent[1]:0:3}"
case "$hash_prefix" in
    '$1$') hashtype=md5;;
    '$5$') hashtype=sha-256;;
    '$6$') hashtype=sha-512;;
    '') case "${ent[0]}" in
            \*|!) report $xwrong;;
            '') die $enodata "[*] error: no shadow entry (are you root?)";;
            *) die $enodata "[*] error: failure parsing shadow entry";;
        esac;;
    *) die $ehash "[*] error: password hash type is unsupported";;
esac

# Extrair o salt corretamente
salt=$(echo "${ent[1]}" | cut -d'$' -f3)

# Verificar se a senha inserida corresponde ao hash armazenado
hashed_pass=$(mkpasswd -m $hashtype -S "$salt" <<<"$pass")
if [[ "${ent[1]}" = *"$hashed_pass"* ]]; then
    report $xcorrect
else
    report $xwrong
fi