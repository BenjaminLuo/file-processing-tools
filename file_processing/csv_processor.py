from file_processor_strategy import FileProcessorStrategy
import csv
import chardet
from errors import FileProcessingFailedError

class CsvFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        try:
            encoding = chardet.detect(open(self.file_path, 'rb').read())['encoding']
            with open(self.file_path, 'r', encoding=encoding) as f:
                reader = csv.reader(f)
                rows = [row for row in reader] # List of rows, e.g. [['row', 'one'], ['row', 'two']]
                text = '\n'.join([','.join(row) for row in rows])
                num_cells = 0
                empty_cells = 0
                for row in rows:
                    for i in range(len(row)):
                        num_cells += 1
                        if row[i] == '':
                            empty_cells += 1
                self.metadata.update({
                    'text': text,
                    'encoding': encoding,
                    'num_rows': len(rows),
                    'num_cols': len(rows[0]) if rows else 0,
                    'num_cells': num_cells,
                    'empty_cells': empty_cells
                })
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while processing {self.file_path}: {e}")

    
    def save(self, output_path: str = None) -> None:
        try:
            save_path = output_path or self.file_path
            with open(save_path, 'w', encoding = self.metadata['encoding']) as f:
                writer = csv.writer(f)
                rows = self.metadata['text'].split('\n')
                for row in rows:
                    writer.writerow(row.split(','))
        except Exception as e:
            raise FileProcessingFailedError(f"Error encountered while saving file {self.file_path} to {save_path}: {e}")