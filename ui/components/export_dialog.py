
import os
from typing import List
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal
from core.models.card import Card
from core.services.renderer_service import RendererService
from core.services.export_service import ExportService
from infrastructure.renderer.card_renderer import CardRenderer
from infrastructure.storage.pdf_exporter import PDFExporter
from app.state import app_state
from app.config import config

class ExportWidget(QWidget):
    export_completed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "title": "Експорт",
                "cards": "Картки для експорту:",
                "no_cards": "Немає карток",
                "select_all": "Вибрати все",
                "deselect_all": "Скасувати вибір",
                "export_images": "Експортувати зображення",
                "export_pdf": "Експортувати PDF",
                "select_folder": "Оберіть папку для збереження",
                "success": "Успішно",
                "success_msg": "Експортовано до {path}",
                "error": "Помилка",
                "no_cards_selected": "Не вибрано жодної картки",
                "confirm_overwrite": "Перезаписати існуючі файли?"
            },
            "en": {
                "title": "Export",
                "cards": "Cards to export:",
                "no_cards": "No cards",
                "select_all": "Select All",
                "deselect_all": "Deselect All",
                "export_images": "Export Images",
                "export_pdf": "Export PDF",
                "select_folder": "Select folder to save",
                "success": "Success",
                "success_msg": "Exported to {path}",
                "error": "Error",
                "no_cards_selected": "No cards selected",
                "confirm_overwrite": "Overwrite existing files?"
            }
        }

        # Ініціалізація сервісів
        self.renderer_service = RendererService(CardRenderer())
        self.export_service = ExportService(PDFExporter())

        self.setup_ui()
        self.update_cards()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        self.cards_label = QLabel(self.strings[self.language]["cards"])
        layout.addWidget(self.cards_label)

        # Список карток
        self.cards_list = QListWidget()
        self.cards_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.cards_list)

        # Кнопки вибору
        selection_layout = QHBoxLayout()

        self.select_all_button = QPushButton(self.strings[self.language]["select_all"])
        self.select_all_button.clicked.connect(self.select_all)
        selection_layout.addWidget(self.select_all_button)

        self.deselect_all_button = QPushButton(self.strings[self.language]["deselect_all"])
        self.deselect_all_button.clicked.connect(self.deselect_all)
        selection_layout.addWidget(self.deselect_all_button)

        layout.addLayout(selection_layout)

        # Кнопки експорту
        export_layout = QHBoxLayout()

        self.export_images_button = QPushButton(self.strings[self.language]["export_images"])
        self.export_images_button.clicked.connect(self.export_images)
        export_layout.addWidget(self.export_images_button)

        self.export_pdf_button = QPushButton(self.strings[self.language]["export_pdf"])
        self.export_pdf_button.clicked.connect(self.export_pdf)
        export_layout.addWidget(self.export_pdf_button)

        layout.addLayout(export_layout)

        self.setLayout(layout)

    def update_cards(self):
        # Очищення списку
        self.cards_list.clear()

        # Додавання карток
        if app_state.current_deck:
            for card in app_state.current_deck:
                self.cards_list.addItem(card.name)
        else:
            self.cards_list.addItem(self.strings[self.language]["no_cards"])

    def select_all(self):
        for i in range(self.cards_list.count()):
            item = self.cards_list.item(i)
            item.setSelected(True)

    def deselect_all(self):
        for i in range(self.cards_list.count()):
            item = self.cards_list.item(i)
            item.setSelected(False)

    def get_selected_cards(self) -> List[Card]:
        selected_cards = []

        for i in range(self.cards_list.count()):
            item = self.cards_list.item(i)
            if item.isSelected():
                card_name = item.text()

                # Пошук картки
                if app_state.current_deck:
                    for card in app_state.current_deck:
                        if card.name == card_name:
                            selected_cards.append(card)
                            break

        return selected_cards

    def export_images(self):
        # Отримання вибраних карток
        selected_cards = self.get_selected_cards()

        if not selected_cards:
            QMessageBox.warning(
                self, 
                self.strings[self.language]["error"],
                self.strings[self.language]["no_cards_selected"]
            )
            return

        # Вибір папки для збереження
        folder = QFileDialog.getExistingDirectory(
            self, 
            self.strings[self.language]["select_folder"],
            os.path.expanduser("~")
        )

        if not folder:
            return

        # Експорт зображень
        try:
            exported_paths = []

            for card in selected_cards:
                # Рендеринг картки
                rendered_path = self.renderer_service.render_card(card)

                # Переміщення до вибраної папки
                file_name = os.path.basename(rendered_path)
                target_path = os.path.join(folder, file_name)

                # Перевірка на існуючий файл
                if os.path.exists(target_path):
                    reply = QMessageBox.question(
                        self, 
                        self.strings[self.language]["confirm_overwrite"],
                        self.strings[self.language]["confirm_overwrite"]
                    )

                    if reply != QMessageBox.Yes:
                        continue

                # Копіювання файлу
                import shutil
                shutil.copy(rendered_path, target_path)
                exported_paths.append(target_path)

            # Повідомлення про успішний експорт
            QMessageBox.information(
                self, 
                self.strings[self.language]["success"],
                self.strings[self.language]["success_msg"].format(path=folder)
            )

            # Сигнал про завершення експорту
            self.export_completed.emit(folder)

        except Exception as e:
            QMessageBox.critical(
                self, 
                self.strings[self.language]["error"],
                str(e)
            )

    def export_pdf(self):
        # Отримання вибраних карток
        selected_cards = self.get_selected_cards()

        if not selected_cards:
            QMessageBox.warning(
                self, 
                self.strings[self.language]["error"],
                self.strings[self.language]["no_cards_selected"]
            )
            return

        # Вибір файлу для збереження
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            self.strings[self.language]["select_folder"],
            os.path.expanduser("~/deck.pdf"),
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        # Рендеринг карток
        try:
            rendered_paths = []

            for card in selected_cards:
                rendered_path = self.renderer_service.render_card(card)
                rendered_paths.append(rendered_path)

            # Експорт у PDF
            pdf_path = self.export_service.export_deck_to_pdf(rendered_paths, file_path)

            # Повідомлення про успішний експорт
            QMessageBox.information(
                self, 
                self.strings[self.language]["success"],
                self.strings[self.language]["success_msg"].format(path=pdf_path)
            )

            # Сигнал про завершення експорту
            self.export_completed.emit(pdf_path)

        except Exception as e:
            QMessageBox.critical(
                self, 
                self.strings[self.language]["error"],
                str(e)
            )

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        self.cards_label.setText(self.strings[self.language]["cards"])
        self.select_all_button.setText(self.strings[self.language]["select_all"])
        self.deselect_all_button.setText(self.strings[self.language]["deselect_all"])
        self.export_images_button.setText(self.strings[self.language]["export_images"])
        self.export_pdf_button.setText(self.strings[self.language]["export_pdf"])

        # Оновлення списку
        self.update_cards()
