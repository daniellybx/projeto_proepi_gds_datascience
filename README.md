# Análise de Dados para Detecção de Anomalias em Vigilância Participativa
## Projeto Guardiões da Saúde - ProEpi

**Análise Científica para Artigo de Pesquisa**

---

## 📋 Resumo do Projeto

Este repositório contém a análise de dados completa para o artigo científico "Detecção de Anomalias em Vigilância Participativa: Uma Análise de Dados do Aplicativo Guardiões da Saúde na Universidade de Brasília". O projeto visa desenvolver e validar métodos de detecção precoce de surtos de doenças utilizando dados de vigilância participativa.

### 🎯 Objetivos da Pesquisa

1. **Análise Exploratória**: Caracterizar o perfil dos usuários e distribuição temporal/espacial dos sintomas
2. **Clusterização**: Identificar síndromes potenciais através de agrupamento de sintomas similares
3. **Diagnóstico por Agente**: Classificar combinações únicas de sintomas (ProEpi/Guardiões da Saúde) em relação ao dataset Medley Disease and symptoms 2023 usando similaridade de Jaccard
4. **Modelagem Temporal**: Desenvolver modelos preditivos para incidência esperada de síndromes
5. **Detecção de Anomalias**: Implementar sistema de alerta para desvios significativos da normalidade

### 📊 Fonte de Dados

- **Aplicação**: Guardiões da Saúde (GoH) - ProEpi
- **População**: Comunidade da Universidade de Brasília (UnB)
- **Período**: 2022-2024
- **Volume**: ~1.1 milhão de relatos de sintomas
- **Tipo**: Dados de vigilância participativa (autorrelato)

---

## 🗂️ Estrutura do Projeto

```
projeto_proepi_gds_datascience/
├── data/                           # Dados do projeto
│   ├── raw/                        # Dados brutos (CSV, Excel)
│   ├── inputs/                     # Dados de entrada (ex.: Disease and symptoms dataset)
│   ├── processed/                  # Dados processados e limpos
│   ├── results/                    # Resultados das análises
│   │   ├── clusters_outputs/       # Saídas da clusterização (notebook 02)
│   │   └── agent_outputs/          # Saídas do agente de diagnóstico (notebook 03)
│   └── external/                   # Dados externos de referência
├── notebooks/                      # Jupyter Notebooks de análise
│   ├── 01_exploratory_data_analysis.ipynb   # Análise Exploratória de Dados
│   ├── 02_clustering_syndromes.ipynb       # Clusterização para Síndromes
│   ├── 03_agent_diagnosis_surveillance.ipynb  # Diagnóstico por Agente (Jaccard + Medley)
│   ├── 04_time_series_analysis.ipynb       # Análise de Séries Temporais
│   ├── tabelas/                    # Tabelas de resultados
│   └── graficos/                   # Gráficos e visualizações
├── models/                         # Modelos treinados e scripts
│   ├── trained/                    # Modelos salvos (.pkl, .joblib)
│   │   ├── clustering_models/
│   │   ├── time_series_models/
│   │   └── anomaly_detection_models/
│   └── scripts/                    # Scripts para treinar modelos
│       ├── train_clustering.py
│       └── train_time_series.py
├── scripts/                        # Scripts auxiliares do projeto
│   ├── setup_environment.py       # Configuração do ambiente (GPU, logging, paths)
│   └── create_presentation.py     # Geração de apresentação a partir dos notebooks
├── src/                            # Código fonte Python
│   ├── data/                       # Carregamento e processamento de dados (DataLoader)
│   └── utils/                      # Utilitários (config, environment, logging, helpers)
├── requirements.txt                # Dependências Python
├── setup.py                        # Configuração do pacote
├── env.example                     # Exemplo de variáveis de ambiente
└── README.md                       # Este arquivo
```

---

## 🔬 Metodologia Científica

### Fase 1: Análise Exploratória de Dados (EDA)
- **Objetivo**: Compreender características dos dados e qualidade
- **Processos**:
  - Limpeza e tratamento de valores ausentes
  - Análise descritiva de variáveis
  - Análise temporal e espacial
  - Identificação de padrões e outliers

### Fase 2: Clusterização para Definição de Síndromes
- **Objetivo**: Agrupar sintomas similares em síndromes
- **Algoritmo**: K-Prototype (dados mistos numéricos/categóricos)
- **Validação**: Silhouette Score e análise de estabilidade
- **Output**: Definição de síndromes para análise temporal (ex.: `clusters_outputs_dataset_sintomas_grupos.xlsx`)

### Fase 3: Diagnóstico por Agente (Agent Diagnosis)
- **Objetivo**: Classificar combinações únicas de sintomas em relação a um dataset de referência de doenças
- **Referência**: Medley Disease and symptoms dataset 2023 (773 doenças, 377 sintomas)
- **Método**: Similaridade de Jaccard entre sintomas (PT-BR) e dataset em inglês; mapeamento de nomes de sintomas
- **Ferramentas**: Diagnóstico primário (melhor match; se ≥60%); diagnósticos secundários (matches 50–59% quando primário ≥60%)
- **Output**: Planilhas classificadas em `data/results/agent_outputs/`

