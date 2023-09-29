from file_processor_strategy import FileProcessorStrategy
import extract_msg

class msgFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}
    
    def process(self) -> None:
        msg = extract_msg.Message(self.file_path)
        self.metadata.update({'text': msg.body})
        self.metadata.update({'subject': msg.subject})
        self.metadata.update({'date': msg.date})
        self.metadata.update({'sender': msg.sender})
        msg.close()



    def save(self, output_path: str = None) -> None:
        output_path = output_path or self.file_path
        msg_file = extract_msg.Message(self.file_path)
        msg_file.export(path=output_path)
        msg_file.close()
    