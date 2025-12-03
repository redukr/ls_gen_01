
from typing import List, Optional, Callable
from core.models.card import Card
from infrastructure.ai.image_generator import ImageGenerator

class AIService:
    def __init__(self, image_generator: ImageGenerator):
        self.image_generator = image_generator

    def generate_card_image(self, card: Card, count: int = 1, is_aborted: Optional[Callable[[], bool]] = None) -> List[str]:
        """Генерує зображення для картки"""
        prompt = self._create_prompt(card)
        return self.image_generator.generate_images(
            prompt=prompt,
            count=count,
            width=664,
            height=1040,
            is_aborted=is_aborted
        )

    def _create_prompt(self, card: Card) -> str:
        """Створює промпт на основі даних картки"""
        base_prompt = f"{card.name}"

        if card.is_unit():
            return f"{base_prompt}, Ukrainian Air Assault soldier. Scene must reflect this role. Style of Ukrainian graphic novel 'Воля': thick ink lines, warm muted colors, gritty cel-shading. No superheroes."
        elif card.is_tactic():
            return f"Tactical diagram for: {base_prompt}. 'Воля' style, thick lines, warm palette, simple arrows. No characters."
        elif card.is_equipment():
            return f"Ukrainian Air Assault equipment: {base_prompt}. 'Воля' style, thick lines, warm muted colors, cel-shading."
        elif card.is_event():
            return f"Military comic panel: {base_prompt}. 'Воля' style, thick lines, warm palette, gritty cel-shading."
        elif card.is_thematic():
            return f"Airborne emblem for: {base_prompt}, in 'Воля' comic style, thick lines, warm muted palette."
        else:
            return f"{base_prompt}. Cinematic board-game art, cohesive color grading, well-defined subject, tactical atmosphere"
