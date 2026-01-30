import os
import pandas as pd
from typing import List, Optional

class ExcelProcessor:
    """Handles the reading, processing, and saving of Excel files."""

    @staticmethod
    def process_file(
        input_path: str,
        template_columns: List[str],
        output_dir: str,
        overwrite: bool = False
    ) -> str:
        """
        Processes a single Excel file to match the template columns.
        
        Args:
            input_path: Path to source Excel file.
            template_columns: List of desired columns in order.
            output_dir: Directory to save the converted file.
            overwrite: Whether to overwrite existing files.

        Returns:
            The path to the generated output file.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if not template_columns:
            raise ValueError("Template columns cannot be empty.")

        # Determine output path
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_converted.xlsx" # Always output as xlsx
        output_path = os.path.join(output_dir, output_filename)

        if not overwrite and os.path.exists(output_path):
             raise FileExistsError(f"Output file already exists: {output_path}")

        # Read Data
        # Support xlsx, xls, csv
        if input_path.lower().endswith('.csv'):
            try:
                df = pd.read_csv(input_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(input_path, encoding='gb18030')
                except UnicodeDecodeError:
                     # Final attempt/fallback
                     df = pd.read_csv(input_path, encoding='gbk')
        else:
            df = pd.read_excel(input_path)
            
        # Strip whitespace from columns to ensure matching works
        df.columns = df.columns.astype(str).str.strip()
            
        # Standardize Columns
        # This reorders existings columns, drops unknown ones if stricter logic was needed (but user said "Missing columns -> empty", 
        # usually implies we keep template cols only. Requirement: "Output file columns order must match template perfectly")
        # reindex with fill_value='' does exactly this: keeps only keys in `columns`, fills missing with ''
        df_standardized = df.reindex(columns=template_columns, fill_value='')

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Write Data
        df_standardized.to_excel(output_path, index=False)
        
        return output_path
