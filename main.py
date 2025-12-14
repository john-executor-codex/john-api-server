"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     JOHN | REVIT BIM MANAGER - API SERVER                    ║
║                         AEX Inteligência Construtiva                         ║
║                              Versão 2.0.0                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Servidor FastAPI para o sistema JOHN | Revit BIM Manager.
Implementa todos os 18 endpoints do GPT Builder.

INSTALAÇÃO:
    pip install fastapi uvicorn pydantic python-multipart aiofiles

EXECUÇÃO:
    python main.py

NGROK:
    ngrok http 8000
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import json

# ============================================
# INICIALIZAÇÃO DO APP
# ============================================

app = FastAPI(
    title="JOHN | Revit BIM Manager API",
    description="API oficial do sistema JOHN | Revit BIM Manager - AEX Inteligência Construtiva",
    version="2.0.0",
    contact={
        "name": "AEX | Inteligência Construtiva",
        "email": "suporte@aexconstrutiva.com.br"
    }
)

# CORS - Permite requisições do GPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# BANCO DE DADOS EM MEMÓRIA (SIMULADO)
# ============================================

# Armazena requisições
requisicoes_db: Dict[str, Dict] = {}

# Templates pré-definidos
templates_db = [
    {
        "id": "tpl-001",
        "nome": "Template Residencial Básico",
        "tipo_projeto": "residencial",
        "disciplina": "arquitetura",
        "descricao": "Template para projetos residenciais com vistas padrão",
        "versao_revit": "2024",
        "tamanho_mb": 15.2
    },
    {
        "id": "tpl-002",
        "nome": "Template Comercial Completo",
        "tipo_projeto": "comercial",
        "disciplina": "coordenacao",
        "descricao": "Template para edifícios comerciais com todas as disciplinas",
        "versao_revit": "2024",
        "tamanho_mb": 28.5
    },
    {
        "id": "tpl-003",
        "nome": "Template Industrial MEP",
        "tipo_projeto": "industrial",
        "disciplina": "mep",
        "descricao": "Template focado em instalações industriais",
        "versao_revit": "2024",
        "tamanho_mb": 22.1
    }
]

# Famílias pré-definidas
familias_db = [
    {
        "id": "fam-001",
        "nome": "Porta Madeira 80x210",
        "categoria": "portas",
        "lod": 300,
        "parametros": ["Largura", "Altura", "Espessura", "Material"],
        "tamanho_kb": 256
    },
    {
        "id": "fam-002",
        "nome": "Janela Alumínio 120x120",
        "categoria": "janelas",
        "lod": 300,
        "parametros": ["Largura", "Altura", "Peitoril", "Tipo_Vidro"],
        "tamanho_kb": 312
    },
    {
        "id": "fam-003",
        "nome": "Mesa Escritório",
        "categoria": "mobiliario",
        "lod": 200,
        "parametros": ["Comprimento", "Largura", "Altura"],
        "tamanho_kb": 128
    }
]

# Scripts Dynamo pré-definidos
scripts_db = [
    {
        "id": "dyn-001",
        "nome": "Renomear Views por Nível",
        "descricao": "Renomeia todas as views de planta adicionando o nome do nível como prefixo",
        "categoria": "automacao",
        "complexidade": "simples",
        "pacotes_necessarios": []
    },
    {
        "id": "dyn-002",
        "nome": "Exportar Parâmetros para Excel",
        "descricao": "Exporta parâmetros de elementos selecionados para planilha Excel",
        "categoria": "dados",
        "complexidade": "intermediario",
        "pacotes_necessarios": ["archi-lab"]
    },
    {
        "id": "dyn-003",
        "nome": "Criar Sheets em Lote",
        "descricao": "Cria múltiplas sheets a partir de lista Excel",
        "categoria": "documentacao",
        "complexidade": "intermediario",
        "pacotes_necessarios": ["Clockwork"]
    }
]

