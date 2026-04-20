"""Provide ranking tools for diagnosis selection from symptom sets.

This module contains pure functions used by the diagnosis agent to score and
rank disease candidates from Medley symptom definitions.
"""

from __future__ import annotations


def jaccard_similarity(patient_symptoms: set[str], disease_symptoms: set[str]) -> float:
    """Compute Jaccard similarity between patient and disease symptom sets.

    Args:
        patient_symptoms (set[str]): Symptoms identified for one patient pattern.
        disease_symptoms (set[str]): Symptoms associated with one disease.

    Returns:
        float: Similarity score between 0 and 1.

    Example:
        >>> jaccard_similarity({'fever'}, {'fever', 'cough'})
    """
    if not patient_symptoms and not disease_symptoms:
        return 0.0
    union_size = len(patient_symptoms | disease_symptoms)
    if union_size == 0:
        return 0.0
    return len(patient_symptoms & disease_symptoms) / union_size


def rank_all_diseases(
    patient_symptoms: set[str],
    disease_symptom_map: dict[str, set[str]],
    disease_frequency: dict[str, int],
) -> list[tuple[str, float]]:
    """Rank all diseases by Jaccard score and frequency tie-break.

    Args:
        patient_symptoms (set[str]): Symptoms identified for one patient pattern.
        disease_symptom_map (dict[str, set[str]]): Disease to symptom set index.
        disease_frequency (dict[str, int]): Disease frequency counts for tie-break.

    Returns:
        list[tuple[str, float]]: Ordered disease-score pairs.

    Example:
        >>> rank_all_diseases({'fever'}, {'A': {'fever'}}, {'A': 10})
    """
    ranked = []
    for disease, symptoms in disease_symptom_map.items():
        score = jaccard_similarity(patient_symptoms, symptoms)
        ranked.append((disease, score, disease_frequency.get(disease, 0)))
    ranked.sort(key=lambda item: (item[1], item[2]), reverse=True)
    return [(disease, score) for disease, score, _ in ranked]


def rank_secondary_diseases(
    patient_symptoms: set[str],
    disease_symptom_map: dict[str, set[str]],
    disease_frequency: dict[str, int],
    min_threshold: float,
    max_threshold: float,
) -> list[str]:
    """Select secondary diagnosis candidates in a similarity score range.

    Args:
        patient_symptoms (set[str]): Symptoms identified for one patient pattern.
        disease_symptom_map (dict[str, set[str]]): Disease to symptom set index.
        disease_frequency (dict[str, int]): Disease frequency counts for tie-break.
        min_threshold (float): Minimum score inclusive.
        max_threshold (float): Maximum score exclusive.

    Returns:
        list[str]: Ordered disease names for secondary diagnosis.

    Example:
        >>> rank_secondary_diseases({'fever'}, {'A': {'fever'}}, {'A': 1}, 0.5, 0.6)
    """
    candidates = []
    for disease, symptoms in disease_symptom_map.items():
        score = jaccard_similarity(patient_symptoms, symptoms)
        if min_threshold <= score < max_threshold:
            candidates.append((disease, score, disease_frequency.get(disease, 0)))
    candidates.sort(key=lambda item: (item[1], item[2]), reverse=True)
    return [disease for disease, _, _ in candidates]
