import json
import os
from typing import List

class TemplateManager:
    """Manages the loading, saving, and parsing of column templates."""

    @staticmethod
    def load_from_file(file_path: str) -> List[str]:
        """Loads a list of columns from a JSON or TXT file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Template file not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [str(item) for item in data]
                else:
                    raise ValueError("JSON template must be a list of strings.")
        else:
            # Assume TXT, one column per line
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]

    @staticmethod
    def save_to_file(file_path: str, columns: List[str]) -> None:
        """Saves a list of columns to a JSON or TXT file."""
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(columns, f, indent=4, ensure_ascii=False)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(columns))

    @staticmethod
    def extract_from_excel(file_path: str) -> List[str]:
        """Extracts column headers from an existing Excel file."""
        import pandas as pd
        # Read only the header
        if file_path.lower().endswith('.csv'):
             try:
                 df = pd.read_csv(file_path, nrows=0, encoding='utf-8')
             except UnicodeDecodeError:
                 df = pd.read_csv(file_path, nrows=0, encoding='gb18030')
        else:
             df = pd.read_excel(file_path, nrows=0)
        
        # Strip whitespace from columns
        return [str(c).strip() for c in df.columns]