### Fase 4: Modelagem de Séries Temporais
- **Objetivo**: Prever incidência esperada de cada síndrome
- **Modelos**: SARIMA, XGBoost, LSTM, Prophet
- **Métricas**: RMSE, R², Ljung-Box test
- **Validação**: Time series cross-validation

### Fase 5: Detecção de Anomalias
- **Objetivo**: Identificar desvios significativos da normalidade
- **Critério**: Casos observados > limite superior do IC 95%
- **Output**: Sistema de alerta para surtos potenciais

---

## 🛠️ Stack Tecnológico

### Linguagens e Ambientes
- **Python 3.8+**: Linguagem principal
- **Jupyter Notebooks**: Análise interativa
- **Git**: Controle de versão

### Bibliotecas Principais
- **Análise de Dados**: `pandas`, `numpy`, `openpyxl`
- **Machine Learning e Séries Temporais**: `scikit-learn`, `xgboost`, `statsmodels`, `flaml` (AutoML e previsão temporal)
- **Visualização**: `matplotlib`
- **Agentes e embeddings** (opcional): `langchain`, `langchain-community`, `langchain-huggingface`, `langchain-chroma`, `chromadb`, `sentence-transformers`, `ollama`, `pypdf`

---

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Git
- 8GB+ RAM recomendado

### Instalação
```bash
# 1. Clone o repositório
git clone https://github.com/daniellybx/projeto_proepi_gds_datascience.git
cd projeto_proepi_gds_datascience

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Instale em modo desenvolvimento
pip install -e .
```

### Configuração
```bash
# Configure variáveis de ambiente (opcional)
cp env.example .env
# Edite .env com suas configurações
```

---

## 📊 Execução da Análise

### 1. Configuração do ambiente (opcional)
```bash
python scripts/setup_environment.py
```

### 2. Notebooks (ordem recomendada)
```bash
# 1. Análise Exploratória de Dados
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb

# 2. Clusterização para Síndromes
jupyter notebook notebooks/02_clustering_syndromes.ipynb

# 3. Diagnóstico por Agente (Jaccard + Medley)
jupyter notebook notebooks/03_agent_diagnosis_surveillance.ipynb

# 4. Análise de Séries Temporais
jupyter notebook notebooks/04_time_series_analysis.ipynb
```

### 3. Treinamento de modelos (scripts)
```bash
# Clusterização
python models/scripts/train_clustering.py

# Séries Temporais
python models/scripts/train_time_series.py
```

### 4. Geração de apresentação (opcional)
```bash
# Gera PowerPoint a partir dos notebooks de clustering e séries temporais
python scripts/create_presentation.py
```

---

## 📈 Resultados Esperados

### Produtos da Análise
1. **Modelos Treinados**: Arquivos `.pkl` salvos em `models/trained/`
2. **Gráficos**: Visualizações salvas em `notebooks/graficos/`
3. **Tabelas**: Resultados numéricos em `notebooks/tabelas/`
4. **Notebooks**: Análises completas em `notebooks/`

### Métricas de Avaliação
- **Clusterização**: Silhouette Score, Davies-Bouldin Index
- **Séries Temporais**: RMSE, MAE, R², Ljung-Box p-value
- **Detecção**: Precision, Recall, F1-Score para anomalias

---

## 🧪 Testes

```bash
# Executar testes (quando disponíveis)
pytest
```

---

## 📝 Contribuição para Pesquisa

### Para Colaboradores
1. Crie branch seguindo padrão: `local-{máquina}-{nome}`
   - Exemplos: `local-macbook-danielly`, `local-pc-danielly`
2. Faça suas modificações
3. Commit com mensagem descritiva
4. Abra Pull Request

### Padrões de Código
- Siga PEP 8 para Python
- Use type hints
- Documente funções com docstrings
- Escreva testes para novas funcionalidades

---

## 📚 Referências e Citações

### Dados
- **Fonte**: Aplicativo Guardiões da Saúde (ProEpi)
- **Período**: 2022-2024
- **População**: Comunidade UnB

### Metodologia
- K-Prototype clustering para dados mistos
- Diagnóstico por agente: similaridade de Jaccard com Medley Disease and symptoms dataset 2023
- Múltiplos modelos de séries temporais
- Detecção de anomalias baseada em intervalos de confiança

---

## 👥 Autores e Contato

**Pesquisadora Principal:**
- **Danielly Xavier**
- Email: danielly.xavier@outlook.com
- Afiliação: ProEpi - Guardiões da Saúde

**Instituição:**
- **ProEpi - Guardiões da Saúde**
- Website: https://proepi.org.br

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---