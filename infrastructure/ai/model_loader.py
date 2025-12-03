
import os
from typing import Dict, Tuple

class ModelLoader:
    def __init__(self, models_dir: str = "infrastructure/ai/models"):
        self.models_dir = models_dir
        self.available_models = self._discover_models()

    def _discover_models(self) -> Dict[str, str]:
        """Виявляє доступні моделі в директорії"""
        models = {}

        if not os.path.exists(self.models_dir):
            return models

        # Перевіряємо наявність відомих моделей
        realvisxl_path = os.path.join(self.models_dir, "realvisxl")
        if os.path.exists(realvisxl_path):
            models["RealVisXL (SDXL)"] = ("sdxl", realvisxl_path)

        sdxl_path = os.path.join(self.models_dir, "stable-diffusion-xl-base-1.0")
        if os.path.exists(sdxl_path):
            models["SDXL Base 1.0"] = ("sdxl", sdxl_path)

        return models

    def get_model_path(self, model_name: str) -> Tuple[str, str]:
        """Повертає тип та шлях до моделі"""
        if model_name in self.available_models:
            return self.available_models[model_name]

        # Якщо модель не знайдено, повертаємо першу доступну
        if self.available_models:
            first_model = next(iter(self.available_models.values()))
            return first_model

        raise ValueError(f"Модель '{model_name}' не знайдена")

    def get_available_models(self) -> Dict[str, str]:
        """Повертає список доступних моделей"""
        return self.available_models

    def refresh_models(self):
        """Оновлює список доступних моделей"""
        self.available_models = self._discover_models()