# Normas técnicas
normas_db = [
    {
        "codigo": "NBR-15965",
        "titulo": "Sistema de classificação da informação da construção",
        "tipo": "nbr",
        "area": "bim",
        "resumo": "Estabelece o sistema de classificação da informação da construção para uso em BIM",
        "aplicacao_bim": "Classificação de elementos, organização de informações, interoperabilidade"
    },
    {
        "codigo": "ISO-19650",
        "titulo": "Organização da informação sobre obras de construção",
        "tipo": "iso",
        "area": "bim",
        "resumo": "Norma internacional para gestão da informação usando BIM",
        "aplicacao_bim": "Gestão de informação, processos de entrega, requisitos de dados"
    },
    {
        "codigo": "NBR-9050",
        "titulo": "Acessibilidade a edificações, mobiliário, espaços e equipamentos urbanos",
        "tipo": "nbr",
        "area": "acessibilidade",
        "resumo": "Critérios e parâmetros técnicos de acessibilidade",
        "aplicacao_bim": "Verificação de rotas acessíveis, dimensionamento de espaços, clash detection"
    },
    {
        "codigo": "NBR-6118",
        "titulo": "Projeto de estruturas de concreto",
        "tipo": "nbr",
        "area": "estrutura",
        "resumo": "Requisitos para projeto de estruturas de concreto armado e protendido",
        "aplicacao_bim": "Modelagem estrutural, detalhamento de armaduras, verificação de cobrimentos"
    }
]


# ============================================
# MODELOS PYDANTIC (REQUEST/RESPONSE)
# ============================================

# --- Templates ---
class TemplateRequest(BaseModel):
    tipo_projeto: str = Field(..., description="Tipo do projeto")
    disciplina: Optional[str] = "arquitetura"
    normas: Optional[List[str]] = []

class TemplateResponse(BaseModel):
    status: str
    id_requisicao: str
    arquivo: str
    url_download: str
    mensagem: str

# --- Famílias ---
class FamiliaRequest(BaseModel):
    nome: str
    categoria: str
    lod: Optional[int] = 300
    parametros: Optional[Dict[str, Any]] = {}

class FamiliaResponse(BaseModel):
    status: str
    id_requisicao: str
    arquivo: str
    url_download: str
    mensagem: str

# --- Dynamo ---
class DynamoScriptRequest(BaseModel):
    descricao: str
    categoria: Optional[str] = "automacao"
    usar_python: Optional[bool] = False
    versao_dynamo: Optional[str] = "2.x"

class PythonNodeRequest(BaseModel):
    descricao: str
    usar_revit_api: Optional[bool] = True

# --- Auditoria ---
class AuditoriaRequest(BaseModel):
    arquivo_url: str
    nivel_auditoria: Optional[str] = "padrao"

class ChecklistRequest(BaseModel):
    tipo_projeto: str
    fase: str
    disciplinas: Optional[List[str]] = []

# --- Quantitativos ---
class QuantitativosRequest(BaseModel):
    arquivo_url: str
    categorias: Optional[List[str]] = []
    formato_saida: Optional[str] = "json"

# --- IFC ---
class IFCValidacaoRequest(BaseModel):
    arquivo_url: str
    mvd: Optional[str] = "coordination_view"

# --- Relatórios ---
class BEPRequest(BaseModel):
    nome_projeto: str
    tipo_projeto: str
    cliente: Optional[str] = ""
    disciplinas: Optional[List[str]] = []


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def gerar_id_requisicao() -> str:
    """Gera ID único para requisição"""
    return f"req-{uuid.uuid4().hex[:8]}"

def salvar_requisicao(id_req: str, tipo: str, dados: dict):
    """Salva requisição no banco"""
    requisicoes_db[id_req] = {
        "id_requisicao": id_req,
        "tipo": tipo,
        "status": "concluido",
        "progresso_percentual": 100,
        "criado_em": datetime.now().isoformat(),
        "resultado": dados
    }

