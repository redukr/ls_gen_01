
from infrastructure.translation.translator import Translator

class TranslationService:
    def __init__(self, translator: Translator):
        self.translator = translator

    def translate(self, text: str, from_lang: str = "uk", to_lang: str = "en") -> str:
        """Перекладає текст з однієї мови на іншу"""
        return self.translator.translate(text, from_lang, to_lang)

    def translate_card(self, card, target_lang: str = "en") -> dict:
        """Перекладає дані картки на цільову мову"""
        translated_data = {
            "name": self.translate(card.name, "uk", target_lang),
            "type": card.type,
            "cost": card.cost,
            "cost_type": card.cost_type
        }

        if card.stats:
            translated_data.update({
                "atk": card.stats.atk,
                "def": card.stats.def,
                "stb": card.stats.stb,
                "init": card.stats.init,
                "rng": card.stats.rng,
                "move": card.stats.move
            })

        if card.description:
            translated_data["description"] = self.translate(card.description, "uk", target_lang)

        return translated_data
