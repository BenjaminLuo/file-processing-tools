import os
from txt_processor import TextFileProcessor
from pdf_processor import PdfFileProcessor
from docx_processor import DocxFileProcessor
from ocr_decorator import OCRDecorator

class File:
    OCR_APPLICABLE_EXTENSIONS = {".pdf", ".jpeg", ".png"}

    def __init__(self, path, use_ocr=False):
        self.path = path
        self.processor = self._get_processor(use_ocr)
        self.process()

    def _get_processor(self, use_ocr):
        _, extension = os.path.splitext(self.path)
        processor = None

        if extension == ".txt":
            processor = TextFileProcessor(self.path)
        elif extension == ".pdf":
            processor = PdfFileProcessor(self.path)
        elif extension == ".docx":
            processor = DocxFileProcessor(self.path)
        else:
            raise ValueError(f"No processor for file type {extension}")

        if use_ocr:
            if extension not in File.OCR_APPLICABLE_EXTENSIONS:
                raise ValueError(f"OCR is not applicable for file type {extension}.")
            return OCRDecorator(processor)
        return processor

    def process(self):
        return self.processor.process()

    @property
    def file_name(self):
        return self.processor.file_name

    @property
    def metadata(self):
        return self.processor.metadata
