#!/bin/bash

#######################################################################
# Nome do Script: run.sh
# Descrição: Facilita a execução da ferramenta com comandos predefinidos.
# Autor: https://github.com/jeanrafaellourenco
# Data: 12/09/2023
# Dependências: python3, pip, python3-venv
# Codificação: UTF8
# Nota: Este script não requer permissões especiais para ser executado.
#######################################################################

echo -e "Executando aplicação python"
. venv/bin/activate &&  python3 ApiScan.py
