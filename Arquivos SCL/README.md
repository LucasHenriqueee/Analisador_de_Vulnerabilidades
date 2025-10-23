# Arquivos SCL

Nessa pasta encontra-se todos arquivos de modelos de comunicação do padrão IEC 61850 usados no projeto. O padrão IEC 61850 para automação de subestações especifica uma linguagem de configuração de subestação (SCL) padronizada para transferir  descrições de dispositivos e parâmetros de comunicação entre diferentes fornecedores/fabricantes. Os arquivos SCL definem vários subconjuntos de capacidades para o IED instanciar suas capacidades.

- **Hierarquia de Arquivos SCL**:
    1. **Arquivo de Especificação do Sistema (SSD)**: Descreve a configuração completa da subestação com todos os equipamentos primários.
    2. **Arquivo de Capacidades do IED (ICD)**: Detalha as características de um IED, permitindo a troca de informações com ferramentas de configuração.
    3. **Arquivo de Configuração da Subestação (SCD)**: Descreve as características primárias da subestação e todas as configurações dos IEDs.
    4. **Arquivo de Configuração do IED (CID)**: Versão reduzida do SCD, contendo apenas as informações necessárias para o IED.

## Descição dos arquivos

- O arquivo [IEC station 1.scd](PIBIT/Arquivos%20SCL/IEC%20station%201.scd) IEC station 1.scd é um modelo real de uma subestão que utiliza o IEC 61850.
- O arquivo SCD_model.scd é um arquivos derivado da SCL que foi utilizado para realizar a simulação nesse projeto. Foi por meio dele que foi elaborado a criação da topologia no GNS3.
- O arquivo simpleIO_direct_control.cid é apenas uma cofiguração final do IED dentra da IEC 61850.
