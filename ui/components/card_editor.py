
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton
from PySide6.QtCore import Signal
from core.models.card import Card

class CardEditorWidget(QWidget):
    card_changed = Signal(Card)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "name": "Назва картки:",
                "type": "Тип:",
                "cost": "Вартість:",
                "cost_type": "Тип вартості:",
                "description": "Опис:",
                "save": "Зберегти",
                "cancel": "Скасувати"
            },
            "en": {
                "name": "Card name:",
                "type": "Type:",
                "cost": "Cost:",
                "cost_type": "Cost type:",
                "description": "Description:",
                "save": "Save",
                "cancel": "Cancel"
            }
        }

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Назва картки
        self.name_edit = QLineEdit()
        layout.addWidget(QLabel(self.strings[self.language]["name"]))
        layout.addWidget(self.name_edit)

        # Тип картки
        self.type_combo = QComboBox()
        self.type_combo.addItems(["unit", "tactic", "equipment", "event", "thematic"])
        layout.addWidget(QLabel(self.strings[self.language]["type"]))
        layout.addWidget(self.type_combo)

        # Вартість
        self.cost_edit = QLineEdit()
        layout.addWidget(QLabel(self.strings[self.language]["cost"]))
        layout.addWidget(self.cost_edit)

        # Тип вартості
        self.cost_type_combo = QComboBox()
        self.cost_type_combo.addItems(["BF", "MF", "GF"])
        layout.addWidget(QLabel(self.strings[self.language]["cost_type"]))
        layout.addWidget(self.cost_type_combo)

        # Опис
        self.description_edit = QTextEdit()
        layout.addWidget(QLabel(self.strings[self.language]["description"]))
        layout.addWidget(self.description_edit)

        # Кнопки
        self.save_button = QPushButton(self.strings[self.language]["save"])
        self.save_button.clicked.connect(self.save_card)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton(self.strings[self.language]["cancel"])
        self.cancel_button.clicked.connect(self.reset_form)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def save_card(self):
        # Створення картки з даних форми
        card = Card(
            name=self.name_edit.text(),
            type=self.type_combo.currentText(),
            cost=int(self.cost_edit.text() or "0"),
            cost_type=self.cost_type_combo.currentText(),
            description=self.description_edit.toPlainText()
        )

        # Сигнал про зміну картки
        self.card_changed.emit(card)

    def reset_form(self):
        # Очищення форми
        self.name_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.cost_edit.clear()
        self.cost_type_combo.setCurrentIndex(0)
        self.description_edit.clear()

    def load_card(self, card: Card):
        # Завантаження даних картки у форму
        self.name_edit.setText(card.name)
        self.type_combo.setCurrentText(card.type)
        self.cost_edit.setText(str(card.cost))
        self.cost_type_combo.setCurrentText(card.cost_type)
        self.description_edit.setPlainText(card.description)

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language
        # Оновлення текстів у віджетах
        # (Тут потрібно оновити всі тексти у віджетах)
