# Technical Report: Participatory Surveillance and AI

### Methodology (Step-by-Step)

The methodology of this ecological epidemiological study followed these technical stages:

1.  **Data Treatment and Pre-processing:**
    *   **Source and Volume:** 1,110,874 reports from the *Guardiões da Saúde* platform (2022-2024) were processed.
    *   **Cleaning and Integrity:** Variable casting, geographical filtering for the Federal District, and removal of inconsistent records or those without minimal clinical info were performed.
    *   **Logical Deduplication:** Data were grouped by `user_id` and temporal windows to consolidate multiple reports from the same user into a single "symptomatic event," creating an individual atomic unit.

2.  **Evolution of Classification Strategy:**
    *   **Statistical Approaches (Discarded):** Multivariate clustering (DBSCAN) and symptom-only clustering (K-Modes, LCA, Louvain Graph Theory) were tested.
    *   **Reason for Rejection:** These techniques showed **clinical incoherence**, clustering symptoms from different individuals into "pseudo-diseases" and failing to preserve the clinical integrity of each patient.

3.  **Individualized Classification via AI Agent:**
    *   **Technology:** The **LLaMA 3** model was used, running locally (Ollama) to ensure full privacy of sensitive health data.
    *   **Knowledge Base:** The agent used the *Disease and Symptoms Dataset* (773 diseases and 377 symptoms) as a technical reference.
    *   **Similarity Calculation:** The agent performed semantic translation of symptoms and applied the **Jaccard Similarity Index** to measure the overlap between reports and the database profiles.
    *   **Decision Criteria:** Primary Diagnoses were defined with similarity $\ge$ 60%, and Secondary Diagnoses in the 50% to 59% range.

4.  **Modeling and Outbreak Detection:**
    *   **Eligibility:** Only conditions with temporal density $\ge$ 0.1 (records on >10% of days) and volume $\ge$ 30 weeks were modeled.
    *   **Predictive Modeling:** **AutoML (FLAML)** was used to competitively test algorithms such as ARIMA, Prophet, and tree-based models.
    *   **Final Alert Protocol:** Due to the failure of complex predictive models, a system based on **7-day moving averages** and the upper limit of the **95% Confidence Interval** (CI95%) from the previous 30 days was adopted.

### Results

*   **Disease Identification:** The AI Agent classified **86 distinct diseases**, converting unstructured reports into clinically grounded time series.
*   **Feasibility Filter:** From the initial universe of pathologies, only 16 met the density and volume criteria for longitudinal modeling attempts.
*   **AutoML Performance:** All 16 series modeled via AutoML were considered **unfeasible for predictive baselines**, showing critical errors (**MAPE > 100%**) and inconsistent confidence intervals due to high data discontinuity and scarce records.
*   **Outbreak Detection Success:** The statistical threshold strategy (moving averages + CI95%) successfully detected **epidemiological spikes**, correctly identifying **dengue and influenza** outbreaks that exceeded the calculated historical variability.
```