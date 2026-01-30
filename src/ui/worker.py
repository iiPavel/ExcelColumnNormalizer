import os
import traceback
from PySide6.QtCore import QThread, Signal, QObject
from src.core.processor import ExcelProcessor

class ProcessingWorker(QThread):
    """
    Worker thread to process Excel files without freezing the GUI.
    """
    progress_updated = Signal(int, int, str)  # current, total, filename
    log_message = Signal(str, str)            # message, level (INFO/ERROR)
    finished_processing = Signal()

    def __init__(self, files, template_columns, output_dir, parent=None):
        super().__init__(parent)
        self.files = files
        self.template_columns = template_columns
        self.output_dir = output_dir
        self.is_running = True

    def run(self):
        total_files = len(self.files)
        success_count = 0
        error_count = 0

        self.log_message.emit(f"开始批量处理 {total_files} 个文件...", "INFO")

        for idx, file_path in enumerate(self.files):
            if not self.is_running:
                break
            
            filename = os.path.basename(file_path)
            try:
                self.log_message.emit(f"正在处理：{filename}", "INFO")
                ExcelProcessor.process_file(
                    file_path,
                    self.template_columns,
                    self.output_dir,
                    overwrite=True # Policy: default to overwrite or we could make it configurable
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                error_msg = f"处理失败 {filename}: {str(e)}"
                self.log_message.emit(error_msg, "ERROR")
                # Optional: log traceback to file or detailed log?
                # print(traceback.format_exc())

            self.progress_updated.emit(idx + 1, total_files, filename)

        self.log_message.emit(
            f"处理完成。成功：{success_count}，失败：{error_count}", 
            "INFO"
        )
        self.finished_processing.emit()

    def stop(self):
        self.is_running = False
