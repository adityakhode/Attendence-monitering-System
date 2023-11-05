import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
import os
import shutil
import pandas as pd
import sqlite3
import tempfile
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets

button_y_position = 0.1  # Initial Y position for the buttons
class Addsubject(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Custom Pop-up Block')
        self.setGeometry(400, 200, 400, 200)

        # Create layouts for the dialog
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Create labels and line edits for subject name, teacher name, and number of students
        subject_label = QLabel("Subject Name:")
        self.subject_edit = QLineEdit(self)

        button1 = QPushButton("Create")
        button1.clicked.connect(self.on_button1_click)
        
        self.label_message = QLabel('Select the Students data Excel file:')
    
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_file)
        

        # Create and add a button to the button layout
        

        # Add labels, line edits, and the button to the layouts
        main_layout.addWidget(subject_label)
        main_layout.addWidget(self.subject_edit)
        main_layout.addWidget(self.label_message)
        main_layout.addWidget(browse_button)
        button_layout.addWidget(button1)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def on_button1_click(self):
        subject_name = self.subject_edit.text()

        print(f"Subject Name: {subject_name}")
        self.accept()
        
    def create_class_data(self):
        subject_name = self.subject_edit.text()

        return subject_name 
    
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Excel File', '', 'Excel files (*.xlsx);;All Files (*)', options=options)

        if file_path:
            self.label_message.setText("File Opened: " + file_path)
            self.process_excel_file(file_path)

    def process_excel_file(self, file_path):
        # Create a temporary directory
        temporary_directory = tempfile.mkdtemp()

        # Copy the Excel file to the temporary directory
        temp_file_path = os.path.join(temporary_directory, os.path.basename(file_path))

        try:
            shutil.copy(file_path, temp_file_path)

            # Connect to the database
            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()

            # Read the Excel file
            df = pd.read_excel(temp_file_path)

            # Insert data into the Students table
            for _, row in df.iterrows():
                roll_number = str(row["Roll Number"])
                name = row["Name"]
                cursor.execute("INSERT INTO Students (Roll_Number, Name) VALUES (?, ?)", (roll_number, name))
                
            cursor.execute("SELECT * FROM Students;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            # Commit the changes and close the connection
            conn.commit()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
