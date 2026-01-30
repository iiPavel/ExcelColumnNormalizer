import os
import shutil
import unittest
import pandas as pd
from src.core.template import TemplateManager
from src.core.processor import ExcelProcessor

class TestCSVSupport(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_csv"
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_path = os.path.join(self.test_dir, "test.csv")
        self.data = {"ColA": [1, 2], "ColB": [3, 4], "ColC": [5, 6]}
        df = pd.DataFrame(self.data)
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_extract_template_from_csv(self):
        cols = TemplateManager.extract_from_excel(self.csv_path)
        self.assertEqual(cols, ["ColA", "ColB", "ColC"])

    def test_process_csv_file(self):
        template = ["ColC", "ColA"] # Reorder and drop ColB
        output_path = ExcelProcessor.process_file(self.csv_path, template, self.test_dir)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith("_converted.xlsx"))
        
        df_out = pd.read_excel(output_path)
        self.assertEqual(list(df_out.columns), ["ColC", "ColA"])
        self.assertEqual(df_out.iloc[0]["ColC"], 5)
        self.assertEqual(df_out.iloc[0]["ColA"], 1)

if __name__ == '__main__':
    unittest.main()
