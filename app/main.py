
import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Додаємо поточну директорію до шляху пошуку модулів
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
