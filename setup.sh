#!/bin/bash

#######################################################################
# Nome do Script: setup.sh
# Descrição: Configura automaticamente o ambiente, instalando dependências necessárias.
# Autor: https://github.com/jeanrafaellourenco
# Data: 12/09/2023
# Dependências: python3, pip, python3-venv
# Codificação: UTF8
# Nota: Este script pode solicitar permissões de sudo.
#######################################################################

# Python3 Verificação
if ! [ -x "$(command -v python3)" ]; then
    echo '[ERRO] python3 não está instalado.' >&2
    exit 1
fi

# Verificação da Versão do Python3
python_version="$(python3 --version 2>&1 | awk '{print $2}')"
py_major=$(echo "$python_version" | cut -d'.' -f1)
py_minor=$(echo "$python_version" | cut -d'.' -f2)
if [ "$py_major" -eq "3" ] && [ "$py_minor" -ge "8" ]; then
    echo "[INSTALAÇÃO] Python ${python_version} encontrado"
else
    echo "[ERRO] As dependências requerem o Python 3.8 ou superior. Você possui a versão ${python_version} ou python3 aponta para o Python ${python_version}."
    exit 1
fi

# Verificação e Atualização do Pip
python3 -m pip -V
if [ $? -eq 0 ]; then
    echo '[INSTALAÇÃO] Pip encontrado'
    python3 -m pip install --no-cache-dir --upgrade pip --user
else
    echo '[ALERTA] python3-pip não está instalado'
    sudo apt install python3-pip -y
    python3 -m pip install --no-cache-dir --upgrade pip --user
fi

# Instalação do venv
sudo apt install python3-venv -y
echo '[INSTALAÇÃO] Usando virtualenv Python'
rm -rf ./venv
python3 -m venv ./venv
if [ $? -eq 0 ]; then
    echo '[INSTALAÇÃO] Ativando virtualenv'
    source venv/bin/activate
    pip3 install --upgrade pip
else
    echo '[ERRO] Falha ao criar virtualenv.'
    exit 1
fi

echo '[INSTALAÇÃO] Instalando Requisitos'
pip3 install --no-cache-dir wheel
pip3 install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt
