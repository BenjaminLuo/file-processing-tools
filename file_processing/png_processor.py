from file_processor_strategy import FileProcessorStrategy
from PIL import Image
from errors import FileProcessingFailedError

class PngFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            image = Image.open(self.file_path)
            image.load()
            self.metadata.update({
                'original_format': image.format,
                # mode defines type and width of a pixel (https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes)
                'mode': image.mode,
                'width': image.width,
                'height': image.height,
            })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing {self.file_path}: {e}")
    
    
    def save(self, output_path: str = None) -> None:
        try:
            image = Image.open(self.file_path)
            
            save_path = output_path or self.file_path
            image.save(save_path)
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving to {save_path}: {e}")