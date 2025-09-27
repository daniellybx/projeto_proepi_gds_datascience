# Projeto Guardiões da Saúde - ProEpi [Ciência de Dados]

Repositório do projeto de Ciência de Dados para detecção de anomalias e potenciais surtos de doenças, utilizando dados do aplicativo Guardiões da Saúde (GoH) na comunidade da Universidade de Brasília (UnB).

## 1. Sobre o Projeto

A vigilância em saúde tradicional é, em grande parte, reativa. Este projeto visa construir um pipeline de dados para a detecção precoce de surtos, aplicando técnicas de Machine Learning sobre dados de vigilância participativa. O sistema irá analisar sintomas autorrelatados pela comunidade acadêmica da UnB para identificar padrões e anomalias que fujam da normalidade sazonal, servindo como um sistema de alerta para a saúde pública.

O objetivo final é desenvolver um modelo piloto capaz de revelar a "morbidade invisível" — casos que não são capturados por canais formais de notificação — e permitir intervenções mais ágeis.

**Fonte de Dados:**
* **Aplicação:** Guardiões da Saúde (GoH)
* **População:** Comunidade da Universidade de Brasília (UnB)
* **Período:** 2022 a 2024
* **Volume:** ~1.1 milhão de relatos

## 2. Estrutura do Projeto

```
projeto_proepi_gds_datascience/
├── data/                           # Dados do projeto
│   ├── raw/                       # Dados brutos (CSV, Excel, etc.)
│   ├── processed/                 # Dados processados e limpos
│   └── external/                  # Dados externos de referência
├── notebooks/                     # Jupyter Notebooks organizados por fase
│   ├── 01_eda/                   # Análise Exploratória de Dados
│   ├── 02_clustering/            # Clusterização e definição de síndromes
│   ├── 03_time_series/           # Modelagem de séries temporais
│   └── 04_anomaly_detection/     # Detecção de anomalias
├── src/                          # Código fonte Python
│   ├── data/                     # Módulos de processamento de dados
│   │   ├── data_loader.py        # Carregamento de dados
│   │   ├── data_preprocessor.py  # Pré-processamento e limpeza
│   │   └── feature_engineering.py # Engenharia de features
│   ├── models/                   # Modelos de Machine Learning
│   │   ├── clustering.py         # Modelos de clusterização
│   │   ├── time_series.py        # Modelos de séries temporais
│   │   └── anomaly_detection.py  # Detecção de anomalias
│   ├── visualization/            # Módulos de visualização
│   │   ├── plots.py              # Funções de plotagem
│   │   └── dashboards.py         # Dashboards interativos
│   └── utils/                    # Utilitários gerais
│       ├── config.py             # Configurações do projeto
│       ├── logging_config.py     # Configuração de logs
│       └── helpers.py            # Funções auxiliares
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   └── integration/              # Testes de integração
├── docs/                         # Documentação do projeto
├── reports/                      # Relatórios e resultados
├── requirements.txt              # Dependências Python
├── setup.py                      # Configuração do pacote
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

## 3. Stack Tecnológico

Este projeto será desenvolvido utilizando o seguinte stack:

* **Linguagem de Programação:** `Python 3.8+`
* **Ambiente de Desenvolvimento (IDE):** `Cursor`
* **Principais Bibliotecas:**
    * `Pandas`: Para manipulação e análise de dados.
    * `Scikit-learn`: Para pré-processamento e modelagem.
    * `Kmodes`: Para a implementação do algoritmo K-Prototype.
    * `Statsmodels`: Para análise estatística e modelos SARIMA.
    * `XGBoost`: Para modelagem de séries temporais com Gradient Boosting.
    * `TensorFlow / Keras`: Para a implementação de modelos LSTM.
    * `Prophet`: Para modelagem de séries temporais da Meta.
    * `Matplotlib` / `Seaborn`: Para visualização de dados.

## 4. Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/proepi/projeto_proepi_gds_datascience.git
cd projeto_proepi_gds_datascience
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o pacote em modo de desenvolvimento:
```bash
pip install -e .
```

### Configuração
1. Configure as variáveis de ambiente (opcional):
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

2. Configure o logging:
```python
from src.utils.logging_config import setup_logging
setup_logging()
```

## 5. Uso do Projeto

### Carregamento de Dados
```python
from src.data import DataLoader

# Carregar dados de sintomas
loader = DataLoader("data/raw")
symptoms_df = loader.load_symptoms_data("sintomas_goh.csv")
```

### Execução dos Notebooks
Os notebooks estão organizados por fase do projeto:
1. `notebooks/01_eda/` - Análise Exploratória de Dados
2. `notebooks/02_clustering/` - Clusterização e definição de síndromes
3. `notebooks/03_time_series/` - Modelagem de séries temporais
4. `notebooks/04_anomaly_detection/` - Detecção de anomalias

### Execução de Testes
```bash
# Executar todos os testes
pytest

# Executar testes específicos
pytest tests/unit/
pytest tests/integration/
```

## 6. Metodologia e Pipeline de Análise

O estudo é uma análise retrospectiva e observacional. O pipeline de processamento e análise dos dados foi estruturado nas seguintes etapas:

### Fase 1: Análise Descritiva e Pré-processamento (EDA)
* **Objetivo:** Compreender e preparar os dados.
* **Processos:**
    * Limpeza de dados: tratamento de valores ausentes e inconsistentes.
    * Análise Exploratória de Dados (EDA) para caracterizar o perfil dos usuários e a distribuição dos sintomas.
    * Engenharia de features e codificação de variáveis categóricas.

### Fase 2: Clusterização para Definição de Síndromes
* **Objetivo:** Agrupar relatos com sintomas similares para identificar síndromes potenciais (ex: síndrome gripal, gastrointestinal).
* **Algoritmo:** `K-Prototype`, ideal para lidar com datasets que contêm variáveis numéricas e categóricas.
* **Avaliação:** A qualidade e o número ideal de clusters serão validados com o `Silhouette Score`.

### Fase 3: Modelagem de Séries Temporais e Detecção de Anomalias
* **Objetivo:** Prever a incidência esperada de cada síndrome e identificar desvios significativos.
* **Processo:**
    1.  Cálculo das taxas de incidência semanais para cada síndrome, padronizadas por 100.000 habitantes.
    2.  Treinamento e avaliação de múltiplos modelos de séries temporais: `SARIMA`, `XGBoost`, `LSTM` e `Prophet`.
    3.  As métricas de avaliação incluem RMSE, R² e análise de resíduos (Ljung-Box).
    4.  Uma **anomalia** será sinalizada quando o número de casos observados em uma semana ultrapassar o limite superior do intervalo de confiança (95%) das previsões do modelo.

## 7. Contribuição

Este é um projeto da ProEpi - Guardiões da Saúde. Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- Siga o PEP 8 para estilo de código Python
- Use type hints quando possível
- Escreva testes para novas funcionalidades
- Documente funções e classes com docstrings

## 8. Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 9. Contato

- **ProEpi - Guardiões da Saúde**
- Email: contato@proepi.org.br
- Website: https://proepi.org.br

## 10. Agradecimentos

- Comunidade da Universidade de Brasília (UnB)
- Equipe do aplicativo Guardiões da Saúde
- Todos os voluntários e colaboradores do projeto
