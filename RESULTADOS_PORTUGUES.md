# Relatório Técnico: Vigilância Participativa e Inteligência Artificial

### Metodologia (Passo a Passo)

A metodologia deste estudo epidemiológico ecológico foi dividida nas seguintes etapas técnicas:

1.  **Tratamento e Pré-processamento de Dados:**
    *   **Fonte e Volume:** Foram processados 1.110.874 relatos da plataforma *Guardiões da Saúde* (2022-2024).
    *   **Limpeza e Integridade:** Realizou-se a tipagem de variáveis (*casting*), filtragem geográfica para o Distrito Federal e remoção de registros inconsistentes ou sem informações clínicas mínimas.
    *   **Deduplicação Lógica:** Implementou-se um agrupamento por `user_id` e janelas temporais para consolidar múltiplos relatos de um mesmo usuário em um único "evento sintomático", transformando dados brutos em uma unidade atômica individual.

2.  **Evolução da Estratégia de Classificação:**
    *   **Abordagens Estatísticas (Descartadas):** Testou-se o agrupamento multivariado (DBSCAN) e o agrupamento exclusivo por sintomas (K-Modes, LCA, Teoria de Grafos com Louvain).
    *   **Motivo da Rejeição:** Essas técnicas apresentaram **incoerência clínica**, pois aglutinavam sintomas de indivíduos diferentes em "pseudo-enfermidades", falhando em preservar a integridade do quadro clínico de cada paciente.

3.  **Classificação Individualizada via Agente de IA:**
    *   **Tecnologia:** Utilizou-se o modelo **LLaMA 3** executado localmente (Ollama) para garantir a total privacidade dos dados sensíveis.
    *   **Base de Conhecimento:** O agente utilizou o *Disease and Symptoms Dataset* (773 doenças e 377 sintomas) como referência técnica.
    *   **Cálculo de Similaridade:** O agente realizou a tradução semântica dos sintomas e aplicou o **Índice de Similaridade de Jaccard** para medir a sobreposição entre os relatos e os perfis da base de dados.
    *   **Critérios de Decisão:** Diagnósticos Primários foram definidos com similaridade $\ge$ 60% e Diagnósticos Secundários no intervalo de 50% a 59%.

4.  **Modelagem e Detecção de Surtos:**
    *   **Elegibilidade:** Apenas agravos com densidade temporal $\ge$ 0,1 (registros em >10% dos dias) e volume $\ge$ 30 semanas foram modelados.
    *   **Modelagem Preditiva:** Utilizou-se **AutoML (FLAML)** para testar competitivamente algoritmos como ARIMA, Prophet e modelos de árvore.
    *   **Protocolo de Alerta Final:** Devido à falha dos modelos preditivos complexos, adotou-se um sistema baseado em **médias móveis de 7 dias** e no limite superior do **Intervalo de Confiança de 95%** (IC95%) dos 30 dias anteriores.

### Resultados

*   **Identificação de Enfermidades:** O Agente de IA classificou **86 enfermidades distintas**, convertendo relatos não estruturados em séries temporais clinicamente fundamentadas.
*   **Filtro de Viabilidade:** Do universo inicial de patologias, apenas 16 atenderam aos critérios de densidade e volume para a tentativa de modelagem longitudinal.
*   **Desempenho do AutoML:** Todas as 16 séries modeladas via AutoML foram consideradas **inviáveis para baselines preditivas**, apresentando erros críticos (**MAPE > 100%**) e intervalos de confiança inconsistentes devido à alta descontinuidade dos dados e escassez de registros.
*   **Sucesso na Detecção de Surtos:** A estratégia de limiares estatísticos (médias móveis + IC95%) obteve êxito na detecção de **picos epidemiológicos (*spikes*)**, identificando corretamente surtos de **dengue e influenza** que ultrapassaram a variabilidade histórica calculada.