def gerar_codigo_python(descricao: str, usar_api: bool) -> dict:
    """Gera código Python baseado na descrição"""
    
    # Templates de código baseados em palavras-chave
    if "parede" in descricao.lower() or "wall" in descricao.lower():
        codigo = '''# SELECIONAR PAREDES POR TIPO
# Descrição: Seleciona todas as paredes de um tipo específico
# Input: IN[0] = Nome do tipo de parede (string)

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
tipo_busca = IN[0]

# Coletar todas as paredes
collector = FilteredElementCollector(doc)
walls = collector.OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# Filtrar por tipo
resultado = [w for w in walls if w.Name == tipo_busca]

OUT = resultado'''

    elif "view" in descricao.lower() or "vista" in descricao.lower():
        codigo = '''# RENOMEAR VIEWS
# Descrição: Renomeia views adicionando prefixo
# Input: IN[0] = Prefixo (string)

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
prefixo = IN[0]

# Coletar views
collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements()

# Filtrar views válidas (não são templates)
views_validas = [v for v in views if not v.IsTemplate and v.CanBePrinted]

TransactionManager.Instance.EnsureInTransaction(doc)

renomeadas = []
for view in views_validas:
    try:
        novo_nome = f"{prefixo}_{view.Name}"
        view.Name = novo_nome
        renomeadas.append(novo_nome)
    except:
        pass

TransactionManager.Instance.TransactionTaskDone()

OUT = renomeadas'''

    elif "excel" in descricao.lower() or "export" in descricao.lower():
        codigo = '''# EXPORTAR PARA EXCEL
# Descrição: Exporta dados de elementos para Excel
# Input: IN[0] = Elementos, IN[1] = Caminho do arquivo

import clr
clr.AddReference('RevitAPI')

from Autodesk.Revit.DB import *

elementos = UnwrapElement(IN[0])
caminho = IN[1]

# Coletar dados
dados = []
for elem in elementos:
    linha = {
        "Id": elem.Id.IntegerValue,
        "Categoria": elem.Category.Name if elem.Category else "N/A",
        "Tipo": elem.Name
    }
    dados.append(linha)

# Criar CSV simples
import csv
with open(caminho, 'w', newline='', encoding='utf-8') as f:
    if dados:
        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)

OUT = f"Exportado: {len(dados)} elementos para {caminho}"'''

    else:
        codigo = f'''# SCRIPT PERSONALIZADO
# Descrição: {descricao}
# Gerado automaticamente pelo JOHN | Revit BIM Manager

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# TODO: Implementar lógica específica
# Baseado na descrição: {descricao}

# Exemplo de collector
collector = FilteredElementCollector(doc)
elementos = collector.WhereElementIsNotElementType().ToElements()

OUT = f"Total de elementos: {{len(list(elementos))}}"'''

    return {
        "codigo": codigo,
        "explicacao": f"Script Python gerado para: {descricao}",
        "inputs": ["IN[0] - Parâmetro de entrada"],
        "outputs": ["OUT - Resultado da operação"],
        "referencias": ["RevitAPI", "RevitServices"]
    }


# ============================================
# ENDPOINTS - HEALTH
# ============================================

