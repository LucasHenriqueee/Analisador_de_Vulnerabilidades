# Usando a imagem base Ubuntu 20.04
FROM ubuntu:20.04

# Informações do mantenedor
LABEL maintainer="lucashenrique.oliveira@ee.ufcg.edu.br"

# Defina variáveis de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualizando o sistema e instalando pacotes necessários, incluindo o SSH
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    nano \
    sudo \
    libpam-pwquality \
    curl \
    bash \
    net-tools \
    iputils-ping \
    iproute2 \
    software-properties-common \
    openssh-server \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Criar um usuário comum (não-root)
RUN useradd -m -s /bin/bash -G sudo user && \
    echo "user:user" | chpasswd && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Criar diretório necessário para o SSH
RUN mkdir /run/sshd

# Expondo a porta 22 para o serviço SSH
EXPOSE 22

# Definir o diretório de trabalho para o novo usuário
WORKDIR /home/user

# Iniciar o serviço SSH como root e, em seguida, rodar o Bash como "user"
CMD service ssh start && su - user
