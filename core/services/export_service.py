
from typing import List
from infrastructure.storage.pdf_exporter import PDFExporter

class ExportService:
    def __init__(self, pdf_exporter: PDFExporter):
        self.pdf_exporter = pdf_exporter

    def export_to_pdf(self, image_paths: List[str], output_path: str) -> str:
        """Експортує список зображень у PDF"""
        return self.pdf_exporter.export_images(image_paths, output_path)

    def export_deck_to_pdf(self, card_paths: List[str], output_path: str) -> str:
        """Експортує колоду карток у PDF"""
        return self.pdf_exporter.export_images(card_paths, output_path)
