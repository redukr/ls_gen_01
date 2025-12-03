
import os
from typing import List
from PIL import Image
from fpdf import FPDF

class PDFExporter:
    def __init__(self):
        self.page_width = 210  # A4 width in mm
        self.page_height = 297  # A4 height in mm
        self.margin = 10  # Margin in mm
        self.card_width = 70  # Card width in mm
        self.card_height = 100  # Card height in mm

    def export_images(self, image_paths: List[str], output_path: str) -> str:
        """Експортує список зображень у PDF"""
        pdf = FPDF()
        pdf.add_page()

        # Розрахунок кількості карток на сторінці
        cards_per_row = int((self.page_width - 2 * self.margin) / self.card_width)
        cards_per_col = int((self.page_height - 2 * self.margin) / self.card_height)
        cards_per_page = cards_per_row * cards_per_col

        for i, image_path in enumerate(image_paths):
            # Визначення позиції картки на сторінці
            page_num = i // cards_per_page
            card_num_on_page = i % cards_per_page

            row = card_num_on_page // cards_per_row
            col = card_num_on_page % cards_per_row

            x = self.margin + col * self.card_width
            y = self.margin + row * self.card_height

            # Додавання нової сторінки, якщо потрібно
            if page_num > 0 and card_num_on_page == 0:
                pdf.add_page()

            # Додавання зображення
            pdf.image(image_path, x, y, self.card_width, self.card_height)

        # Збереження PDF
        pdf.output(output_path)
        return output_path

    def export_deck_to_pdf(self, card_paths: List[str], output_path: str) -> str:
        """Експортує колоду карток у PDF"""
        pdf = FPDF()
        pdf.add_page()

        # Розрахунок кількості карток на сторінці
        cards_per_row = int((self.page_width - 2 * self.margin) / self.card_width)
        cards_per_col = int((self.page_height - 2 * self.margin) / self.card_height)
        cards_per_page = cards_per_row * cards_per_col

        for i, card_path in enumerate(card_paths):
            # Визначення позиції картки на сторінці
            page_num = i // cards_per_page
            card_num_on_page = i % cards_per_page

            row = card_num_on_page // cards_per_row
            col = card_num_on_page % cards_per_row

            x = self.margin + col * self.card_width
            y = self.margin + row * self.card_height

            # Додавання нової сторінки, якщо потрібно
            if page_num > 0 and card_num_on_page == 0:
                pdf.add_page()

            # Додавання зображення
            pdf.image(card_path, x, y, self.card_width, self.card_height)

        # Збереження PDF
        pdf.output(output_path)
        return output_path

    def export_card_backs(self, count: int, back_image_path: str, output_path: str) -> str:
        """Експортує зворотні сторони карток у PDF"""
        pdf = FPDF()
        pdf.add_page()

        # Розрахунок кількості карток на сторінці
        cards_per_row = int((self.page_width - 2 * self.margin) / self.card_width)
        cards_per_col = int((self.page_height - 2 * self.margin) / self.card_height)
        cards_per_page = cards_per_row * cards_per_col

        for i in range(count):
            # Визначення позиції картки на сторінці
            page_num = i // cards_per_page
            card_num_on_page = i % cards_per_page

            row = card_num_on_page // cards_per_row
            col = card_num_on_page % cards_per_row

            x = self.margin + col * self.card_width
            y = self.margin + row * self.card_height

            # Додавання нової сторінки, якщо потрібно
            if page_num > 0 and card_num_on_page == 0:
                pdf.add_page()

            # Додавання зображення
            pdf.image(back_image_path, x, y, self.card_width, self.card_height)

        # Збереження PDF
        pdf.output(output_path)
        return output_path
