
import json
import os
from typing import Dict, Any, List

class TemplateRepository:
    def __init__(self, templates_dir: str = "resources/templates"):
        self.templates_dir = templates_dir

    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Завантажує шаблон за назвою"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.json")

        with open(template_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_template(self, template_name: str, template_data: Dict[str, Any]):
        """Зберігає шаблон"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.json")

        with open(template_path, 'w', encoding='utf-8') as file:
            json.dump(template_data, file, indent=4, ensure_ascii=False)

    def list_templates(self) -> List[str]:
        """Повертає список доступних шаблонів"""
        if not os.path.exists(self.templates_dir):
            return []

        templates = []
        for file in os.listdir(self.templates_dir):
            if file.endswith('.json'):
                templates.append(file[:-5])  # Відкидаємо розширення .json

        return templates

    def create_default_template(self) -> Dict[str, Any]:
        """Створює шаблон за замовчуванням"""
        return {
            "meta": {
                "width": 744,
                "height": 1038,
                "dpi": 300,
                "background": "#1a1a1a",
                "grid": 25,
                "snap": 5
            },
            "items": {
                "artwork": {
                    "type": "image",
                    "pos": {"x": 112, "y": 150},
                    "size": {"w": 520, "h": 320},
                    "z": 1,
                    "locked": False,
                    "opacity": 1.0
                },
                "title": {
                    "type": "text",
                    "text": "Назва картки",
                    "pos": {"x": 60, "y": 40},
                    "font": {"family": "Montserrat", "size": 32, "bold": True},
                    "color": "#FFFFFF",
                    "text_width": 520,
                    "z": 5
                },
                "type": {
                    "type": "text",
                    "text": "UNIT",
                    "pos": {"x": 60, "y": 90},
                    "font": {"family": "Montserrat", "size": 20, "bold": True},
                    "color": "#F7D56E",
                    "z": 5
                },
                "description": {
                    "type": "text",
                    "text": "Опис здібностей, довгий текст...",
                    "pos": {"x": 60, "y": 520},
                    "font": {"family": "Montserrat", "size": 18},
                    "color": "#FFFFFF",
                    "text_width": 520,
                    "z": 5
                },
                "cost": {
                    "type": "text",
                    "text": "0",
                    "pos": {"x": 620, "y": 34},
                    "font": {"family": "Montserrat", "size": 28, "bold": True},
                    "color": "#FFFFFF",
                    "z": 6
                },
                "cost_type": {
                    "type": "text",
                    "text": "BF",
                    "pos": {"x": 620, "y": 74},
                    "font": {"family": "Montserrat", "size": 20},
                    "color": "#F7D56E",
                    "z": 6
                },
                "stat_atk": {
                    "type": "text",
                    "text": "ATK 0",
                    "pos": {"x": 80, "y": 740},
                    "font": {"family": "Montserrat", "size": 20, "bold": True},
                    "color": "#FFFFFF",
                    "z": 6
                },
                "stat_def": {
                    "type": "text",
                    "text": "DEF 0",
                    "pos": {"x": 80, "y": 780},
                    "font": {"family": "Montserrat", "size": 20, "bold": True},
                    "color": "#FFFFFF",
                    "z": 6
                },
                "stat_stb": {
                    "type": "text",
                    "text": "STB 0",
                    "pos": {"x": 80, "y": 820},
                    "font": {"family": "Montserrat", "size": 20, "bold": True},
                    "color": "#FFFFFF",
                    "z": 6
                }
            }
        }
