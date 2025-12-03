
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Signal
from ui.components.ai_generator import AIGeneratorWidget
from ui.components.card_editor import CardEditorWidget
from ui.components.deck_viewer import DeckViewerWidget
from ui.components.export_dialog import ExportWidget
from app.state import app_state
from app.config import config

class MainWindow(QMainWindow):
    language_changed = Signal(str)

    def __init__(self):
        super().__init__()

        # Налаштування вікна
        self.setWindowTitle(config.get("app.name"))
        self.setMinimumSize(800, 600)
        self.resize(config.get("ui.window_size", [1200, 800])[0], 
                     config.get("ui.window_size", [1200, 800])[1])

        # Створення центрального віджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Створення layout
        layout = QVBoxLayout(central_widget)

        # Створення вкладок
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Створення віджетів для вкладок
        self.ai_generator = AIGeneratorWidget()
        self.card_editor = CardEditorWidget()
        self.deck_viewer = DeckViewerWidget()
        self.export_widget = ExportWidget()

        # Додавання віджетів до вкладок
        self.tabs.addTab(self.ai_generator, "Генератор ШІ")
        self.tabs.addTab(self.card_editor, "Редактор карток")
        self.tabs.addTab(self.deck_viewer, "Перегляд колоди")
        self.tabs.addTab(self.export_widget, "Експорт")

        # Встановлення мови
        self.set_language(app_state.language)

    def set_language(self, language: str):
        app_state.language = language
        self.setWindowTitle(config.get("app.name"))

        # Оновлення текстів у вкладках
        if language == "uk":
            self.tabs.setTabText(0, "Генератор ШІ")
            self.tabs.setTabText(1, "Редактор карток")
            self.tabs.setTabText(2, "Перегляд колоди")
            self.tabs.setTabText(3, "Експорт")
        else:
            self.tabs.setTabText(0, "AI Generator")
            self.tabs.setTabText(1, "Card Editor")
            self.tabs.setTabText(2, "Deck Viewer")
            self.tabs.setTabText(3, "Export")

        # Повідомлення про зміну мови
        self.language_changed.emit(language)

        # Оновлення мови у віджетах
        self.ai_generator.set_language(language)
        self.card_editor.set_language(language)
        self.deck_viewer.set_language(language)
        self.export_widget.set_language(language)
