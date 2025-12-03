
from typing import List, Optional
from core.models.card import Card

class AppState:
    def __init__(self):
        self.current_deck: List[Card] = []
        self.selected_card: Optional[Card] = None
        self.generated_images: List[str] = []
        self.rendered_cards: List[str] = []
        self.language = "uk"

    def add_card(self, card: Card):
        self.current_deck.append(card)

    def remove_card(self, card: Card):
        if card in self.current_deck:
            self.current_deck.remove(card)

    def select_card(self, card: Optional[Card]):
        self.selected_card = card

    def add_generated_image(self, image_path: str):
        self.generated_images.append(image_path)

    def add_rendered_card(self, card_path: str):
        self.rendered_cards.append(card_path)

    def clear_generated_images(self):
        self.generated_images.clear()

    def clear_rendered_cards(self):
        self.rendered_cards.clear()

# Глобальний екземпляр стану додатку
app_state = AppState()
