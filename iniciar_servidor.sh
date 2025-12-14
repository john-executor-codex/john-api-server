#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                     JOHN | REVIT BIM MANAGER - API SERVER                    ║"
echo "║                         AEX Inteligência Construtiva                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado! Instale com: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "[INFO] Instalando dependências..."
pip install -r requirements.txt -q

# Iniciar servidor
echo ""
echo "[OK] Iniciando servidor na porta 8000..."
echo "[OK] Acesse: http://localhost:8000/docs"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo " Para expor na internet, abra OUTRO terminal e execute:"
echo " ngrok http 8000"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

python main.py