@app.get("/health", tags=["Health"])
async def verificar_saude():
    """Verificar saúde da API"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "service": "JOHN | Revit BIM Manager API",
        "endpoints_ativos": 18
    }


# ============================================
# ENDPOINTS - TEMPLATES
# ============================================

@app.get("/templates", tags=["Templates"])
async def listar_templates(
    tipo_projeto: Optional[str] = Query(None, description="Filtrar por tipo de projeto")
):
    """Listar templates disponíveis"""
    if tipo_projeto:
        return [t for t in templates_db if t["tipo_projeto"] == tipo_projeto]
    return templates_db


@app.post("/templates", tags=["Templates"])
async def criar_template(request: TemplateRequest):
    """Criar template Revit personalizado"""
    id_req = gerar_id_requisicao()
    
    arquivo = f"template_{request.tipo_projeto}_{request.disciplina}_v1.rte"
    
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "arquivo": arquivo,
        "url_download": f"https://api.aexconstrutiva.com.br/download/{id_req}/{arquivo}",
        "mensagem": f"Template {request.tipo_projeto} para {request.disciplina} criado com sucesso!",
        "detalhes": {
            "tipo_projeto": request.tipo_projeto,
            "disciplina": request.disciplina,
            "normas_aplicadas": request.normas,
            "vistas_criadas": 12,
            "view_templates": 8,
            "parametros_compartilhados": 45
        }
    }
    
    salvar_requisicao(id_req, "template", resultado)
    return resultado


@app.get("/templates/{template_id}/download", tags=["Templates"])
async def download_template(template_id: str = Path(..., description="ID do template")):
    """Download do arquivo template"""
    template = next((t for t in templates_db if t["id"] == template_id), None)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return {
        "id": template_id,
        "arquivo": f"{template['nome'].replace(' ', '_')}.rte",
        "url_download": f"https://storage.aexconstrutiva.com.br/templates/{template_id}.rte",
        "validade": "24 horas",
        "tamanho_mb": template["tamanho_mb"]
    }


# ============================================
# ENDPOINTS - FAMÍLIAS
# ============================================

@app.get("/familias", tags=["Famílias"])
async def listar_familias(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria")
):
    """Listar famílias disponíveis"""
    if categoria:
        return [f for f in familias_db if f["categoria"] == categoria]
    return familias_db


@app.post("/familias", tags=["Famílias"])
async def criar_familia(request: FamiliaRequest):
    """Criar família paramétrica Revit"""
    id_req = gerar_id_requisicao()
    
    arquivo = f"{request.nome.replace(' ', '_').lower()}.rfa"
    
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "arquivo": arquivo,
        "url_download": f"https://api.aexconstrutiva.com.br/download/{id_req}/{arquivo}",
        "mensagem": f"Família '{request.nome}' criada com sucesso!",
        "detalhes": {
            "nome": request.nome,
            "categoria": request.categoria,
            "lod": request.lod,
            "parametros_criados": len(request.parametros) if request.parametros else 4,
            "tipos_gerados": 1
        }
    }
    
    salvar_requisicao(id_req, "familia", resultado)
    return resultado


@app.get("/familias/{familia_id}/download", tags=["Famílias"])
async def download_familia(familia_id: str = Path(..., description="ID da família")):
    """Download do arquivo família"""
    familia = next((f for f in familias_db if f["id"] == familia_id), None)
    
    if not familia:
        raise HTTPException(status_code=404, detail="Família não encontrada")
    
    return {
        "id": familia_id,
        "arquivo": f"{familia['nome'].replace(' ', '_')}.rfa",
        "url_download": f"https://storage.aexconstrutiva.com.br/familias/{familia_id}.rfa",
        "validade": "24 horas",
        "tamanho_kb": familia["tamanho_kb"]
    }


# ============================================
# ENDPOINTS - DYNAMO
# ============================================

@app.get("/dynamo/scripts", tags=["Dynamo"])
async def listar_scripts_dynamo(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria")
):
    """Listar scripts Dynamo disponíveis"""
    if categoria:
        return [s for s in scripts_db if s["categoria"] == categoria]
    return scripts_db


@app.post("/dynamo/scripts", tags=["Dynamo"])
async def gerar_script_dynamo(request: DynamoScriptRequest):
    """Gerar script Dynamo baseado na descrição"""
    id_req = gerar_id_requisicao()
    
    # Gerar nome do arquivo baseado na descrição
    nome_arquivo = request.descricao[:30].replace(" ", "_").lower()
    arquivo = f"{nome_arquivo}.dyn"
    
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "arquivo": arquivo,
        "url_download": f"https://api.aexconstrutiva.com.br/download/{id_req}/{arquivo}",
        "instrucoes_uso": f"""
COMO USAR O SCRIPT:

1. Abra o Revit e o projeto desejado
2. Vá em Manage > Dynamo
3. File > Open > Selecione o arquivo {arquivo}
4. Configure os inputs conforme necessário
5. Clique em "Run"

DESCRIÇÃO:
{request.descricao}

