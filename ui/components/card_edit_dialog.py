from PySide6.QtWidgets import QDialog, QVBoxLayout

from ui.components.card_editor import CardEditorWidget


class CardEditDialog(QDialog):
    """Диалогове вікно для створення та редагування карток."""

    def __init__(self, parent=None, card=None):
        super().__init__(parent)

        self.setWindowTitle("Edit card")

        layout = QVBoxLayout(self)
        self.editor = CardEditorWidget(self)
        layout.addWidget(self.editor)

        # Закриття діалогу після збереження/скасування
        self.editor.card_saved.connect(self._accept_and_close)
        self.editor.edit_canceled.connect(self.reject)

        if card:
            self.editor.load_card(card)

    def _accept_and_close(self, card):  # pylint: disable=unused-argument
        self.accept()

    def set_language(self, language: str):
        self.editor.set_language(language)
        # Назва вікна залежить від мови
        if language == "uk":
            self.setWindowTitle("Редагування картки")
        else:
            self.setWindowTitle("Card editor")
