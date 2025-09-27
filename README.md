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

## 2. Stack Tecnológico

Este projeto será desenvolvido utilizando o seguinte stack:

* **Linguagem de Programação:** `Python 3.13`
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

## 3. Metodologia e Pipeline de Análise

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