CATEGORIA: {request.categoria}
VERSÃO DYNAMO: {request.versao_dynamo}
USA PYTHON: {"Sim" if request.usar_python else "Não"}
        """,
        "preview": {
            "nodes_principais": ["Input", "Collector", "Filter", "Output"],
            "pacotes_necessarios": ["Clockwork"] if request.usar_python else [],
            "complexidade_estimada": "intermediário"
        }
    }
    
    salvar_requisicao(id_req, "dynamo", resultado)
    return resultado


@app.post("/dynamo/python", tags=["Dynamo"])
async def gerar_python_node(request: PythonNodeRequest):
    """Gerar código Python para Dynamo"""
    resultado = gerar_codigo_python(request.descricao, request.usar_revit_api)
    return resultado


# ============================================
# ENDPOINTS - AUDITORIA
# ============================================

@app.post("/auditoria/modelo", tags=["Auditoria"])
async def auditar_modelo(request: AuditoriaRequest):
    """Auditar modelo Revit"""
    id_req = gerar_id_requisicao()
    
    # Simular análise
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "score_geral": 78,
        "classificacao": "bom",
        "resumo": {
            "tamanho_arquivo_mb": 125.4,
            "total_elementos": 15420,
            "total_familias": 234,
            "total_warnings": 45,
            "total_erros": 3
        },
        "categorias": [
            {"nome": "Modelagem", "score": 85, "status": "bom"},
            {"nome": "Organização", "score": 72, "status": "regular"},
            {"nome": "Performance", "score": 68, "status": "regular"},
            {"nome": "Documentação", "score": 88, "status": "bom"},
            {"nome": "Coordenação", "score": 75, "status": "bom"}
        ],
        "recomendacoes": [
            "Executar Purge Unused para remover 23 famílias não utilizadas",
            "Resolver 12 warnings de elementos duplicados",
            "Otimizar 5 famílias com geometria excessiva",
            "Atualizar 8 views com view templates desatualizados"
        ],
        "url_relatorio_pdf": f"https://api.aexconstrutiva.com.br/download/{id_req}/auditoria_relatorio.pdf"
    }
    
    salvar_requisicao(id_req, "auditoria", resultado)
    return resultado


@app.post("/auditoria/checklist", tags=["Auditoria"])
async def gerar_checklist(request: ChecklistRequest):
    """Gerar checklist de auditoria BIM"""
    
    # Checklists por fase
    itens_por_fase = {
        "concepcao": [
            "Volume geral do edifício definido",
            "Níveis principais criados",
            "Grid estrutural básico",
            "Estudo de massas concluído"
        ],
        "anteprojeto": [
            "Paredes externas modeladas",
            "Esquadrias principais posicionadas",
            "Circulações verticais definidas",
            "Cobertura modelada"
        ],
        "projeto_legal": [
            "Áreas calculadas e verificadas",
            "Cotas de nível conferidas",
            "Acessibilidade verificada (NBR 9050)",
            "Recuos e afastamentos conferidos"
        ],
        "executivo": [
            "Detalhamento completo",
            "Quantitativos extraídos",
            "Compatibilização realizada",
            "Pranchas geradas"
        ],
        "as_built": [
            "Modelo atualizado conforme construído",
            "Informações de fabricantes incluídas",
            "Documentação de manutenção anexada",
            "Entrega para operação preparada"
        ]
    }
    
    itens = itens_por_fase.get(request.fase, [])
    
    checklist = {
        "titulo": f"Checklist BIM - {request.tipo_projeto.title()} - Fase {request.fase.replace('_', ' ').title()}",
        "tipo_projeto": request.tipo_projeto,
        "fase": request.fase,
        "disciplinas": request.disciplinas or ["geral"],
        "itens": [
            {
                "categoria": "Verificações Gerais",
                "verificacoes": [
                    {"item": item, "obrigatorio": True, "status": "pendente"}
                    for item in itens
                ]
            },
            {
                "categoria": "Qualidade do Modelo",
                "verificacoes": [
                    {"item": "Warnings abaixo de 100", "obrigatorio": True, "status": "pendente"},
                    {"item": "Purge Unused executado", "obrigatorio": True, "status": "pendente"},
                    {"item": "Audit realizado", "obrigatorio": False, "status": "pendente"},
                    {"item": "Nomenclatura padronizada", "obrigatorio": True, "status": "pendente"}
                ]
            }
        ],
        "gerado_em": datetime.now().isoformat()
    }
    
    return checklist


# ============================================
# ENDPOINTS - QUANTITATIVOS
# ============================================

@app.post("/quantitativos/extrair", tags=["Quantitativos"])
async def extrair_quantitativos(request: QuantitativosRequest):
    """Extrair quantitativos do modelo"""
    id_req = gerar_id_requisicao()
    
    # Simular extração
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "resumo": {
            "total_categorias": 8,
            "total_elementos": 1250,
            "formato": request.formato_saida
        },
        "quantitativos": [
            {
                "categoria": "Paredes",
                "quantidade": 245,
                "area_total_m2": 1850.5,
                "volume_total_m3": 425.2
            },
            {
                "categoria": "Pisos",
                "quantidade": 45,
                "area_total_m2": 2100.0,
                "volume_total_m3": 210.0
            },
            {
                "categoria": "Portas",
                "quantidade": 86,
                "unidades": 86
            },
            {
                "categoria": "Janelas",
                "quantidade": 124,
                "unidades": 124,
                "area_total_m2": 186.0
            }
        ],
        "url_download_excel": f"https://api.aexconstrutiva.com.br/download/{id_req}/quantitativos.xlsx"
    }
    
    salvar_requisicao(id_req, "quantitativos", resultado)
    return resultado


# ============================================
# ENDPOINTS - IFC
# ============================================

@app.post("/ifc/validar", tags=["IFC"])
async def validar_ifc(request: IFCValidacaoRequest):
    """Validar arquivo IFC"""
    id_req = gerar_id_requisicao()
    
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "valido": True,
        "versao_ifc": "IFC4",
        "mvd_testado": request.mvd,
        "estatisticas": {
            "total_entidades": 45230,
            "ifcwall": 245,
            "ifcslab": 45,
            "ifcdoor": 86,
            "ifcwindow": 124,
            "ifcspace": 52
        },
        "erros": [],
        "alertas": [
            {
                "tipo": "recomendacao",
                "mensagem": "12 elementos sem classificação definida",
                "severidade": "baixa"
            },
            {
                "tipo": "recomendacao", 
                "mensagem": "5 espaços sem nome definido",
                "severidade": "media"
            }
        ]
    }
    
    salvar_requisicao(id_req, "ifc", resultado)
    return resultado


# ============================================
# ENDPOINTS - NORMAS
# ============================================

@app.get("/normas", tags=["Normas"])
async def listar_normas(
    tipo: Optional[str] = Query(None, description="Tipo da norma (nbr, iso, ifc)"),
    area: Optional[str] = Query(None, description="Área de aplicação")
):
    """Listar normas técnicas disponíveis"""
    resultado = normas_db
    
    if tipo:
        resultado = [n for n in resultado if n["tipo"] == tipo]
    if area:
        resultado = [n for n in resultado if n["area"] == area]
    
    return resultado


@app.get("/normas/{codigo}", tags=["Normas"])
async def consultar_norma(codigo: str = Path(..., description="Código da norma")):
    """Consultar norma específica"""
    norma = next((n for n in normas_db if n["codigo"] == codigo), None)
    
    if not norma:
        raise HTTPException(status_code=404, detail="Norma não encontrada")
    
    return norma


# ============================================
# ENDPOINTS - RELATÓRIOS
# ============================================

@app.post("/relatorios/bep", tags=["Relatórios"])
async def gerar_bep(request: BEPRequest):
    """Gerar BIM Execution Plan"""
    id_req = gerar_id_requisicao()
    
    resultado = {
        "status": "sucesso",
        "id_requisicao": id_req,
        "arquivo": f"BEP_{request.nome_projeto.replace(' ', '_')}.pdf",
        "url_download": f"https://api.aexconstrutiva.com.br/download/{id_req}/bep.pdf",
        "conteudo_gerado": {
            "nome_projeto": request.nome_projeto,
            "tipo_projeto": request.tipo_projeto,
            "cliente": request.cliente,
            "disciplinas": request.disciplinas or ["Arquitetura", "Estrutura", "MEP"],
            "secoes_incluidas": [
                "Informações do Projeto",
                "Objetivos BIM",
                "Usos do Modelo BIM",
                "Matriz de Responsabilidades",
                "Requisitos de Entrega",
                "Padrões e Protocolos",
                "Infraestrutura Tecnológica",
                "Controle de Qualidade"
            ]
        }
    }
    
    salvar_requisicao(id_req, "bep", resultado)
    return resultado


# ============================================
# ENDPOINTS - STATUS
# ============================================

@app.get("/status/{id_requisicao}", tags=["Status"])
async def obter_status(id_requisicao: str = Path(..., description="ID da requisição")):
    """Verificar status de uma requisição"""
    
    if id_requisicao in requisicoes_db:
        return requisicoes_db[id_requisicao]
    
    raise HTTPException(status_code=404, detail="Requisição não encontrada")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     JOHN | REVIT BIM MANAGER - API SERVER                    ║
║                         AEX Inteligência Construtiva                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Servidor iniciando em: http://localhost:8000                                ║
║  Documentação Swagger:  http://localhost:8000/docs                           ║
║  Documentação ReDoc:    http://localhost:8000/redoc                          ║
║                                                                              ║
║  Para expor na internet, execute em outro terminal:                          ║
║  > ngrok http 8000                                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
