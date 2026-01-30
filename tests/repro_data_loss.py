import os
import shutil
import unittest
import pandas as pd
from src.core.processor import ExcelProcessor

class TestDataLoss(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_dataloss"
        os.makedirs(self.test_dir, exist_ok=True)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_whitespace_in_headers(self):
        """Test if trailing whitespace in headers causes data loss."""
        # Create CSV with whitespace in header "Name "
        csv_path = os.path.join(self.test_dir, "whitespace.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("Name ,Age\nAlice,30\nBob,25")
            
        # Template expects "Name" (no space)
        template = ["Name", "Age"]
        
        output_path = ExcelProcessor.process_file(csv_path, template, self.test_dir)
        df = pd.read_excel(output_path)
        
        # If "Name " != "Name", column "Name" will be empty (data loss)
        print(f"\n[Whitespace Test] Columns found: {df.columns.tolist()}")
        print(f"[Whitespace Test] Row 0: {df.iloc[0].to_dict()}")
        
        # We expect data to be present if we handle whitespace, or lost if we don't.
        # Currently the code does NOT handle it, so I expect IsNan or empty.
        self.assertFalse(pd.isna(df.iloc[0]["Name"]), "Data lost due to whitespace mismatch!")

    def test_encoding_gbk(self):
        """Test reading GBK encoded CSV (common in China)."""
        csv_path = os.path.join(self.test_dir, "gbk.csv")
        try:
            with open(csv_path, "w", encoding="gbk") as f:
                f.write("姓名,年龄\n张三,30\n李四,25")
        except UnicodeEncodeError:
            print("Skipping GBK test (system might not support it)")
            return

        template = ["姓名", "年龄"]
        
        # This might fail with UnicodeDecodeError or read garbage
        try:
            output_path = ExcelProcessor.process_file(csv_path, template, self.test_dir)
            df = pd.read_excel(output_path)
            print(f"\n[GBK Test] Columns found: {df.columns.tolist()}")
            if "姓名" in df.columns:
                 print(f"[GBK Test] Row 0: {df.iloc[0].to_dict()}")
            self.assertEqual(df.iloc[0]["姓名"], "张三", "Data corrupted due to encoding!")
        except Exception as e:
            print(f"\n[GBK Test] Failed with error: {e}")
            # We want to capture this failure
            self.fail(f"GBK processing failed: {e}")

if __name__ == '__main__':
    unittest.main()
