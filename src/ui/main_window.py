import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QListWidget, 
    QPlainTextEdit, QTextEdit, QProgressBar, QMessageBox,
    QSplitter, QGroupBox, QLineEdit
)
from PySide6.QtCore import Qt, QTimer
from src.core.template import TemplateManager
from src.ui.worker import ProcessingWorker
from src.core.config import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        
        self.setWindowTitle(f"Excel 列标准化工具{self.config_manager.get_title_suffix()}")
        self.resize(1000, 700)
        
        # Data
        self.files_to_process = []
        self.template_columns = []
        self.worker = None

        # Setup UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self._setup_left_panel()
        self._setup_right_panel()

        # Connect signals
        self.btn_browse_files.clicked.connect(self.browse_files)
        # self.btn_browse_folder.clicked.connect(self.browse_folder) # TODO
        self.btn_clear_files.clicked.connect(self.clear_files)
        
        self.btn_load_template.clicked.connect(self.load_template_file)
        self.btn_save_template.clicked.connect(self.save_template_file)
        self.btn_extract_template.clicked.connect(self.extract_template_from_file)
        
        self.btn_process.clicked.connect(self.start_processing)

        # Startup Log: defer logging until the event loop runs to avoid
        # QTextCursor warnings when appending to `QTextEdit` before show.
        startup_msg = self.config_manager.get_startup_message()
        if startup_msg:
            QTimer.singleShot(0, lambda: self.log(startup_msg, "INFO"))

    def _setup_left_panel(self):
        """File Selection and Logs Panel"""
        # Using a splitter for vertical resizing
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.main_layout.addWidget(panel, 1) # Stretch factor 1

        # --- File Selection Group ---
        grp_files = QGroupBox("1. 选择源文件")
        grp_layout = QVBoxLayout(grp_files)
        
        self.files_list_widget = QListWidget()
        grp_layout.addWidget(self.files_list_widget)

        btn_layout = QHBoxLayout()
        self.btn_browse_files = QPushButton("添加文件")
        self.btn_browse_folder = QPushButton("添加文件夹") # Optional feature
        self.btn_clear_files = QPushButton("清空列表")
        btn_layout.addWidget(self.btn_browse_files)
        btn_layout.addWidget(self.btn_browse_folder)
        btn_layout.addWidget(self.btn_clear_files)
        grp_layout.addLayout(btn_layout)
        
        layout.addWidget(grp_files, 2)

        # --- Output Config ---
        grp_output = QGroupBox("3. 输出设置")
        out_layout = QHBoxLayout(grp_output)
        self.edit_output_dir = QLineEdit()
        self.edit_output_dir.setPlaceholderText("选择输出目录")
        self.btn_select_output = QPushButton("...")
        self.btn_select_output.clicked.connect(self.select_output_dir)
        out_layout.addWidget(QLabel("保存至："))
        out_layout.addWidget(self.edit_output_dir)
        out_layout.addWidget(self.btn_select_output)
        layout.addWidget(grp_output)

        # --- Logs and Progress ---
        grp_logs = QGroupBox("日志与进度")
        log_layout = QVBoxLayout(grp_logs)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        
        self.progress_bar = QProgressBar()
        log_layout.addWidget(self.progress_bar)
        
        layout.addWidget(grp_logs, 1)

    def _setup_right_panel(self):
        """Template Configuration Panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.main_layout.addWidget(panel, 1)

        grp_template = QGroupBox("2. 配置列模板")
        tmpl_layout = QVBoxLayout(grp_template)
        
        tmpl_layout.addWidget(QLabel("输入列名（每行一列）："))
        self.template_edit = QPlainTextEdit()
        tmpl_layout.addWidget(self.template_edit)
        
        btn_layout = QHBoxLayout()
        self.btn_load_template = QPushButton("加载模板")
        self.btn_save_template = QPushButton("保存模板")
        self.btn_extract_template = QPushButton("从文件提取")
        btn_layout.addWidget(self.btn_load_template)
        btn_layout.addWidget(self.btn_save_template)
        tmpl_layout.addLayout(btn_layout)
        tmpl_layout.addWidget(self.btn_extract_template)
        
        layout.addWidget(grp_template)
        
        # --- Action Buttons ---
        self.btn_process = QPushButton("开始处理")
        self.btn_process.setMinimumHeight(50)
        self.btn_process.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(self.btn_process)

    # --- Logic ---

    def log(self, message, level="INFO"):
        color = "black"
        if level == "ERROR":
            color = "red"
        elif level == "SUCCESS":
            color = "green"
        self.log_output.append(f'<span style="color:{color}">[{level}] {message}</span>')

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 Excel 文件", "", "Excel 文件 (*.xlsx *.xls);;CSV 文件 (*.csv)"
        )
        if files:
            for f in files:
                if f not in self.files_to_process:
                    self.files_to_process.append(f)
                    self.files_list_widget.addItem(os.path.basename(f))
            self.log(f"添加了 {len(files)} 个文件。", "INFO")

    def clear_files(self):
        self.files_to_process = []
        self.files_list_widget.clear()
        self.log("已清空文件列表。", "INFO")

    def select_output_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.edit_output_dir.setText(d)

    def load_template_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "加载模板", "", "模板文件 (*.json *.txt)")
        if f:
            try:
                cols = TemplateManager.load_from_file(f)
                self.template_edit.setPlainText("\n".join(cols))
                self.log(f"已加载模板：{os.path.basename(f)}", "SUCCESS")
            except Exception as e:
                self.log(f"加载模板失败：{e}", "ERROR")

    def save_template_file(self):
        f, _ = QFileDialog.getSaveFileName(self, "保存模板", "", "JSON 模板 (*.json);;文本模板 (*.txt)")
        if f:
            cols = self.get_template_columns()
            if not cols:
                 QMessageBox.warning(self, "警告", "模板内容为空！")
                 return
            try:
                TemplateManager.save_to_file(f, cols)
                self.log(f"模板已保存至：{os.path.basename(f)}", "SUCCESS")
            except Exception as e:
                self.log(f"保存模板失败：{e}", "ERROR")

    def extract_template_from_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "从 Excel 提取模板", "", "Excel 文件/CSV (*.xlsx *.xls *.csv);;Excel 文件 (*.xlsx *.xls);;CSV 文件 (*.csv)")
        if f:
            try:
                cols = TemplateManager.extract_from_excel(f)
                self.template_edit.setPlainText("\n".join(cols))
                self.log(f"已从 {os.path.basename(f)} 提取了 {len(cols)} 列", "SUCCESS")
            except Exception as e:
                self.log(f"提取失败：{e}", "ERROR")

    def get_template_columns(self):
        text = self.template_edit.toPlainText().strip()
        if not text:
            return []
        return [line.strip() for line in text.split('\n') if line.strip()]

    def start_processing(self):
        if not self.files_to_process:
             QMessageBox.warning(self, "错误", "未选择任何文件！")
             return
        
        cols = self.get_template_columns()
        if not cols:
             QMessageBox.warning(self, "错误", "模板列为空！")
             return
             
        out_dir = self.edit_output_dir.text()
        if not out_dir:
            # Default to source dir of first file / converted
            first_dir = os.path.dirname(self.files_to_process[0])
            out_dir = os.path.join(first_dir, "converted")
            self.edit_output_dir.setText(out_dir)

        self.btn_process.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.worker = ProcessingWorker(self.files_to_process, cols, out_dir)
        self.worker.progress_updated.connect(self.on_progress)
        self.worker.log_message.connect(self.log)
        self.worker.finished_processing.connect(self.on_finished)
        self.worker.start()

    def on_progress(self, current, total, filename):
        self.progress_bar.setValue(int((current / total) * 100))

    def on_finished(self):
        self.btn_process.setEnabled(True)
        QMessageBox.information(self, "完成", "处理已完成！")
