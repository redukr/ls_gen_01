
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from core.models.card import Card
from app.state import app_state

class CardPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "no_card": "Немає картки",
                "no_image": "Немає зображення"
            },
            "en": {
                "no_card": "No card",
                "no_image": "No image"
            }
        }

        self.current_card = None
        self.setup_ui()

        # Підписка на зміни стану
        app_state.selected_card = self.set_card

    def setup_ui(self):
        layout = QVBoxLayout()

        # Назва картки
        self.name_label = QLabel(self.strings[self.language]["no_card"])
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.name_label)

        # Тип картки
        self.type_label = QLabel()
        layout.addWidget(self.type_label)

        # Вартість
        self.cost_label = QLabel()
        layout.addWidget(self.cost_label)

        # Зображення картки
        self.image_label = QLabel(self.strings[self.language]["no_image"])
        self.image_label.setMinimumSize(256, 256)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        layout.addWidget(self.image_label)

        # Стати
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        # Опис
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        self.setLayout(layout)

    def set_card(self, card: Optional[Card]):
        self.current_card = card

        if card:
            # Оновлення текстових полів
            self.name_label.setText(card.name)
            self.type_label.setText(f"Тип: {card.type}")
            self.cost_label.setText(f"Вартість: {card.cost} {card.cost_type}")

            # Оновлення зображення
            if card.image_path:
                pixmap = QPixmap(card.image_path)
                self.image_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            else:
                self.image_label.setText(self.strings[self.language]["no_image"])

            # Оновлення статів
            if card.is_unit() and card.stats:
                stats_text = (
                    f"Атака: {card.stats.atk}
"
                    f"Захист: {card.stats.def}
"
                    f"Стійкість: {card.stats.stb}
"
                    f"Ініціатива: {card.stats.init}
"
                    f"Дальність: {card.stats.rng}
"
                    f"Рух: {card.stats.move}"
                )
                self.stats_label.setText(stats_text)
            else:
                self.stats_label.setText("")

            # Оновлення опису
            self.description_label.setText(card.description)
        else:
            # Очищення полів
            self.name_label.setText(self.strings[self.language]["no_card"])
            self.type_label.setText("")
            self.cost_label.setText("")
            self.image_label.setText(self.strings[self.language]["no_image"])
            self.stats_label.setText("")
            self.description_label.setText("")

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        if self.current_card:
            self.set_card(self.current_card)
        else:
            self.name_label.setText(self.strings[self.language]["no_card"])
            self.image_label.setText(self.strings[self.language]["no_image"])
