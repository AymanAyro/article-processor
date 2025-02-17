# gui.py

import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QTextEdit, QLineEdit, 
                            QPushButton, QFileDialog, QMessageBox, QDateEdit,
                            QProgressBar, QSplitter, QFrame, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QPalette, QColor

from agent_processor import process_article, save_files, ArticleOutput

class StyledQFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

class ProcessThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, article_text, article_date, filename, author):
        super().__init__()
        self.article_text = article_text
        self.article_date = article_date
        self.filename = filename
        self.author = author
        
    def run(self):
        try:
            result = process_article(
                article_text=self.article_text,
                article_date=self.article_date,
                filename=self.filename,
                author=self.author
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arabic Article Processor")
        self.setMinimumSize(1000, 700)
        self.selected_image_path = None
        self.setup_ui()
        self.apply_styles()
        
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
            QCheckBox {
                font-size: 13px;
            }
        """)
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Arabic Article to Markdown/JSON Converter")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("""
            color: #2c3e50;
            margin: 20px 0;
            padding: 10px;
            background-color: white;
            border-radius: 10px;
            border: 2px solid #3498db;
        """)
        main_layout.addWidget(title_label)
        
        # Input section
        input_frame = StyledQFrame()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(10)
        
        # Metadata section
        metadata_layout = QHBoxLayout()
        
        # Filename input
        filename_layout = QVBoxLayout()
        filename_label = QLabel("Output Filename:")
        filename_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter filename (without extension)")
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        metadata_layout.addLayout(filename_layout)
        
        # Author input
        author_layout = QVBoxLayout()
        author_label = QLabel("Author (optional):")
        author_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_input)
        metadata_layout.addLayout(author_layout)
        
        input_layout.addLayout(metadata_layout)
        
        # Image selection
        image_layout = QHBoxLayout()
        image_label = QLabel("Image:")
        image_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.image_path_label = QLineEdit()
        self.image_path_label.setReadOnly(True)
        self.image_path_label.setPlaceholderText("No image selected")
        select_image_button = QPushButton("Select Image")
        select_image_button.setIcon(QIcon.fromTheme("document-open"))
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_path_label)
        image_layout.addWidget(select_image_button)
        input_layout.addLayout(image_layout)
        
        # Article input
        input_label = QLabel("Article Text:")
        input_label.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout.addWidget(input_label)
        
        self.article_text = QTextEdit()
        self.article_text.setPlaceholderText("Paste your Arabic article here...")
        input_layout.addWidget(self.article_text)
        
        # Date selection
        date_layout = QHBoxLayout()
        date_label = QLabel("Article Date (optional):")
        date_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setSpecialValueText(" ")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setEnabled(False)
        
        self.use_date_checkbox = QCheckBox("Enable Date Selection")
        self.use_date_checkbox.clicked.connect(self.toggle_date)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(self.use_date_checkbox)
        date_layout.addStretch()
        input_layout.addLayout(date_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("Process Article")
        self.process_button.setIcon(QIcon.fromTheme("system-run"))
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.setEnabled(False)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        input_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(input_frame)
        
        # Output section
        output_splitter = QSplitter(Qt.Vertical)
        
        # Markdown output
        markdown_frame = StyledQFrame()
        markdown_layout = QVBoxLayout(markdown_frame)
        markdown_label = QLabel("Markdown Output:")
        markdown_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.markdown_output = QTextEdit()
        self.markdown_output.setReadOnly(True)
        markdown_layout.addWidget(markdown_label)
        markdown_layout.addWidget(self.markdown_output)
        
        # JSON output
        json_frame = StyledQFrame()
        json_layout = QVBoxLayout(json_frame)
        json_label = QLabel("JSON Output:")
        json_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.json_output = QTextEdit()
        self.json_output.setReadOnly(True)
        json_layout.addWidget(json_label)
        json_layout.addWidget(self.json_output)
        
        output_splitter.addWidget(markdown_frame)
        output_splitter.addWidget(json_frame)
        output_splitter.setSizes([300, 300])
        
        main_layout.addWidget(output_splitter)
        
        # Connect signals
        self.process_button.clicked.connect(self.process_article)
        self.save_button.clicked.connect(self.save_results)
        self.clear_button.clicked.connect(self.clear_all)
        select_image_button.clicked.connect(self.select_image)

    def toggle_date(self, checked):
        self.date_edit.setEnabled(checked)
        if not checked:
            self.date_edit.setSpecialValueText(" ")
            self.date_edit.setDate(QDate.currentDate())
    
    def select_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if image_path:
            self.selected_image_path = image_path
            self.image_path_label.setText(image_path)
            
    def process_article(self):
        article_text = self.article_text.toPlainText()
        if not article_text:
            QMessageBox.warning(self, "Warning", "Please enter article text")
            return
        
        filename = self.filename_input.text().strip()
        author = self.author_input.text().strip()
        
        # Get date only if enabled and selected
        date_str = None
        if self.use_date_checkbox.isChecked():
            date = self.date_edit.date()
            if date.isValid():
                date_str = date.toString("d MMM yyyy")
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.process_button.setEnabled(False)
        
        # Process in thread
        self.thread = ProcessThread(article_text, date_str, filename, author)
        self.thread.finished.connect(self.display_results)
        self.thread.error.connect(self.show_error)
        self.thread.start()
    
    def display_results(self, result):
        self.result = result
        
        # Show markdown result
        self.markdown_output.setText(result.markdown)
        
        # Show JSON result
        import json
        # Remove empty keys from json_metadata
        filtered_metadata = {k: v for k, v in result.json_metadata.items() if v}
        json_str = json.dumps(filtered_metadata, ensure_ascii=False, indent=2)
        self.json_output.setText(json_str)
        
        # Handle user queries if any
        if result.user_queries:
            query_text = "The following information is needed from the user:\n"
            for query in result.user_queries:
                query_text += f"- {query}\n"
            QMessageBox.information(self, "User Information Needed", query_text)
        
        self.save_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(True)
    
    def show_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(True)
    
    def save_results(self):
        if not hasattr(self, 'result'):
            return
            
        filename = self.filename_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "Warning", "Please enter a filename")
            return
            
        try:
            # Create output directory
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Handle image if selected
            if self.selected_image_path:
                # Get the file extension from the original image
                ext = Path(self.selected_image_path).suffix
                # Create the new image path using the provided filename
                new_image_name = f"{filename}{ext}"
                new_image_path = output_dir / new_image_name
                # Copy the image
                shutil.copy2(self.selected_image_path, new_image_path)
                # Update the image path in the metadata to match the new filename
                self.result.json_metadata['image'] = new_image_name
            
            # Save files
            md_path, json_path = save_files(self.result, filename)
            
            success_message = f"Files saved successfully:\nMarkdown: {md_path}\nJSON: {json_path}"
            if self.selected_image_path:
                success_message += f"\nImage: {new_image_path}"
            
            QMessageBox.information(self, "Files Saved", success_message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save files: {str(e)}")
    
    def clear_all(self):
        self.article_text.clear()
        self.markdown_output.clear()
        self.json_output.clear()
        self.filename_input.clear()
        self.image_path_label.clear()
        self.selected_image_path = None
        self.use_date_checkbox.setChecked(False)
        self.date_edit.setEnabled(False)
        self.date_edit.setSpecialValueText(" ")
        self.save_button.setEnabled(False)
        if hasattr(self, 'result'):
            del self.result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())