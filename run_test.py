
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Test imports
try:
    from app.main import main
    print("✓ Successfully imported main function")
except ImportError as e:
    print(f"✗ Failed to import main function: {e}")

try:
    from ui.main_window import MainWindow
    print("✓ Successfully imported MainWindow")
except ImportError as e:
    print(f"✗ Failed to import MainWindow: {e}")

try:
    from ui.components.card_editor import CardEditorWidget
    print("✓ Successfully imported CardEditorWidget")
except ImportError as e:
    print(f"✗ Failed to import CardEditorWidget: {e}")

try:
    from ui.components.ai_generator import AIGeneratorWidget
    print("✓ Successfully imported AIGeneratorWidget")
except ImportError as e:
    print(f"✗ Failed to import AIGeneratorWidget: {e}")

try:
    from ui.components.deck_viewer import DeckViewerWidget
    print("✓ Successfully imported DeckViewerWidget")
except ImportError as e:
    print(f"✗ Failed to import DeckViewerWidget: {e}")

try:
    from ui.components.export_dialog import ExportWidget
    print("✓ Successfully imported ExportWidget")
except ImportError as e:
    print(f"✗ Failed to import ExportWidget: {e}")

try:
    from core.models.card import Card
    print("✓ Successfully imported Card model")
except ImportError as e:
    print(f"✗ Failed to import Card model: {e}")

try:
    from core.models.deck import Deck
    print("✓ Successfully imported Deck model")
except ImportError as e:
    print(f"✗ Failed to import Deck model: {e}")

print("\nTest complete!")
