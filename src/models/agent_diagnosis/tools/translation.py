"""Provide local LLaMA-backed translation tools for diagnosis names.

This module abstracts translation behavior and falls back gracefully when
Ollama or models are unavailable.
"""

from __future__ import annotations

from typing import Iterable


class DiagnosisTranslator:
    """Translate diagnosis strings from English to Brazilian Portuguese.

    Args:
        ollama_host (str): Ollama host URL.
        preferred_models (Iterable[str]): Model preference order.

    Returns:
        None: Translator instance with internal cache.

    Example:
        >>> translator = DiagnosisTranslator('http://localhost:11434', ('llama3.2',))
    """

    def __init__(self, ollama_host: str, preferred_models: Iterable[str]):
        self.ollama_host = ollama_host
        self.preferred_models = tuple(preferred_models)
        self.cache: dict[str, str] = {}
        self.client = None
        self.model_name = None
        self.available = False
        self._bootstrap_client()

    def _bootstrap_client(self) -> None:
        """Initialize Ollama client and choose an available model.

        Args:
            None

        Returns:
            None: Internal state is updated.

        Example:
            >>> translator._bootstrap_client()
        """
        try:
            import ollama
            self.client = ollama.Client(host=self.ollama_host)
            response = self.client.list()
            models = response.get("models") or []
            names = [m.get("name") or m.get("model", "") for m in models if m.get("name") or m.get("model")]
            selected = None
            for preferred in self.preferred_models:
                for model_name in names:
                    if preferred.lower() in model_name.lower():
                        selected = model_name
                        break
                if selected:
                    break
            if not selected and names:
                selected = names[0]
            if selected:
                self.model_name = selected
                self.available = True
        except Exception:
            self.available = False

    def translate_one(self, text: str) -> str:
        """Translate one disease name from English to PT-BR.

        Args:
            text (str): Input disease name.

        Returns:
            str: Translated diagnosis name.

        Example:
            >>> translator.translate_one('dengue fever')
        """
        value = str(text or "").strip()
        if not value:
            return ""
        if value in self.cache:
            return self.cache[value]
        if not self.available or not self.client or not self.model_name:
            self.cache[value] = value
            return value
        prompt = (
            "Translate this medical diagnosis from English to Brazilian Portuguese. "
            "Return only the translated term. Keep proper nouns unchanged.\n\n"
            f"{value}"
        )
        try:
            response = self.client.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            translated = ((response.get("message") or {}).get("content") or "").strip().splitlines()[0].strip()
            if not translated:
                translated = value
        except Exception:
            translated = value
        self.cache[value] = translated
        return translated

    def translate_many(self, values: list[str]) -> list[str]:
        """Translate a sequence of diagnosis names.

        Args:
            values (list[str]): Input diagnosis names.

        Returns:
            list[str]: Translated diagnosis names in the same order.

        Example:
            >>> translator.translate_many(['dengue', 'influenza'])
        """
        return [self.translate_one(value) for value in values]
