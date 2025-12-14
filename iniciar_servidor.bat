@echo off
title JOHN | Revit BIM Manager API Server

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                     JOHN ^| REVIT BIM MANAGER - API SERVER                    ║
echo ║                         AEX Inteligência Construtiva                         ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale em: https://python.org
    pause
    exit /b 1
)

:: Criar ambiente virtual se não existir
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
)

:: Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Instalar dependências
echo [INFO] Instalando dependencias...
pip install -r requirements.txt -q

:: Iniciar servidor
echo.
echo [OK] Iniciando servidor na porta 8000...
echo [OK] Acesse: http://localhost:8000/docs
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo  Para expor na internet, abra OUTRO terminal e execute:
echo  ngrok http 8000
echo ════════════════════════════════════════════════════════════════════════════════
echo.

python main.py

pause
