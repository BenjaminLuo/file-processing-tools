from file_processor_strategy import FileProcessorStrategy
from striprtf.striprtf import rtf_to_text
from errors import FileProcessingFailedError, UnsupportedFileTypeError

class RtfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            self.metadata.update({"text": rtf_to_text(file_content)})
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing {self.file_path}: {e}")


    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w') as f:
                f.write(self.metadata['text'])
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving {self.file_path}: {e}")