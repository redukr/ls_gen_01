
from typing import Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QPushButton, QMessageBox)
from PySide6.QtCore import Signal
from core.models.card import Card
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
                "confirm_delete": "Видалити картку?",
                "error": "Помилка"
            },
            "en": {
                "title": "Deck Viewer",
                "cards": "Cards:",
                "no_cards": "No cards",
                "delete": "Delete",
                "edit": "Edit",
                "confirm_delete": "Delete card?",
                "error": "Error"
            }
        }

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

        layout.addLayout(buttons_layout)

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
            # Сигнал про редагування картки
            self.card_selected.emit(card)

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

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        self.cards_label.setText(self.strings[self.language]["cards"])
        self.edit_button.setText(self.strings[self.language]["edit"])
        self.delete_button.setText(self.strings[self.language]["delete"])

        # Оновлення списку
        self.update_deck()
