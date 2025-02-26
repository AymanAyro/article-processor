import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QTextEdit, QLineEdit, 
                            QPushButton, QFileDialog, QMessageBox, QDateEdit,
                            QProgressBar, QSplitter, QFrame, QCheckBox,
                            QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QPalette, QColor, QPixmap, QFontDatabase

from agent_processor import process_article, save_files, ArticleOutput

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None, icon=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 9, QFont.Bold))
        if icon:
            self.setIcon(icon)
        self.setCursor(Qt.PointingHandCursor)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # Animation for hover effect
        self._animation = QPropertyAnimation(self, b"size")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        # Slightly increase size on hover
        self._animation.setStartValue(self.size())
        self._animation.setEndValue(QSize(int(self.width() * 1.02), int(self.height() * 1.02)))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        # Return to normal size
        self._animation.setStartValue(self.size())
        self._animation.setEndValue(QSize(int(self.width() / 1.02), int(self.height() / 1.02)))
        self._animation.start()
        super().leaveEvent(event)

class StyledQFrame(QFrame):
    def __init__(self, parent=None, shadow_enabled=True):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #EEEAE4;
                border-radius: 12px;
                border: 1px solid #DACDD3;
            }
        """)
        
        if shadow_enabled:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 40))
            shadow.setOffset(0, 4)
            self.setGraphicsEffect(shadow)

class ProcessThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, article_text, article_date, filename, author):
        super().__init__()
        self.article_text = article_text
        self.article_date = article_date
        self.filename = filename
        self.author = author
        
    def run(self):
        try:
            # Simulate progress for better UX
            for i in range(0, 101, 10):
                self.progress.emit(i)
                self.msleep(100)
                
            result = process_article(
                article_text=self.article_text,
                article_date=self.article_date,
                filename=self.filename,
                author=self.author
            )
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Article Processor")
        self.setMinimumSize(1100, 800)
        self.selected_image_path = None
        
        # Load custom fonts
        self.load_fonts()
        
        # Setup UI components
        self.setup_ui()
        self.apply_styles()
        
    def load_fonts(self):
        # This would typically load custom fonts, but for this example we'll use system fonts
        pass
        
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0E9E1;
            }
            QLabel {
                color: #2F2D2C;
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #DACDD3;
                border-radius: 8px;
                background-color: #EEEAE4;
                font-size: 13px;
                selection-background-color: #B67251;
                selection-color: #EEEAE4;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1.5px solid #B67251;
            }
            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #DACDD3;
            }
            QPushButton {
                background-color: #B67251;
                color: #EEEAE4;
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #965C3F;
            }
            QPushButton:pressed {
                background-color: #7A4C34;
            }
            QPushButton:disabled {
                background-color: #DACDD3;
                color: #2F2D2C;
            }
            QProgressBar {
                border: 1px solid #DACDD3;
                border-radius: 8px;
                text-align: center;
                height: 16px;
                color: #2F2D2C;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #B67251;
                border-radius: 7px;
            }
            QCheckBox {
                font-size: 13px;
                color: #2F2D2C;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #B67251;
            }
            QCheckBox::indicator:checked {
                background-color: #B67251;
            }
            QDateEdit {
                background-color: #EEEAE4;
                padding: 5px;
                border: 1px solid #DACDD3;
                border-radius: 8px;
            }
            QSplitter::handle {
                background-color: #DACDD3;
                height: 2px;
            }
            QScrollBar:vertical {
                border: none;
                background: #EEEAE4;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B67251;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            /* Fix for frames with layouts */
            QFrame {
                padding: 0px;
            }
        """)
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title section with logo/icon
        title_layout = QHBoxLayout()
        
        # Logo (could be replaced with an actual logo image)
        logo_label = QLabel()
        logo_label.setFixedSize(60, 60)
        logo_label.setStyleSheet("""
            background-color: #B67251;
            border-radius: 30px;
            color: white;
            font-size: 30px;
            font-weight: bold;
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setText("AP")  # App initials
        
        # Title with subtitle
        title_text_layout = QVBoxLayout()
        title_label = QLabel("Article Processor")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2F2D2C; padding: 0;")
        
        subtitle_label = QLabel("Convert article content to Markdown & JSON with ease")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setStyleSheet("color: #965C3F;")
        
        title_text_layout.addWidget(title_label)
        title_text_layout.addWidget(subtitle_label)
        
        title_layout.addWidget(logo_label)
        title_layout.addLayout(title_text_layout)
        title_layout.addStretch()
        
        main_layout.addLayout(title_layout)
        
        # Input section
        input_frame = StyledQFrame()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(15)
        
        # Section header
        input_header = QLabel("Article Input")
        input_header.setFont(QFont("Arial", 14, QFont.Bold))
        input_header.setStyleSheet("color: #B67251; margin-bottom: 5px;")
        input_layout.addWidget(input_header)
        
        # Metadata section with improved layout
        metadata_layout = QHBoxLayout()
        metadata_layout.setSpacing(15)
        
        # Filename input
        filename_layout = QVBoxLayout()
        filename_label = QLabel("Output Filename:")
        filename_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter filename (without extension)")
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        metadata_layout.addLayout(filename_layout, 1)
        
        # Author input
        author_layout = QVBoxLayout()
        author_label = QLabel("Author (optional):")
        author_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_input)
        metadata_layout.addLayout(author_layout, 1)
        
        input_layout.addLayout(metadata_layout)
        
        # Image selection with better layout
        image_frame = QFrame()
        image_frame.setFrameShape(QFrame.StyledPanel)
        image_frame.setStyleSheet("""
            QFrame {
                background-color: #F4F1ED;
                border-radius: 8px;
                border: 1px dashed #B67251;
            }
        """)
        image_layout = QHBoxLayout(image_frame)
        image_layout.setContentsMargins(10, 10, 10, 10)
        
        image_label = QLabel("Image:")
        image_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.image_path_label = QLineEdit()
        self.image_path_label.setReadOnly(True)
        self.image_path_label.setPlaceholderText("No image selected")
        self.image_path_label.setStyleSheet("""
            border: none;
            background-color: transparent;
            padding-left: 0;
        """)
        
        select_image_button = QPushButton("Select Image")
        select_image_button.setCursor(Qt.PointingHandCursor)
        select_image_button.setIcon(QIcon.fromTheme("document-open"))
        
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_path_label, 1)
        image_layout.addWidget(select_image_button)
        
        input_layout.addWidget(image_frame)
        
        # Article input
        input_label = QLabel("Article Text:")
        input_label.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout.addWidget(input_label)
        
        self.article_text = QTextEdit()
        self.article_text.setPlaceholderText("Paste your article here...")
        self.article_text.setMinimumHeight(150)
        input_layout.addWidget(self.article_text)
        
        # Date selection with improved styling
        date_frame = QFrame()
        date_frame.setFrameShape(QFrame.StyledPanel)
        date_frame.setStyleSheet("""
            QFrame {
                background-color: #F4F1ED;
                border-radius: 8px;
                border: none;
            }
        """)
        date_layout = QHBoxLayout(date_frame)
        date_layout.setContentsMargins(10, 10, 10, 10)
        
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
        
        input_layout.addWidget(date_frame)
        
        # Buttons with improved styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.process_button = QPushButton("Process Article")
        self.process_button.setCursor(Qt.PointingHandCursor)
        self.process_button.setIcon(QIcon.fromTheme("system-run"))
        self.process_button.setMinimumHeight(35)
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.setEnabled(False)
        self.save_button.setMinimumHeight(35)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        self.clear_button.setMinimumHeight(35)
        self.clear_button.setStyleSheet("""
            background-color: #DACDD3;
            color: #2F2D2C;
        """)
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(button_layout)
        
        # Progress bar with improved styling
        progress_frame = QFrame()
        progress_frame.setStyleSheet("background: transparent; border: none;")
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.progress_label = QLabel("Processing article...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.progress_label.setVisible(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        input_layout.addWidget(progress_frame)
        
        main_layout.addWidget(input_frame)
        
        # Output section with improved styling
        output_header = QLabel("Output Preview")
        output_header.setFont(QFont("Arial", 14, QFont.Bold))
        output_header.setStyleSheet("color: #B67251; margin: 5px 0;")
        main_layout.addWidget(output_header)
        
        output_splitter = QSplitter(Qt.Vertical)
        output_splitter.setHandleWidth(2)
        output_splitter.setChildrenCollapsible(False)
        
        # Markdown output
        markdown_frame = StyledQFrame()
        markdown_layout = QVBoxLayout(markdown_frame)
        markdown_layout.setContentsMargins(15, 15, 15, 15)
        markdown_label = QLabel("Markdown Output:")
        markdown_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.markdown_output = QTextEdit()
        self.markdown_output.setReadOnly(True)
        self.markdown_output.setFont(QFont("Consolas", 11))
        self.markdown_output.setStyleSheet("""
            background-color: #F4F1ED;
            border: 1px solid #DACDD3;
            border-radius: 8px;
        """)
        markdown_layout.addWidget(markdown_label)
        markdown_layout.addWidget(self.markdown_output)
        
        # JSON output
        json_frame = StyledQFrame()
        json_layout = QVBoxLayout(json_frame)
        json_layout.setContentsMargins(15, 15, 15, 15)
        json_label = QLabel("JSON Output:")
        json_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.json_output = QTextEdit()
        self.json_output.setReadOnly(True)
        self.json_output.setFont(QFont("Consolas", 11))
        self.json_output.setStyleSheet("""
            background-color: #F4F1ED;
            border: 1px solid #DACDD3;
            border-radius: 8px;
        """)
        json_layout.addWidget(json_label)
        json_layout.addWidget(self.json_output)
        
        output_splitter.addWidget(markdown_frame)
        output_splitter.addWidget(json_frame)
        output_splitter.setSizes([300, 300])
        
        main_layout.addWidget(output_splitter)
        
        # Add status bar for information
        self.statusBar().setStyleSheet("background-color: #EEEAE4; color: #2F2D2C;")
        self.statusBar().showMessage("Ready to process articles")
        
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
        file_dialog.setStyleSheet(self.styleSheet())
        image_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if image_path:
            self.selected_image_path = image_path
            # Show just the filename instead of the full path for cleaner UI
            filename = os.path.basename(image_path)
            self.image_path_label.setText(filename)
            self.statusBar().showMessage(f"Image selected: {filename}", 3000)
            
    def process_article(self):
        article_text = self.article_text.toPlainText()
        if not article_text:
            self.show_message_box("Warning", "Please enter article text", QMessageBox.Warning)
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
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.process_button.setEnabled(False)
        self.statusBar().showMessage("Processing article...")
        
        # Process in thread
        self.thread = ProcessThread(article_text, date_str, filename, author)
        self.thread.finished.connect(self.display_results)
        self.thread.error.connect(self.show_error)
        self.thread.progress.connect(self.update_progress)
        self.thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def display_results(self, result):
        self.result = result
        
        # Show markdown result with syntax highlighting
        self.markdown_output.setText(result.markdown)
        
        # Show JSON result with formatting
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
            self.show_message_box("User Information Needed", query_text, QMessageBox.Information)
        
        self.save_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.process_button.setEnabled(True)
        self.statusBar().showMessage("Processing completed successfully!", 5000)
        
        # Flash the output background briefly to indicate success
        self.flash_success()
    
    def flash_success(self):
        # Flash the output frames to indicate success
        original_style = self.markdown_output.styleSheet()
        success_style = """
            background-color: #E0F0E0;
            border: 1px solid #DACDD3;
            border-radius: 8px;
        """
        
        self.markdown_output.setStyleSheet(success_style)
        self.json_output.setStyleSheet(success_style)
        QApplication.processEvents()
        
        # Use a timer to reset the style
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(300, lambda: self.markdown_output.setStyleSheet(original_style))
        QTimer.singleShot(300, lambda: self.json_output.setStyleSheet(original_style))
    
    def show_error(self, error_msg):
        self.show_message_box("Error", f"An error occurred: {error_msg}", QMessageBox.Critical)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.process_button.setEnabled(True)
        self.statusBar().showMessage("Error during processing", 5000)
    
    def show_message_box(self, title, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #F0E9E1;
            }
            QLabel {
                color: #2F2D2C;
                font-size: 14px;
            }
            QPushButton {
                background-color: #B67251;
                color: #EEEAE4;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #965C3F;
            }
        """)
        msg_box.exec_()
    
    def save_results(self):
        if not hasattr(self, 'result'):
            return
            
        filename = self.filename_input.text().strip()
        if not filename:
            self.show_message_box("Warning", "Please enter a filename", QMessageBox.Warning)
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
            
            success_message = f"Files saved successfully:\n\nMarkdown: {md_path}\nJSON: {json_path}"
            if self.selected_image_path:
                success_message += f"\nImage: {new_image_name}"
            
            self.show_message_box("Files Saved", success_message, QMessageBox.Information)
            self.statusBar().showMessage(f"Files saved to {output_dir}", 5000)
            
        except Exception as e:
            self.show_message_box("Error", f"Failed to save files: {str(e)}", QMessageBox.Critical)
    
    def clear_all(self):
        self.article_text.clear()
        self.markdown_output.clear()
        self.json_output.clear()
        self.filename_input.clear()
        self.author_input.clear()
        self.image_path_label.clear()
        self.selected_image_path = None
        self.use_date_checkbox.setChecked(False)
        self.date_edit.setEnabled(False)
        self.date_edit.setSpecialValueText(" ")
        self.save_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        if hasattr(self, 'result'):
            del self.result
        self.statusBar().showMessage("All fields cleared", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
