# Usando a imagem base Ubuntu 20.04
FROM ubuntu:20.04

# Informações do mantenedor
LABEL maintainer="lucashenrique.oliveira@ee.ufcg.edu.br"

# Defina variáveis de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

#Atualizando o sistema e isntalando pacotes necessários
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    wget \
    vim \
    git \
    net-tools \
    iputils-ping \
    iproute2 \
    libssl-dev \
    openssh-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# -> Neesa pasta /oraculo, iremos colocar script que realizam as seguinte tarefa dentro da rede:
    # SSH de todos
    # Credenciais do admin
    # A partir disso tudo, oráculo obtém informações de todos os nós e me gera um relatórios


### Criando os diretórios necessários e ajustando permissões
# Precisa desse diretório para armazenar arquivo PID do OpenSSH, sem ele não rodaria
RUN mkdir /var/run/sshd

# Definir senha root para facilitar login via SSH (não recomendado para produção)
RUN echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expondo a porta SSH (acredito que isso não seja seguro, verificar outra alternativa)
#EXPOSE 22

# Defina o diretório de trabalho
WORKDIR /oraculo

### Copie o código-fonte da sua aplicação para o contêiner
# Indentificar os IPs da rede e o SO ativos
COPY scripts_bash/Scan_Network.sh /oraculo/

# Dê permissão de executar ao script
RUN chmod +x /oraculo/Scan_Network.sh

# Comando para ser executado quando o container inicia
CMD ["/bin/bash", "-c", "/usr/sbin/sshd && bash"]