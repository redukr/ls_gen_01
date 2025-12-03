
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Optional
from core.models.card import Card

class CardRenderer:
    def __init__(self, assets_dir: str = "resources/assets"):
        self.assets_dir = assets_dir
        self.fonts_dir = os.path.join(assets_dir, "fonts")
        self.icons_dir = os.path.join(assets_dir, "icons")
        self.frames_dir = os.path.join(assets_dir, "frames")

        # Завантажуємо шрифти
        self._load_fonts()

    def _load_fonts(self):
        """Завантажує шрифти"""
        try:
            self.font_title = ImageFont.truetype(
                os.path.join(self.fonts_dir, "LS_font.ttf"), 48
            )
            self.font_desc = ImageFont.truetype(
                os.path.join(self.fonts_dir, "LS_font.ttf"), 32
            )
            self.font_stats = ImageFont.truetype(
                os.path.join(self.fonts_dir, "LS_font.ttf"), 40
            )
        except Exception as e:
            print(f"Помилка завантаження шрифтів: {e}")
            # Використовуємо шрифт за замовчуванням
            self.font_title = ImageFont.load_default()
            self.font_desc = ImageFont.load_default()
            self.font_stats = ImageFont.load_default()

    def render(self, card: Card, template_path: Optional[str] = None) -> Image.Image:
        """Рендерить картку"""
        # Розміри полотна
        width, height = 744, 1038

        # Створюємо полотно
        card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)

        # Додаємо рамку, якщо вона є
        self._draw_frame(card)

        # Додаємо зображення, якщо воно є
        self._draw_image(card, draw)

        # Додаємо текстові елементи
        self._draw_title(card, draw)
        self._draw_description(card, draw)

        # Додаємо стати, якщо це юніт
        if card.is_unit() and card.stats:
            self._draw_stats(card, draw)

        return card

    def _draw_frame(self, card: Image.Image):
        """Додає рамку до картки"""
        frame_path = os.path.join(self.frames_dir, "base_frame.png")
        if os.path.exists(frame_path):
            frame = Image.open(frame_path).convert("RGBA")
            frame = frame.resize((card.width, card.height))
            card.alpha_composite(frame, (0, 0))

    def _draw_image(self, card: Card, draw: ImageDraw.Draw):
        """Додає зображення до картки"""
        if card.image_path and os.path.exists(card.image_path):
            art = Image.open(card.image_path).convert("RGBA")

            # Розміщення та розмір зображення
            x, y, w, h = 112, 150, 520, 320
            art = art.resize((w, h))
            card.alpha_composite(art, (x, y))

    def _draw_title(self, card: Card, draw: ImageDraw.Draw):
        """Додає заголовок до картки"""
        if card.name:
            x, y = 60, 40
            draw.text((x, y), card.name, font=self.font_title, fill=(255, 255, 255, 255))

    def _draw_description(self, card: Card, draw: ImageDraw.Draw):
        """Додає опис до картки"""
        if card.description:
            x, y = 60, 520
            draw.text((x, y), card.description, font=self.font_desc, fill=(220, 220, 220, 255))

    def _draw_stats(self, card: Card, draw: ImageDraw.Draw):
        """Додає стати до картки"""
        if not card.stats:
            return

        # Позиції для статів
        stats = [
            ("ATK", card.stats.atk, 740),
            ("DEF", card.stats.def, 780),
            ("STB", card.stats.stb, 820)
        ]

        x = 80
        for stat_name, stat_value, y in stats:
            # Малюємо іконку, якщо вона є
            icon_path = os.path.join(self.icons_dir, f"{stat_name.lower()}.png")
            if os.path.exists(icon_path):
                icon = Image.open(icon_path).convert("RGBA")
                icon = icon.resize((30, 30))
                card.alpha_composite(icon, (x, y))

            # Малюємо значення
            draw.text((x + 40, y), str(stat_value), font=self.font_stats, fill=(255, 255, 255, 255))
