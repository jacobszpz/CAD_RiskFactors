from pathlib import Path

from record import Record

class Dataset:
    def __init__(self, directory: str | Path):
        self.patients = {}
        folder = Path(directory)
        for file_path in folder.iterdir():
            if file_path.is_file():
                pt_id = str(file_path).split('-')[0]

                if pt_id not in self.patients:
                    self.patients[pt_id] = []
                
                self.patients[pt_id].append(Record(file_path))
        print(f'Read {len(self.patients)} patients')
