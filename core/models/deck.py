
from dataclasses import dataclass, field
from typing import List, Optional
from .card import Card

@dataclass
class Deck:
    name: str
    cards: List[Card] = field(default_factory=list)
    color: str = "#7B1F1F"

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)

    def get_card_by_name(self, name: str) -> Optional[Card]:
        for card in self.cards:
            if card.name == name:
                return card
        return None

    def get_cards_by_type(self, card_type: str) -> List[Card]:
        return [card for card in self.cards if card.type == card_type]

    def count(self) -> int:
        return len(self.cards)

    def count_by_type(self, card_type: str) -> int:
        return len(self.get_cards_by_type(card_type))
