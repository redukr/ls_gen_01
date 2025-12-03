
import json
from typing import Dict, Any, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from core.repositories.template_repository import TemplateRepository

class TemplateEditorWidget(QWidget):
    template_changed = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "title": "Редактор шаблонів",
                "name": "Назва шаблону:",
                "save": "Зберегти",
                "load": "Завантажити",
                "new": "Новий шаблон",
                "error": "Помилка",
                "success": "Успішно",
                "confirm_overwrite": "Перезаписати існуючий шаблон?",
                "no_name": "Введіть назву шаблону",
                "not_found": "Шаблон не знайдено"
            },
            "en": {
                "title": "Template Editor",
                "name": "Template name:",
                "save": "Save",
                "load": "Load",
                "new": "New Template",
                "error": "Error",
                "success": "Success",
                "confirm_overwrite": "Overwrite existing template?",
                "no_name": "Enter template name",
                "not_found": "Template not found"
            }
        }

        self.template_repository = TemplateRepository()
        self.current_template = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Назва шаблону
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel(self.strings[self.language]["name"]))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.new_button = QPushButton(self.strings[self.language]["new"])
        self.new_button.clicked.connect(self.new_template)
        buttons_layout.addWidget(self.new_button)

        self.load_button = QPushButton(self.strings[self.language]["load"])
        self.load_button.clicked.connect(self.load_template)
        buttons_layout.addWidget(self.load_button)

        self.save_button = QPushButton(self.strings[self.language]["save"])
        self.save_button.clicked.connect(self.save_template)
        self.save_button.setEnabled(False)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def new_template(self):
        # Створення нового шаблону за замовчуванням
        self.current_template = self.template_repository.create_default_template()

        # Оновлення UI
        self.name_edit.clear()
        self.save_button.setEnabled(True)

        # Сигнал про зміну шаблону
        self.template_changed.emit(self.current_template)

    def load_template(self):
        # Отримання назви шаблону
        template_name = self.name_edit.text()

        if not template_name:
            QMessageBox.warning(
                self, 
                self.strings[self.language]["error"],
                self.strings[self.language]["no_name"]
            )
            return

        # Завантаження шаблону
        try:
            self.current_template = self.template_repository.load_template(template_name)

            # Оновлення UI
            self.save_button.setEnabled(True)

            # Сигнал про зміну шаблону
            self.template_changed.emit(self.current_template)

        except Exception as e:
            QMessageBox.critical(
                self, 
                self.strings[self.language]["error"],
                f"{self.strings[self.language]['not_found']}: {str(e)}"
            )

    def save_template(self):
        if not self.current_template:
            return

        # Отримання назви шаблону
        template_name = self.name_edit.text()

        if not template_name:
            QMessageBox.warning(
                self, 
                self.strings[self.language]["error"],
                self.strings[self.language]["no_name"]
            )
            return

        # Перевірка на існуючий шаблон
        templates = self.template_repository.list_templates()
        if template_name in templates:
            reply = QMessageBox.question(
                self, 
                self.strings[self.language]["confirm_overwrite"],
                self.strings[self.language]["confirm_overwrite"]
            )

            if reply != QMessageBox.Yes:
                return

        # Збереження шаблону
        try:
            self.template_repository.save_template(template_name, self.current_template)

            QMessageBox.information(
                self, 
                self.strings[self.language]["success"],
                self.strings[self.language]["success"]
            )

        except Exception as e:
            QMessageBox.critical(
                self, 
                self.strings[self.language]["error"],
                str(e)
            )

    def update_template(self, template_data: Dict[str, Any]):
        if self.current_template:
            self.current_template.update(template_data)

            # Сигнал про зміну шаблону
            self.template_changed.emit(self.current_template)

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        self.name_edit.setPlaceholderText(self.strings[self.language]["name"])
        self.new_button.setText(self.strings[self.language]["new"])
        self.load_button.setText(self.strings[self.language]["load"])
        self.save_button.setText(self.strings[self.language]["save"])
