# Memory Lab

> **4-Tier Cognitive Memory Architecture for Autonomous Software Engineering Agents**  
> Um sistema local-first de persistência e orquestração de memória cognitiva inspirado no ACT-R, integrando ferramentas MCP, hooks de ciclo de vida e um dashboard de inspeção visual com estética *Dark Luxury*.

---

## 📑 Sumário

- [Visão Geral](#-visão-geral)
- [Arquitetura dos 4 Níveis Cognitivos](#-arquitetura-dos-4-níveis-cognitivos)
- [Recursos e Diferenciais](#-recursos-e-diferenciais)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Instalação e Pré-requisitos](#-instalação-e-pré-requisitos)
- [Como Executar](#-como-executar)
  - [1. Suíte de Testes Unitários](#1-suíte-de-testes-unitários)
  - [2. Dashboard Interativo (React + Vite)](#2-dashboard-interativo-react--vite)
  - [3. Servidor MCP (Model Context Protocol)](#3-servidor-mcp-model-context-protocol)
- [Guia de Uso (Python SDK)](#-guia-de-uso-python-sdk)
  - [Memória Episódica (`StorageEngine`)](#1-memória-episódica-storageengine)
  - [Memória Semântica (`SemanticGraph`)](#2-memória-semântica-semanticgraph)
  - [Memória de Trabalho (`WorkingMemoryBuffer`)](#3-memória-de-trabalho-workingmemorybuffer)
  - [Memória Procedural (`ProceduralStore`)](#4-memória-procedural-proceduralstore)
  - [Ciclo de Vida do Agente (`MemoryHook`)](#5-ciclo-de-vida-do-agente-memoryhook)
- [Configuração do MCP para Agentes (Claude / Cursor)](#-configuração-do-mcp-para-agentes-claude--cursor)
- [Metodologia e Proveniência (Converge)](#-metodologia-e-proveniência-converge)

---

## 🧠 Visão Geral

Modelos de linguagem operam sem memória contínua e sofrem com degradação por sobrecarga de contexto. O **Memory Lab** resolve essa limitação desacoplando o fluxo de retenção em quatro camadas cognitivas especializadas:

1. **Memória de Trabalho:** Foco atencional com teto rígido de tokens e despejo inteligente.
2. **Memória Episódica:** Registro durável de rastros de execução, comandos e aprendizados com índice de busca em texto pleno.
3. **Memória Semântica:** Grafo de conceitos com ativação espalhada (*spreading activation*) ponderada por decaimento.
4. **Memória Procedural:** Rotinas e habilidades reforçadas com base na frequência de sucesso e recência de uso (*Power Law of Practice*).

---

## 🏛 Arquitetura dos 4 Níveis Cognitivos

```
┌────────────────────────────────────────────────────────────────────────┐
│                          MEMORY LAB RUNTIME                            │
├────────────────────────────────────────────────────────────────────────┤
│  Tier 1: WORKING MEMORY (Atenção Imediata)                             │
│  - Limite estrito de 4.000 tokens                                      │
│  - Algoritmo de despejo por menor saliência e recência                 │
├────────────────────────────────────────────────────────────────────────┤
│  Tier 2: EPISODIC MEMORY (Histórico de Execuções)                      │
│  - SQLite WAL (Write-Ahead Logging) local-first                        │
│  - Latência de escrita/leitura < 100ms                                 │
│  - Indexação full-text via FTS5 (Porter Unicode tokenizer)             │
├────────────────────────────────────────────────────────────────────────┤
│  Tier 3: SEMANTIC MEMORY (Grafo Associativo)                           │
│  - Nós conceituais e arestas ponderadas bidirecionais                  │
│  - Spreading Activation (decaimento 0.85, max_hops 2)                  │
├────────────────────────────────────────────────────────────────────────┤
│  Tier 4: PROCEDURAL MEMORY (Habilidades Operacionais)                  │
│  - Receitas e passos executáveis registrados                           │
│  - ACT-R Power Law of Practice (reforço logarítmico em sucesso)        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Recursos e Diferenciais

- **100% Local-First:** Opera integralmente sobre SQLite em modo WAL. Zero dependência de nuvem, banco externo ou custo por token de embedding.
- **Suporte Nativo a MCP:** Servidor padrão JSON-RPC 2.0 via `stdio` pronto para plugar em agentes como Claude Code, Cursor, Windsurf e Antigravity.
- **Hooks de Ciclo de Vida (`MemoryHook`):** Injeta contexto destilado automaticamente antes do disparo do LLM (`pre_execution`) e consolida aprendizado após o término (`post_execution`).
- **Dashboard Visual Dark Luxury:**
  - Estética refinada `#0a0a0a` com tipografia em *EB Garamond* e *JetBrains Mono*.
  - **Amber Cascades:** Partículas douradas/âmbar fluidas em Canvas 2D renderizadas a 60 FPS com resposta interativa ao cursor.
  - **LiquidGlass:** Botões estilizados com refração óptica via SVG `<feDisplacementMap>`.
  - **Graph Explorer:** Visualizador gráfico com halos radiantes e pulsos luminosos de ativação espalhada.

---

## 📂 Estrutura do Repositório

```
memory_lab/
├── memory_lab/
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── schema.py              # Esquema SQLite, pragmas WAL, FTS5 e índices
│   │   └── engine.py              # Motor StorageEngine (CRUD transacional < 100ms)
│   ├── cognitive/
│   │   ├── __init__.py
│   │   ├── semantic.py            # SemanticGraph e algoritmo de Spreading Activation
│   │   └── working.py             # WorkingMemoryBuffer (4k tokens) e ProceduralStore
│   └── interfaces/
│       ├── __init__.py
│       ├── mcp_server.py          # Servidor MCP stdio / JSON-RPC 2.0
│       └── hook.py                # Converge MemoryHook de ciclo pré/pós-execução
├── tests/
│   ├── test_storage.py            # Testes de persistência SQLite e FTS5
│   ├── test_semantic.py           # Testes do grafo associativo e ativação espalhada
│   ├── test_cognitive.py          # Testes de teto de tokens e power-law procedural
│   ├── test_mcp.py                # Testes de ferramentas MCP e protocolo JSON-RPC
│   └── test_hook.py               # Testes dos hooks de ciclo de vida
├── frontend/
│   ├── index.html                 # Shell HTML com fontes e Tailwind CDN
│   ├── package.json               # Dependências React 18, Vite e TypeScript
│   ├── vite.config.ts             # Configuração do Vite dev server
│   └── src/
│       ├── App.tsx                # Painel central, métricas dos 4 tiers e botões LiquidGlass
│       ├── index.css              # Custom scrollbars e estilos base
│       └── components/
│           ├── AmberCascades.tsx  # Simulação de partículas Canvas a 60 FPS
│           └── GraphExplorer.tsx  # Visualizador de nós e ativação interativa
└── cvg/                           # Artefatos metodológicos Converge (BRD, ADRs, Task-Specs)
```

---

## 🛠 Instalação e Pré-requisitos

### Pré-requisitos
- **Python**: 3.10 ou superior
- **Node.js**: 18.0 ou superior (com npm)

### Clonando e preparando o ambiente

```bash
# Clone ou navegue para o repositório
cd memory_lab

# (Opcional) Crie e ative um ambiente virtual Python
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate
```

---

## 🚀 Como Executar

### 1. Suíte de Testes Unitários

Execute a suíte completa com os 24 testes unitários automatizados:

```bash
python -m unittest discover tests
```

*Saída esperada:*
```text
Ran 24 tests in 0.021s
OK
```

### 2. Dashboard Interativo (React + Vite)

Navegue até a pasta `frontend`, instale as dependências e inicie o servidor:

```bash
cd frontend
npm install
npm run dev
```

Abra no navegador em: **[http://localhost:5173/](http://localhost:5173/)**

No painel, você pode:
- Alternar entre as abas para inspecionar cada tier cognitivo.
- Clicar nos nós conceituais na aba **Semantic** para observar a onda de ativação espalhada e o cálculo de energia.
- Usar os botões **`+ Ingest Episode`** e **`Evict Buffer`** para testar as regras de retenção e teto de tokens em tempo real.

### 3. Servidor MCP (Model Context Protocol)

Para executar o servidor MCP interativo via entrada/saída padrão (`stdio`):

```bash
python -m memory_lab.interfaces.mcp_server
```

---

## 📖 Guia de Uso (Python SDK)

### 1. Memória Episódica (`StorageEngine`)

```python
from memory_lab.storage.engine import StorageEngine

# Inicializa banco de dados com WAL e índices FTS5
storage = StorageEngine("memory_lab.db")
storage.init_db()

# Registra um episódio de execução
episode_id = storage.record_episode(
    session_id="build-session-1",
    actor="agent-executor",
    content="Refatorado o módulo de serialização JSON com sucesso.",
    salience=0.9,
    tags="refactor,serialization,json"
)

# Recupera episódios ordenados cronologicamente
episodes = storage.get_episodes_by_session("build-session-1")
for ep in episodes:
    print(f"[{ep['actor']}] {ep['content']} (Saliência: {ep['salience']})")
```

### 2. Memória Semântica (`SemanticGraph`)

```python
from memory_lab.cognitive.semantic import SemanticGraph

graph = SemanticGraph("memory_lab.db")

# Criação de conceitos
graph.add_concept("Python", {"category": "language"})
graph.add_concept("SQLite", {"category": "database"})
graph.add_concept("WAL", {"category": "journal_mode"})

# Criação de arestas relacionais ponderadas
graph.link("Python", "SQLite", weight=0.85)
graph.link("SQLite", "WAL", weight=0.95)

# Consulta com Spreading Activation (ativação espalhada)
# Dispara a partir de 'Python' e descobre vizinhos associados
activations = graph.activate("Python", decay=0.85, max_hops=2)
print("Conceitos ativados por relevância:", activations)
# Exemplo de saída: {'Python': 1.0, 'SQLite': 0.7225, 'WAL': 0.583}
```

### 3. Memória de Trabalho (`WorkingMemoryBuffer`)

```python
from memory_lab.cognitive.working import WorkingMemoryBuffer

buffer = WorkingMemoryBuffer(max_tokens=4000)

# Inserção de contexto imediato
buffer.add_item("system-rules", "Contrato arquitetural imutável...", tokens=400, salience=1.0)
buffer.add_item("task-context", "Instruções do usuário...", tokens=1200, salience=0.8)

# Se itens futuros ultrapassarem 4000 tokens, o buffer
# despeja automaticamente os registros de menor saliência
print(f"Tokens em uso: {buffer.current_tokens} / {buffer.max_tokens}")
packed_prompt = buffer.pack_context()
```

### 4. Memória Procedural (`ProceduralStore`)

```python
from memory_lab.cognitive.working import ProceduralStore

procedural = ProceduralStore("memory_lab.db")

# Registra uma habilidade ou receita de execução
procedural.register_skill(
    name="executar_migracao",
    steps=["backup_db", "apply_sql", "run_smoke_test"]
)

# Reforça a habilidade após uma execução bem-sucedida (Power Law)
procedural.reinforce("executar_migracao", success=True)

skill = procedural.get_skill("executar_migracao")
print("Nível de ativação da habilidade:", skill["base_activation"])
```

### 5. Ciclo de Vida do Agente (`MemoryHook`)

```python
from memory_lab.interfaces.hook import MemoryHook

hook = MemoryHook(db_path="memory_lab.db")

# 1. ANTES do disparo do agente: compõe markdown comprimido para o prompt
context_md = hook.pre_execution_context(
    session_id="task-42",
    query="migração"
)

# 2. DEPOIS da execução: persiste o rastro e atualiza a curva de aprendizado
hook.post_execution_record(
    session_id="task-42",
    actor="claude-3-7-sonnet",
    outcome_summary="Migração concluída com 0 erros.",
    salience=0.95,
    tags="migration,success",
    skill_name="executar_migracao",
    success=True
)
```

---

## 🔌 Configuração do MCP para Agentes (Claude / Cursor)

Para expor o Memory Lab nativamente para **Claude Desktop**, **Cursor** ou qualquer cliente compatível com MCP, adicione ao seu arquivo de configuração (`claude_desktop_config.json` ou similar):

```json
{
  "mcpServers": {
    "memory-lab": {
      "command": "python",
      "args": [
        "-m",
        "memory_lab.interfaces.mcp_server"
      ],
      "cwd": "C:\\caminho\\para\\memory_lab"
    }
  }
}
```

### Ferramentas expostas pelo servidor MCP:

| Ferramenta | Descrição |
|---|---|
| `remember_episodic` | Grava um rastro de execução ou fato relevante com escore de saliência. |
| `search_semantic` | Executa busca de ativação espalhada no grafo associativo. |
| `get_working_context` | Retorna o contexto de trabalho comprimido respeitando o teto de 4.000 tokens. |
| `reinforce_procedure` | Ajusta a ativação de uma habilidade operacional segundo o histórico de execuções. |

---

## 🛡 Metodologia e Proveniência (Converge)

Este projeto foi concebido e implementado seguindo o rigor formal do **Converge Descent Pipeline** (Pass 0 ao Pass 8):

- **Pass 0 (Capture):** BRD detalhado (`cvg/docs/brd/memory-lab.md`).
- **Pass 1 (Intent):** Especificação técnica completa (`cvg/docs/tech-spec/memory-lab.md`).
- **Pass 2 (Structure):** 5 Architectural Decision Records (`cvg/docs/adrs/`).
- **Pass 3 (Decompose):** 3 Swimlanes (`core`, `interface`, `ui`) com 7 pernas PRD.
- **Pass 4 (Consensus):** Revisão adversarial cruzada resolvida com consenso unânime.
- **Pass 5 (Tasking):** 7 Task-Specs atômicas com **assinaturas criptográficas Tier 1 HMAC-SHA256-v3**.
- **Pass 7 (Bind):** Contratos de execução individuais atestados (`execution-profile.yaml`).
- **Pass 8 (Loop):** Implementação em branches isoladas, aprovação por *Exit Check* independente, conformidade com *blast radius* e aceitação formal via `taskspec accept --stamp`.

Todas as 7 tarefas atingiram o estado **`done`** com 100% de integridade verificada.

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o código-fonte para obter mais informações.
