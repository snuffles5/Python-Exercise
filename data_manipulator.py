from json import JSONDecodeError
from datetime import datetime
from pathlib import Path
import json

VALID_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


class DataManipulator:
    def __init__(self, file_path: Path):
        self.processed_data: dict = {}
        if self.verify_path(file_path):
            self.file_path = file_path
            self.data = self._read_json_file()
        else:
            self.file_path = None
            self.data = {}

    def _read_json_file(self):
        with self.file_path.open(mode='r') as file:
            try:
                return json.load(file)
            except JSONDecodeError as ex:
                print(f'Bad input: {ex}')
                return {}

    def process_dict_data(self):
        processed_data = {}
        if self.data:
            for key in self.data:
                value = self.data[key]
                if type(value) == list:
                    processed_data[key] = self.manipulate_list(value)
                elif type(value) == str:
                    if date_time := self.get_date_time(value):
                        processed_data[key] = self.manipulate_date(date_time)
                    else:
                        processed_data[key] = self.manipulate_string(value)
        self.processed_data = processed_data

    def save_processed_data(self):
        if self.verify_path(self.file_path) and self.processed_data:
            output_file_path = Path(self.file_path.parent, f"{self.file_path.stem}_manip.json")
            try:
                with open(output_file_path, 'w') as file:
                    json.dump(self.processed_data, file)
                return True
            except (TypeError, ValueError, IOError, AttributeError, UnicodeEncodeError) as ex:
                print(f"Failed to save processed data: {ex}")
                return False
        else:
            print("Either path or processed data are invalid")

    @staticmethod
    def verify_path(file_path: Path):
        if not file_path:
            return False
        is_valid = True
        if not file_path.exists():
            is_valid = False
            print(f"The file '{file_path}' could not be found.")
        elif not file_path.is_file():
            print(f"'{file_path}' is not a file.")
            is_valid = False
        return is_valid

    @staticmethod
    def get_date_time(text: str):
        if text:
            try:
                return datetime.strptime(text, VALID_DATE_FORMAT)
            except ValueError:
                return None

    @staticmethod
    def manipulate_date(date_time: datetime):
        if date_time:
            new_date_time = date_time.replace(year=2021)
            return new_date_time.strftime(VALID_DATE_FORMAT)
        return None

    @staticmethod
    def manipulate_string(text: str):
        if text:
            # If the requirement was to remove all spaces (in the middle of the text) and also tab new line
            # I would change the next row to
            # new_text = ''.join(c for c in text if not c.isspace())
            new_text = text.strip()
            new_text = new_text[::-1]
            return new_text
        return None

    @staticmethod
    def manipulate_list(lst: list):
        if not lst:
            return None
        new_list = []
        for element in lst:
            if element not in new_list:
                new_list.append(element)
        return new_list


if __name__ == '__main__':
    path = "/Users/deni/Documents/Projects/Coding/Interviews/ProofPoint/python exercise example json[1][1][1].json"
    dm = DataManipulator(Path(path))
    print(dm.data)
    dm.process_dict_data()
    print(dm.data)
    print(dm.processed_data)
    dm.save_processed_data()
