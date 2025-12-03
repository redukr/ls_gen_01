
import os
import json
from typing import Dict, Optional

class Translator:
    def __init__(self, locales_dir: str = "resources/locales"):
        self.locales_dir = locales_dir
        self.current_locale = "uk"
        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        """Завантажує переклади для поточної локалі"""
        locale_file = os.path.join(self.locales_dir, f"{self.current_locale}.json")

        if os.path.exists(locale_file):
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        else:
            self.translations = {}

    def set_locale(self, locale: str):
        """Встановлює поточну локаль"""
        if locale != self.current_locale:
            self.current_locale = locale
            self._load_translations()

    def translate(self, key: str, **kwargs) -> str:
        """Перекладає ключ з параметрами"""
        translation = self.translations.get(key, key)

        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation

        return translation

    def get_available_locales(self) -> Dict[str, str]:
        """Повертає список доступних локалей"""
        locales = {}

        if os.path.exists(self.locales_dir):
            for file in os.listdir(self.locales_dir):
                if file.endswith('.json'):
                    locale_name = file[:-5]  # Відкидаємо розширення .json

                    # Читаємо назву локалі з файлу
                    locale_file = os.path.join(self.locales_dir, file)
                    try:
                        with open(locale_file, 'r', encoding='utf-8') as f:
                            locale_data = json.load(f)
                            display_name = locale_data.get('_meta', {}).get('display_name', locale_name)
                            locales[locale_name] = display_name
                    except:
                        locales[locale_name] = locale_name

        return locales

    def add_translation(self, key: str, value: str):
        """Додає новий переклад"""
        self.translations[key] = value

    def save_translations(self):
        """Зберігає поточні переклади у файл"""
        locale_file = os.path.join(self.locales_dir, f"{self.current_locale}.json")

        # Створюємо директорію, якщо вона не існує
        os.makedirs(self.locales_dir, exist_ok=True)

        with open(locale_file, 'w', encoding='utf-8') as f:
            json.dump(self.translations, f, indent=4, ensure_ascii=False)

    def translate_card_type(self, card_type: str) -> str:
        """Перекладає тип картки"""
        type_key = f"card_type.{card_type}"
        return self.translate(type_key, default=card_type)

    def translate_stat_name(self, stat_name: str) -> str:
        """Перекладає назву стати"""
        stat_key = f"stat.{stat_name}"
        return self.translate(stat_key, default=stat_name)

    def translate_cost_type(self, cost_type: str) -> str:
        """Перекладає тип вартості"""
        cost_key = f"cost_type.{cost_type}"
        return self.translate(cost_key, default=cost_type)
