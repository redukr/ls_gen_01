
from typing import List
from core.models.card import Card
from infrastructure.renderer.card_renderer import CardRenderer

class RendererService:
    def __init__(self, card_renderer: CardRenderer):
        self.card_renderer = card_renderer

    def render_card(self, card: Card, template_path: str = None) -> str:
        """Рендерить картку та повертає шлях до збереженого файлу"""
        image = self.card_renderer.render(card, template_path)

        # Зберігаємо зображення
        output_path = f"export/rendered_{card.name.replace(' ', '_')}.png"
        image.save(output_path)

        return output_path

    def render_cards(self, cards: List[Card], template_path: str = None) -> List[str]:
        """Рендерить список карток та повертає шляхи до збережених файлів"""
        rendered_paths = []
        for card in cards:
            path = self.render_card(card, template_path)
            rendered_paths.append(path)
        return rendered_paths
