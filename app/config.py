
import os
import json
from typing import Any, Dict

class Config:
    def __init__(self, config_file: str = None):
        self._config = {}

        # Завантажуємо конфігурацію за замовчуванням
        self._load_default_config()

        # Якщо вказано файл конфігурації, завантажуємо його
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self._config.update(json.load(f))

    def _load_default_config(self):
        self._config = {
            "app": {
                "name": "LS_gen_01",
                "version": "1.0.0",
                "language": "uk"
            },
            "ai": {
                "model_path": "infrastructure/ai/models",
                "default_model": "RealVisXL (SDXL)",
                "default_steps": 25,
                "default_width": 664,
                "default_height": 1040
            },
            "renderer": {
                "template_path": "resources/templates",
                "output_path": "export",
                "default_dpi": 300
            },
            "ui": {
                "theme": "dark",
                "window_size": [1200, 800]
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self, config_file: str):
        with open(config_file, 'w') as f:
            json.dump(self._config, f, indent=4)

# Глобальний екземпляр конфігурації
config = Config()
