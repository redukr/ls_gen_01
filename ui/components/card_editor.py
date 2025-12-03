
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QGridLayout,
)
from PySide6.QtCore import Signal
from core.models.card import Card, CardStats
from app.state import app_state

class CardEditorWidget(QWidget):
    card_changed = Signal(Card)
    card_saved = Signal(Card)
    edit_canceled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.editing_index: Optional[int] = None
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
        self.name_label = QLabel(self.strings[self.language]["name"])
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        # Тип картки
        self.type_combo = QComboBox()
        self.type_combo.addItems(["unit", "tactic", "equipment", "event", "thematic"])
        self.type_label = QLabel(self.strings[self.language]["type"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # Вартість
        self.cost_edit = QLineEdit()
        self.cost_label = QLabel(self.strings[self.language]["cost"])
        layout.addWidget(self.cost_label)
        layout.addWidget(self.cost_edit)

        # Тип вартості
        self.cost_type_combo = QComboBox()
        self.cost_type_combo.addItems(["BF", "MF", "GF"])
        self.cost_type_label = QLabel(self.strings[self.language]["cost_type"])
        layout.addWidget(self.cost_type_label)
        layout.addWidget(self.cost_type_combo)

        # Опис
        self.description_edit = QTextEdit()
        self.description_label = QLabel(self.strings[self.language]["description"])
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_edit)

        # Стати юніта
        self.stats_layout = QGridLayout()
        self.stats_inputs = {}
        self.stats_labels = {}
        stat_fields = [
            ("atk", "ATK"),
            ("defense", "DEF"),
            ("stb", "STB"),
            ("init", "INIT"),
            ("rng", "RNG"),
            ("move", "MOVE"),
        ]

        for row, (field_name, label_key) in enumerate(stat_fields):
            label = QLabel(label_key + ":")
            edit = QLineEdit()
            edit.setPlaceholderText("0")
            self.stats_layout.addWidget(label, row, 0)
            self.stats_layout.addWidget(edit, row, 1)
            self.stats_inputs[field_name] = edit
            self.stats_labels[field_name] = label

        layout.addLayout(self.stats_layout)

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
        stats = CardStats(
            atk=int(self.stats_inputs["atk"].text() or 0),
            defense=int(self.stats_inputs["defense"].text() or 0),
            stb=int(self.stats_inputs["stb"].text() or 0),
            init=int(self.stats_inputs["init"].text() or 0),
            rng=int(self.stats_inputs["rng"].text() or 0),
            move=int(self.stats_inputs["move"].text() or 0),
        )

        card = Card(
            name=self.name_edit.text(),
            type=self.type_combo.currentText(),
            cost=int(self.cost_edit.text() or "0"),
            cost_type=self.cost_type_combo.currentText(),
            description=self.description_edit.toPlainText(),
            stats=stats,
        )

        # Оновлення стану додатку
        if self.editing_index is not None and 0 <= self.editing_index < len(app_state.current_deck):
            app_state.current_deck[self.editing_index] = card
        else:
            app_state.add_card(card)
            self.editing_index = len(app_state.current_deck) - 1

        app_state.select_card(card)

        # Сигнали про зміну/збереження картки
        self.card_changed.emit(card)
        self.card_saved.emit(card)

    def reset_form(self):
        # Очищення форми
        self.name_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.cost_edit.clear()
        self.cost_type_combo.setCurrentIndex(0)
        self.description_edit.clear()
        for edit in self.stats_inputs.values():
            edit.clear()
        self.editing_index = None
        self.edit_canceled.emit()

    def load_card(self, card: Optional[Card]):
        if card is None:
            self.reset_form()
            return

        # Завантаження даних картки у форму
        self.name_edit.setText(card.name)
        self.type_combo.setCurrentText(card.type)
        self.cost_edit.setText(str(card.cost))
        self.cost_type_combo.setCurrentText(card.cost_type)
        self.description_edit.setPlainText(card.description)
        if card.stats:
            self.stats_inputs["atk"].setText(str(card.stats.atk))
            self.stats_inputs["defense"].setText(str(card.stats.defense))
            self.stats_inputs["stb"].setText(str(card.stats.stb))
            self.stats_inputs["init"].setText(str(card.stats.init))
            self.stats_inputs["rng"].setText(str(card.stats.rng))
            self.stats_inputs["move"].setText(str(card.stats.move))

        if card in app_state.current_deck:
            self.editing_index = app_state.current_deck.index(card)
        else:
            self.editing_index = None

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language
        # Оновлення текстів у віджетах
        self.name_label.setText(self.strings[self.language]["name"])
        self.type_label.setText(self.strings[self.language]["type"])
        self.cost_label.setText(self.strings[self.language]["cost"])
        self.cost_type_label.setText(self.strings[self.language]["cost_type"])
        self.description_label.setText(self.strings[self.language]["description"])
        self.save_button.setText(self.strings[self.language]["save"])
        self.cancel_button.setText(self.strings[self.language]["cancel"])

        # Статичні лейбли для статів (англійські скорочення збігаються у всіх мовах)
        for field_name, label in self.stats_labels.items():
            label.setText(label.text().split(":")[0] + ":")
