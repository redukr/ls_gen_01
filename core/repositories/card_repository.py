
import csv
import json
import os
from typing import List, Dict, Any
from core.models.card import Card, CardStats

class CardRepository:
    def __init__(self, data_dir: str = "resources/data"):
        self.data_dir = data_dir

    def _resolve_path(self, filename: str) -> str:
        """Allow both absolute paths and data-dir relative names."""

        if os.path.isabs(filename):
            return filename

        return os.path.join(self.data_dir, filename)

    def load_from_csv(self, filename: str) -> List[Card]:
        """Завантажує картки з CSV файлу"""
        cards = []
        file_path = self._resolve_path(filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                card = self._create_card_from_dict(row)
                cards.append(card)

        return cards

    def load_from_json(self, filename: str) -> List[Card]:
        """Завантажує картки з JSON файлу"""
        cards = []
        file_path = self._resolve_path(filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            card_data = data.get('cards', [])

            for row in card_data:
                card = self._create_card_from_dict(row)
                cards.append(card)

        return cards

    def save_to_csv(self, cards: List[Card], filename: str):
        """Зберігає картки у CSV файл"""
        file_path = self._resolve_path(filename)

        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['name', 'type', 'cost', 'cost_type', 'atk', 'def', 'stb', 'init', 'rng', 'move', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for card in cards:
                writer.writerow(self._card_to_dict(card))

    def save_to_json(self, cards: List[Card], filename: str, deck_color: str = "#7B1F1F"):
        """Зберігає картки у JSON файл"""
        file_path = self._resolve_path(filename)

        data = {
            'deck_color': deck_color,
            'cards': [self._card_to_dict(card) for card in cards]
        }

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _create_card_from_dict(self, data: Dict[str, Any]) -> Card:
        """Створює об'єкт Card зі словника"""
        stats = None
        if data.get('atk') is not None:
            stats = CardStats(
                atk=int(data.get('atk', 0)),
                defense=int(data.get('def', 0)),
                stb=int(data.get('stb', 0)),
                init=int(data.get('init', 0)),
                rng=int(data.get('rng', 0)),
                move=int(data.get('move', 0))
            )

        return Card(
            name=data.get('name', ''),
            type=data.get('type', ''),
            cost=int(data.get('cost', 0)),
            cost_type=data.get('cost_type', ''),
            stats=stats,
            description=data.get('description', '')
        )

    def _card_to_dict(self, card: Card) -> Dict[str, Any]:
        """Перетворює об'єкт Card у словник"""
        data = {
            'name': card.name,
            'type': card.type,
            'cost': card.cost,
            'cost_type': card.cost_type,
            'description': card.description
        }

        if card.stats:
            data.update({
                'atk': card.stats.atk,
                'def': card.stats.defense,
                'stb': card.stats.stb,
                'init': card.stats.init,
                'rng': card.stats.rng,
                'move': card.stats.move
            })

        return data
