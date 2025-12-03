
import os
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import Signal
from core.models.card import Card
from core.repositories.card_repository import CardRepository
from ui.components.card_edit_dialog import CardEditDialog
from app.state import app_state

class DeckViewerWidget(QWidget):
    card_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "title": "Перегляд колоди",
                "cards": "Картки:",
                "no_cards": "Немає карток",
                "delete": "Видалити",
                "edit": "Редагувати",
                "add": "Додати",
                "import_json": "Імпорт JSON",
                "import_csv": "Імпорт CSV",
                "export_json": "Експорт JSON",
                "export_csv": "Експорт CSV",
                "confirm_delete": "Видалити картку?",
                "error": "Помилка",
                "success": "Успішно",
                "import_success": "Імпортовано картки з {path}",
                "export_success": "Експортовано картки до {path}",
                "no_cards_for_export": "Немає карток для експорту"
            },
            "en": {
                "title": "Deck Viewer",
                "cards": "Cards:",
                "no_cards": "No cards",
                "delete": "Delete",
                "edit": "Edit",
                "add": "Add",
                "import_json": "Import JSON",
                "import_csv": "Import CSV",
                "export_json": "Export JSON",
                "export_csv": "Export CSV",
                "confirm_delete": "Delete card?",
                "error": "Error",
                "success": "Success",
                "import_success": "Imported cards from {path}",
                "export_success": "Exported cards to {path}",
                "no_cards_for_export": "No cards to export"
            }
        }

        self.repository = CardRepository()
        self.setup_ui()
        self.update_deck()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        self.cards_label = QLabel(self.strings[self.language]["cards"])
        layout.addWidget(self.cards_label)

        # Список карток
        self.cards_list = QListWidget()
        self.cards_list.itemClicked.connect(self.on_card_selected)
        layout.addWidget(self.cards_list)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.edit_button = QPushButton(self.strings[self.language]["edit"])
        self.edit_button.clicked.connect(self.edit_card)
        self.edit_button.setEnabled(False)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton(self.strings[self.language]["delete"])
        self.delete_button.clicked.connect(self.delete_card)
        self.delete_button.setEnabled(False)
        buttons_layout.addWidget(self.delete_button)

        self.add_button = QPushButton(self.strings[self.language]["add"])
        self.add_button.clicked.connect(self.add_card)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        # Кнопки імпорту/експорту
        transfer_layout = QHBoxLayout()
        self.import_json_button = QPushButton(self.strings[self.language]["import_json"])
        self.import_json_button.clicked.connect(self.import_json)
        transfer_layout.addWidget(self.import_json_button)

        self.import_csv_button = QPushButton(self.strings[self.language]["import_csv"])
        self.import_csv_button.clicked.connect(self.import_csv)
        transfer_layout.addWidget(self.import_csv_button)

        self.export_json_button = QPushButton(self.strings[self.language]["export_json"])
        self.export_json_button.clicked.connect(self.export_json)
        transfer_layout.addWidget(self.export_json_button)

        self.export_csv_button = QPushButton(self.strings[self.language]["export_csv"])
        self.export_csv_button.clicked.connect(self.export_csv)
        transfer_layout.addWidget(self.export_csv_button)

        layout.addLayout(transfer_layout)

        self.setLayout(layout)

    def update_deck(self):
        # Очищення списку
        self.cards_list.clear()

        # Додавання карток
        if app_state.current_deck:
            for card in app_state.current_deck:
                self.cards_list.addItem(card.name)
        else:
            self.cards_list.addItem(self.strings[self.language]["no_cards"])

    def on_card_selected(self, item):
        # Отримання назви картки
        card_name = item.text()

        # Пошук картки
        card = None
        if app_state.current_deck:
            for c in app_state.current_deck:
                if c.name == card_name:
                    card = c
                    break

        # Оновлення стану
        app_state.select_card(card)

        # Оновлення UI
        self.edit_button.setEnabled(card is not None)
        self.delete_button.setEnabled(card is not None)

        # Сигнал про вибір картки
        self.card_selected.emit(card)

    def edit_card(self):
        # Отримання вибраної картки
        card = app_state.selected_card

        if card:
            dialog = CardEditDialog(self, card)
            dialog.set_language(self.language)

            if dialog.exec():
                self.update_deck()
                # Встановлюємо вибрану картку після редагування
                app_state.select_card(card)
                self.card_selected.emit(card)

    def add_card(self):
        dialog = CardEditDialog(self)
        dialog.set_language(self.language)

        if dialog.exec():
            self.update_deck()
            self.on_card_selected(self.cards_list.item(self.cards_list.count() - 1))

    def delete_card(self):
        # Отримання вибраної картки
        card = app_state.selected_card

        if not card:
            return

        # Підтвердження видалення
        reply = QMessageBox.question(
            self, 
            self.strings[self.language]["confirm_delete"],
            self.strings[self.language]["confirm_delete"],
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Видалення картки
            app_state.remove_card(card)

            # Оновлення UI
            self.update_deck()
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def import_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.strings[self.language]["import_json"],
            os.path.expanduser("~"),
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            app_state.current_deck = self.repository.load_from_json(file_path)
            app_state.select_card(None)
            self.update_deck()
            QMessageBox.information(
                self,
                self.strings[self.language]["success"],
                self.strings[self.language]["import_success"].format(path=file_path)
            )
        except Exception as exc:  # pylint: disable=broad-except
            QMessageBox.critical(self, self.strings[self.language]["error"], str(exc))

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.strings[self.language]["import_csv"],
            os.path.expanduser("~"),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            app_state.current_deck = self.repository.load_from_csv(file_path)
            app_state.select_card(None)
            self.update_deck()
            QMessageBox.information(
                self,
                self.strings[self.language]["success"],
                self.strings[self.language]["import_success"].format(path=file_path)
            )
        except Exception as exc:  # pylint: disable=broad-except
            QMessageBox.critical(self, self.strings[self.language]["error"], str(exc))

    def export_json(self):
        if not app_state.current_deck:
            QMessageBox.warning(
                self,
                self.strings[self.language]["error"],
                self.strings[self.language]["no_cards_for_export"]
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.strings[self.language]["export_json"],
            os.path.expanduser("~/deck.json"),
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            self.repository.save_to_json(app_state.current_deck, file_path)
            QMessageBox.information(
                self,
                self.strings[self.language]["success"],
                self.strings[self.language]["export_success"].format(path=file_path)
            )
        except Exception as exc:  # pylint: disable=broad-except
            QMessageBox.critical(self, self.strings[self.language]["error"], str(exc))

    def export_csv(self):
        if not app_state.current_deck:
            QMessageBox.warning(
                self,
                self.strings[self.language]["error"],
                self.strings[self.language]["no_cards_for_export"]
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.strings[self.language]["export_csv"],
            os.path.expanduser("~/deck.csv"),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            self.repository.save_to_csv(app_state.current_deck, file_path)
            QMessageBox.information(
                self,
                self.strings[self.language]["success"],
                self.strings[self.language]["export_success"].format(path=file_path)
            )
        except Exception as exc:  # pylint: disable=broad-except
            QMessageBox.critical(self, self.strings[self.language]["error"], str(exc))

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        self.cards_label.setText(self.strings[self.language]["cards"])
        self.edit_button.setText(self.strings[self.language]["edit"])
        self.delete_button.setText(self.strings[self.language]["delete"])
        self.add_button.setText(self.strings[self.language]["add"])
        self.import_json_button.setText(self.strings[self.language]["import_json"])
        self.import_csv_button.setText(self.strings[self.language]["import_csv"])
        self.export_json_button.setText(self.strings[self.language]["export_json"])
        self.export_csv_button.setText(self.strings[self.language]["export_csv"])

        # Оновлення списку
        self.update_deck()
