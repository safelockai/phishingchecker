#!/bin/bash

# Verifica se Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python 3 não encontrado. Instalando o Python 3..."
    
    # Para sistemas baseados em Debian (Ubuntu, Termux, etc.)
    if [ -n "$(command -v apt)" ]; then
        sudo apt update
        sudo apt install -y python3 python3-pip

    # Para sistemas baseados em Red Hat (Fedora, CentOS, etc.)
    elif [ -n "$(command -v yum)" ]; then
        sudo yum install -y python3 python3-pip

    # Para macOS com Homebrew
    elif [ -n "$(command -v brew)" ]; then
        brew install python3

    else
        echo "Gerenciador de pacotes não suportado. Instale o Python 3 manualmente."
        exit 1
    fi
else
    echo "Python 3 já está instalado."
fi

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null
then
    echo "pip não encontrado. Instalando pip..."
    python3 -m ensurepip --upgrade
else
    echo "pip já está instalado."
fi

# Instala as bibliotecas necessárias
echo "Instalando bibliotecas necessárias (requests, beautifulsoup4, validators)..."
pip3 install requests beautifulsoup4 validators

# Confirmação final
echo "Instalação completa. Todas as dependências foram instaladas com sucesso."
