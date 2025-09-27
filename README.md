# Análise de Dados para Detecção de Anomalias em Vigilância Participativa
## Projeto Guardiões da Saúde - ProEpi

**Análise Científica para Artigo de Pesquisa**

---

## 📋 Resumo do Projeto

Este repositório contém a análise de dados completa para o artigo científico "Detecção de Anomalias em Vigilância Participativa: Uma Análise de Dados do Aplicativo Guardiões da Saúde na Universidade de Brasília". O projeto visa desenvolver e validar métodos de detecção precoce de surtos de doenças utilizando dados de vigilância participativa.

### 🎯 Objetivos da Pesquisa

1. **Análise Exploratória**: Caracterizar o perfil dos usuários e distribuição temporal/espacial dos sintomas
2. **Clusterização**: Identificar síndromes potenciais através de agrupamento de sintomas similares
3. **Modelagem Temporal**: Desenvolver modelos preditivos para incidência esperada de síndromes
4. **Detecção de Anomalias**: Implementar sistema de alerta para desvios significativos da normalidade

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
│   ├── raw/                       # Dados brutos (CSV, Excel)
│   │   ├── gds-unb-ano-2024-extractionAt-20250903.csv
│   │   └── dicionario-dados-fonte-dados.xlsx
│   ├── processed/                 # Dados processados e limpos
│   └── external/                  # Dados externos de referência
├── analysis/                      # Scripts de análise por fase
│   ├── eda/                      # Análise Exploratória de Dados
│   ├── clustering/               # Clusterização e definição de síndromes
│   ├── time_series/              # Modelagem de séries temporais
│   └── anomaly_detection/        # Detecção de anomalias
├── notebooks/                     # Jupyter Notebooks de análise
│   ├── 01_exploratory_data_analysis.ipynb  # Análise Exploratória de Dados
│   ├── 02_clustering_syndromes.ipynb  # Clusterização para Síndromes
│   ├── 03_time_series_analysis.ipynb  # Análise de Séries Temporais
│   ├── tabelas/                  # Tabelas de resultados
│   └── graficos/                 # Gráficos e visualizações
├── models/                        # Modelos treinados e scripts
│   ├── trained/                  # Modelos salvos (.pkl, .joblib)
│   │   ├── clustering_models/
│   │   ├── time_series_models/
│   │   └── anomaly_detection_models/
│   └── scripts/                  # Scripts para treinar e executar modelos
│       ├── train_clustering.py
│       ├── train_time_series.py
│       └── detect_anomalies.py
├── src/                          # Código fonte Python
│   ├── data/                     # Processamento de dados
│   ├── models/                   # Implementação de modelos
│   └── utils/                    # Utilitários gerais
├── tests/                        # Testes automatizados
├── requirements.txt              # Dependências Python
├── setup.py                      # Configuração do pacote
└── README.md                     # Este arquivo
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
- **Output**: Definição de síndromes para análise temporal

### Fase 3: Modelagem de Séries Temporais
- **Objetivo**: Prever incidência esperada de cada síndrome
- **Modelos**: SARIMA, XGBoost, LSTM, Prophet
- **Métricas**: RMSE, R², Ljung-Box test
- **Validação**: Time series cross-validation

### Fase 4: Detecção de Anomalias
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
- **Análise de Dados**: `pandas`, `numpy`, `scipy`
- **Machine Learning**: `scikit-learn`, `kmodes`, `xgboost`
- **Séries Temporais**: `statsmodels`, `prophet`, `tensorflow`
- **Visualização**: `matplotlib`, `seaborn`, `plotly`
- **Processamento**: `openpyxl`, `joblib`

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

### 1. Análise Exploratória
```bash
# Execute o notebook de EDA
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### 2. Treinamento de Modelos
```bash
# Clusterização
python models/scripts/train_clustering.py

# Séries Temporais
python models/scripts/train_time_series.py

# Detecção de Anomalias
python models/scripts/detect_anomalies.py
```

### 3. Geração de Resultados
```bash
# Execute notebooks de resultados
jupyter notebook notebooks/05_results/
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
# Executar todos os testes
pytest

# Testes específicos
pytest tests/unit/
pytest tests/integration/
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

## 🙏 Agradecimentos

- Comunidade da Universidade de Brasília (UnB)
- Equipe do aplicativo Guardiões da Saúde
- Todos os voluntários que contribuíram com dados
- Colaboradores e revisores do projeto

---