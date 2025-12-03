
import threading
from typing import List, Optional
from PySide6.QtCore import Signal, QObject, QThread, Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QMessageBox)
from PySide6.QtGui import QPixmap
from core.models.card import Card
from core.services.ai_service import AIService
from infrastructure.ai.image_generator import ImageGenerator
from infrastructure.ai.model_loader import ModelLoader
from app.state import app_state

class AIWorker(QObject):
    finished = Signal(list)
    progress = Signal(int)
    error = Signal(str)

    def __init__(self, ai_service: AIService, card: Card, count: int):
        super().__init__()
        self.ai_service = ai_service
        self.card = card
        self.count = count
        self.abort_event = threading.Event()

    def run(self):
        try:
            images = []
            for i in range(self.count):
                if self.abort_event.is_set():
                    break

                # Генерація одного зображення
                image_paths = self.ai_service.generate_card_image(
                    self.card, 1, self.abort_event.is_set
                )

                if image_paths:
                    images.extend(image_paths)
                    self.progress.emit(i + 1)

            self.finished.emit(images)
        except Exception as e:
            self.error.emit(str(e))

    def abort(self):
        self.abort_event.set()

class AIGeneratorWidget(QWidget):
    image_generated = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "uk"
        self.strings = {
            "uk": {
                "title": "Генератор ШІ",
                "name": "Назва картки:",
                "type": "Тип:",
                "count": "Кількість:",
                "model": "Модель:",
                "generate": "Згенерувати",
                "abort": "Перервати",
                "preview": "Попередній перегляд:",
                "no_image": "Немає зображення",
                "success": "Готово",
                "success_msg": "Згенеровано {count} зображень",
                "error": "Помилка",
                "aborted": "Перервано",
                "aborted_msg": "Генерацію перервано після {count} зображень"
            },
            "en": {
                "title": "AI Generator",
                "name": "Card name:",
                "type": "Type:",
                "count": "Count:",
                "model": "Model:",
                "generate": "Generate",
                "abort": "Abort",
                "preview": "Preview:",
                "no_image": "No image",
                "success": "Done",
                "success_msg": "Generated {count} images",
                "error": "Error",
                "aborted": "Aborted",
                "aborted_msg": "Generation aborted after {count} images"
            }
        }

        self.setup_ui()
        self.setup_services()

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

        # Кількість
        self.count_edit = QLineEdit("1")
        layout.addWidget(QLabel(self.strings[self.language]["count"]))
        layout.addWidget(self.count_edit)

        # Модель
        self.model_combo = QComboBox()
        layout.addWidget(QLabel(self.strings[self.language]["model"]))
        layout.addWidget(self.model_combo)

        # Кнопки
        self.generate_button = QPushButton(self.strings[self.language]["generate"])
        self.generate_button.clicked.connect(self.generate_images)
        layout.addWidget(self.generate_button)

        self.abort_button = QPushButton(self.strings[self.language]["abort"])
        self.abort_button.clicked.connect(self.abort_generation)
        self.abort_button.setEnabled(False)
        layout.addWidget(self.abort_button)

        # Попередній перегляд
        self.preview_label = QLabel(self.strings[self.language]["preview"])
        self.preview_image = QLabel(self.strings[self.language]["no_image"])
        self.preview_image.setMinimumSize(256, 256)
        self.preview_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.preview_image)

        self.setLayout(layout)

    def setup_services(self):
        # Ініціалізація сервісів
        model_loader = ModelLoader()
        self.ai_service = AIService(ImageGenerator())

        # Заповнення списку моделей
        models = model_loader.get_available_models()
        for model_name in models.keys():
            self.model_combo.addItem(model_name)

        # Поточний потік
        self.worker = None
        self.worker_thread = None

    def generate_images(self):
        # Отримання даних з UI
        name = self.name_edit.text()
        card_type = self.type_combo.currentText()

        try:
            count = int(self.count_edit.text())
        except ValueError:
            QMessageBox.warning(self, self.strings[self.language]["error"], 
                          "Кількість має бути числом")
            return

        # Створення картки
        card = Card(
            name=name,
            type=card_type,
            cost=1,
            cost_type="BF"
        )

        # Налаштування UI
        self.generate_button.setEnabled(False)
        self.abort_button.setEnabled(True)

        # Створення та запуск потоку
        self.worker_thread = QThread()
        self.worker = AIWorker(self.ai_service, card, count)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.progress.connect(self.on_progress)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def abort_generation(self):
        if self.worker:
            self.worker.abort()

    def on_generation_finished(self, image_paths: List[str]):
        # Оновлення UI
        self.generate_button.setEnabled(True)
        self.abort_button.setEnabled(False)

        # Збереження зображень у стані
        for path in image_paths:
            app_state.add_generated_image(path)

        # Оновлення попереднього перегляду
        if image_paths:
            pixmap = QPixmap(image_paths[0])
            self.preview_image.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

        # Повідомлення про успішне завершення
        QMessageBox.information(
            self, 
            self.strings[self.language]["success"],
            self.strings[self.language]["success_msg"].format(count=len(image_paths))
        )

        # Сигнал про завершення генерації
        self.image_generated.emit(image_paths)

        # Очищення потоку
        self.worker = None
        self.worker_thread = None

    def on_progress(self, current: int):
        # Можна додати індикатор прогресу
        pass

    def on_error(self, error_msg: str):
        # Оновлення UI
        self.generate_button.setEnabled(True)
        self.abort_button.setEnabled(False)

        # Повідомлення про помилку
        QMessageBox.critical(
            self, 
            self.strings[self.language]["error"],
            error_msg
        )

        # Очищення потоку
        self.worker = None
        self.worker_thread = None

    def set_language(self, language: str):
        if language not in self.strings:
            return

        self.language = language

        # Оновлення текстів
        # (Тут потрібно оновити всі тексти у віджетах)
