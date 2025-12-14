# JOHN | Revit BIM Manager - API Server

## 📋 Visão Geral

Servidor FastAPI que implementa todos os 18 endpoints da API JOHN | Revit BIM Manager para integração com GPT Builder.

## 🚀 Instalação Rápida (Windows)

### Opção 1: Script Automático
```
1. Clique duas vezes em: iniciar_servidor.bat
2. Aguarde a instalação das dependências
3. Servidor estará rodando em http://localhost:8000
```

### Opção 2: Manual
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar servidor
python main.py
```

## 🌐 Expor na Internet (Ngrok)

### Instalação do Ngrok
1. Acesse: https://ngrok.com/download
2. Baixe e extraia o executável
3. (Opcional) Crie conta gratuita para URL fixa

### Uso
```bash
# Em outro terminal:
ngrok http 8000
```

### Copiar URL
```
Ngrok mostrará algo como:
Forwarding: https://xxxx-xxx.ngrok-free.app -> http://localhost:8000

Copie a URL HTTPS e atualize no GPT Builder!
```

## 📚 Documentação da API

Com o servidor rodando, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Status da API |
| GET | `/templates` | Listar templates |
| POST | `/templates` | Criar template |
| GET | `/templates/{id}/download` | Download template |
| GET | `/familias` | Listar famílias |
| POST | `/familias` | Criar família |
| GET | `/familias/{id}/download` | Download família |
| GET | `/dynamo/scripts` | Listar scripts |
| POST | `/dynamo/scripts` | Gerar script Dynamo |
| POST | `/dynamo/python` | Gerar código Python |
| POST | `/auditoria/modelo` | Auditar modelo |
| POST | `/auditoria/checklist` | Gerar checklist |
| POST | `/quantitativos/extrair` | Extrair quantidades |
| POST | `/ifc/validar` | Validar IFC |
| GET | `/normas` | Listar normas |
| GET | `/normas/{codigo}` | Consultar norma |
| POST | `/relatorios/bep` | Gerar BEP |
| GET | `/status/{id}` | Status requisição |

## 🧪 Testar Endpoints

### Via curl
```bash
# Health check
curl http://localhost:8000/health

# Listar templates
curl http://localhost:8000/templates

# Criar template
curl -X POST http://localhost:8000/templates \
  -H "Content-Type: application/json" \
  -d '{"tipo_projeto": "residencial", "disciplina": "arquitetura"}'

# Gerar código Python
curl -X POST http://localhost:8000/dynamo/python \
  -H "Content-Type: application/json" \
  -d '{"descricao": "selecionar todas as paredes"}'
```

### Via Swagger
1. Acesse http://localhost:8000/docs
2. Clique no endpoint desejado
3. Clique em "Try it out"
4. Preencha os parâmetros
5. Clique em "Execute"

## 🔧 Configuração no GPT Builder

1. Acesse chat.openai.com
2. Vá em Explore GPTs > Seu GPT > Configure > Actions
3. Atualize a URL do servidor no campo `servers`:

```yaml
servers:
  - url: https://sua-url-ngrok.ngrok-free.app
```

4. Salve e teste!

## 📁 Estrutura de Arquivos

```
JOHN_API_SERVER/
├── main.py              # Servidor principal
├── requirements.txt     # Dependências Python
├── iniciar_servidor.bat # Script de inicialização (Windows)
└── README.md           # Este arquivo
```

## ⚠️ Notas Importantes

1. **Ngrok Gratuito**: A URL muda toda vez que reinicia. Para URL fixa, assine o plano pago ($8/mês).

2. **Dados em Memória**: Este servidor é uma demonstração. Os dados não persistem após reiniciar.

3. **Produção**: Para uso em produção, considere:
   - Hospedar em Railway, Render ou VPS
   - Adicionar banco de dados (PostgreSQL/MongoDB)
   - Implementar autenticação
   - Configurar HTTPS próprio

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python 3.9+ de https://python.org
- Marque "Add to PATH" durante instalação

### Erro: "Porta 8000 em uso"
- Feche outro programa usando a porta
- Ou altere a porta em main.py: `uvicorn.run(app, port=8001)`

### Ngrok não conecta
- Verifique firewall/antivírus
- Tente: `ngrok http 8000 --host-header=localhost`

## 📞 Suporte

- Email: suporte@aexconstrutiva.com.br
- Site: https://aexconstrutiva.com.br

---

© 2025 AEX | Inteligência Construtiva
