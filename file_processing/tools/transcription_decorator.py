import whisper
import torch
from file_processing.tools import FileProcessorStrategy
from file_processing.tools.errors import TranscriptionProcessingError

class TranscriptionDecorator:
    def __init__(self, processor: FileProcessorStrategy) -> None:
        """Initializes the TranscriptionDecorator with a given file processor."""
        self._processor = processor

    def process(self) -> None:
        """Processes the file using the wrapped processor and then applies transcription."""
        self._processor.process()
        transcribed_text, language = self.extract_text_with_whisper()
        self._processor.metadata['text'] = transcribed_text
        self._processor.metadata['language'] = language

    def extract_text_with_whisper(self) -> str:
        """Extracts text from the file using Whisper by OpenAI.

        Returns:
            list: The extracted text, language
        """
        try:
            has_gpu = torch.cuda.is_available()
            device = 'cuda' if has_gpu else None

            text = whisper.transcribe(
                model=whisper.load_model('base', device=device),
                audio=str(self._processor.file_path),
                fp16=has_gpu
            )
            return text['text'], text['language']
        except Exception as e:
            raise TranscriptionProcessingError(
                f"Error during transcription processing: {e}")

    @property
    def file_name(self) -> str:
        """Returns the file name of the processed file."""
        return self._processor.file_name

    @property
    def metadata(self) -> dict:
        """Returns the metadata of the processed file."""
        return self._processor.metadata
