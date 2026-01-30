import sys
import os
import unittest
import pandas as pd
import shutil

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.processor import ExcelProcessor
from src.core.template import TemplateManager

class TestCoreLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'tests/data'
        os.makedirs(self.test_dir, exist_ok=True)
        self.input_file = os.path.join(self.test_dir, 'input.xlsx')
        self.output_dir = os.path.join(self.test_dir, 'output')
        
        # Create a dummy excel file
        data = {
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z'],
            'OldCol': [7, 8, 9]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.input_file, index=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_processor_standardization(self):
        # Template wants A, C (missing), B
        template_columns = ['A', 'C', 'B']
        
        output_path = ExcelProcessor.process_file(
            self.input_file,
            template_columns,
            self.output_dir
        )
        
        self.assertTrue(os.path.exists(output_path))
        
        # Verify result
        df_out = pd.read_excel(output_path)
        
        # Check columns order
        self.assertEqual(list(df_out.columns), template_columns)
        
        # Check data preservation
        self.assertEqual(df_out['A'].tolist(), [1, 2, 3])
        self.assertEqual(df_out['B'].tolist(), ['x', 'y', 'z'])
        
        # Check missing column is filled (likely with NaN or empty string depending on pandas behavior with reindex and fill_value)
        # We used fill_value='' in processor
        # pandas read_excel reads empty strings as NaN by default unless keep_default_na=False
        # Let's check values directly. 
        # 3.14+ pandas stores string columns as object usually.
        
        # Verify C is empty strings (since we saved it as empty strings)
        # But read_excel might interpret them as NaN. 
        # Let's read with keep_default_na=False to check for empty strings
        df_out_raw = pd.read_excel(output_path, keep_default_na=False)
        self.assertTrue((df_out_raw['C'] == '').all())

    def test_template_manager(self):
        template_file = os.path.join(self.test_dir, 'template.json')
        cols = ['Col1', 'Col2']
        TemplateManager.save_to_file(template_file, cols)
        loaded = TemplateManager.load_from_file(template_file)
        self.assertEqual(loaded, cols)

if __name__ == '__main__':
    unittest.main()
