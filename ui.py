import sys
import io
import contextlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QPlainTextEdit, QHBoxLayout, QMessageBox, QStackedWidget, QDateEdit, QSizePolicy, QLineEdit
)
from PySide6.QtCore import QDate
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import json
from url_fetcher1 import fetcher1



class SimpleUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Fetcher")
        self.setGeometry(100, 100, 300, 300)

        # --- Central widget (QStackedWidget to switch pages) ---
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # --- Pages ---
        self.fetcher_page = QWidget()
        self.dashboard_page = QWidget()
        self.mongodb_page = QWidget()
        self.settings_page = QWidget()

        self.init_fetcher_page()
        self.init_dashboard_page()
        self.init_mongodb_page()
        self.init_settings_page()

        self.stacked_widget.addWidget(self.fetcher_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.mongodb_page)
        self.stacked_widget.addWidget(self.settings_page)

        # --- Menu Bar ---
        menubar = self.menuBar()

        # Fetcher Menu
        fetcher_menu = menubar.addMenu("Fetcher")
        open_fetcher_action = fetcher_menu.addAction("Open Fetcher")
        open_fetcher_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.fetcher_page))

        # Dashboard Menu
        dashboard_menu = menubar.addMenu("Dashboard")
        open_dashboard_action = dashboard_menu.addAction("Open Dashboard")
        open_dashboard_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))

        # Mongodb Menu
        mongodb_menu = menubar.addMenu("MongoDB")
        open_mongodb_action = mongodb_menu.addAction("Download")
        open_mongodb_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.mongodb_page))

        # Settings Menu
        settings_menu = menubar.addMenu("Settings")
        open_settings_action = settings_menu.addAction("Config")
        open_settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_page))

        # Help Menu
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)




    # -----URL FETCHER AREA-----

    def init_fetcher_page(self):
        """Initialize the Fetcher layout and widgets."""
        layout = QVBoxLayout()

        # Widgets
        self.label = QLabel("Website:", self)
        self.label.setFixedWidth(60)
        self.combobox_fetcher = QComboBox(self)
        self.console_fetcher = QPlainTextEdit(self)
        self.console_fetcher.setReadOnly(True)

        # Buttons
        self.submit_button = QPushButton("Submit", self)
        self.clear_button = QPushButton("Clear Console", self)        

        # load available publications from json file
        with open("json_files/publications.json", "r", encoding="utf-8") as file:
            pub_data = json.load(file)

        # Add items to combobox
        self.combobox_fetcher.addItems(sorted(pub_data['publications']))

        # Row for label + combobox
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.label)
        row1_layout.addWidget(self.combobox_fetcher)

        # Row for Submit + Clear buttons
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.submit_button)
        row2_layout.addWidget(self.clear_button)
        
        layout.addLayout(row1_layout)
        layout.addLayout(row2_layout)
        
        # Console
        layout.addWidget(self.console_fetcher)
              

        self.fetcher_page.setLayout(layout)

        # Connect buttons
        self.submit_button.clicked.connect(self.processing)
        self.clear_button.clicked.connect(self.clear_console_fetcher)        

    def clear_console_fetcher(self):
        """Clear all logs in the console area."""
        self.console_fetcher.clear()

    def processing(self):
        selected_item = self.combobox_fetcher.currentText()
                
        with open("json_files/config.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        with open("json_files/fetcher_setting.json", "r", encoding="utf-8") as file:
            fetcher_setting = json.load(file)

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            fetcher_data = data[fetcher_setting[selected_item][0]]
            
            if fetcher_setting[selected_item][-1]==1:
                fetcher1(fetcher_data)
        
        logs = buffer.getvalue()
        self.console_fetcher.appendPlainText(logs if logs else "No logs captured.")
        # else:
        #     self.console_fetcher.appendPlainText("Processing other sources not yet implemented.")

    # ----- DASHBOARD AREA -----

    def init_dashboard_page(self):
        """Initialize a simple dashboard page (placeholder)."""
        layout = QVBoxLayout()

        title = QLabel("📊 Dashboard (coming soon)")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("This page will display graphs, charts, and statistics.")
        layout.addWidget(desc)

        back_button = QPushButton("Back to Fetcher")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.fetcher_page))
        layout.addWidget(back_button)

        self.dashboard_page.setLayout(layout)
    
    # ----- MONGO AREA -----

    def init_mongodb_page(self):
        """Initialize a simple dashboard page (placeholder)."""
        
        # Create Widgets
        self.label_web = QLabel("Website:", self)
        self.label_web.setFixedWidth(60)
        self.label_sdate = QLabel("Start:", self)
        self.label_sdate.setFixedWidth(60)
        self.label_edate = QLabel("End:", self)
        self.label_edate.setFixedWidth(60)
        self.website_combo = QComboBox(self)
        self.website_combo.setFixedWidth(150)
        self.date_spicker = QDateEdit(self)
        self.date_spicker.setCalendarPopup(True)  # Enables calendar dropdown
        self.date_spicker.setDate(QDate.currentDate())  # Default: today
        self.date_spicker.setFixedWidth(150)
        self.date_epicker = QDateEdit(self)
        self.date_epicker.setCalendarPopup(True)  # Enables calendar dropdown
        self.date_epicker.setDate(QDate.currentDate())  # Default: today
        self.date_epicker.setFixedWidth(150)
        
        self.fetch_button = QPushButton("Get Data")
        self.fetch_button.setFixedWidth(220)

        self.download_button = QPushButton('Download Data')
        self.download_button.setFixedWidth(220)

        # self.clear_button = QPushButton("Clear Console", self)
        # self.clear_button.setFixedWidth(150)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter path")
        
        # self.console_mongodb = QPlainTextEdit(self)
        # self.console_mongodb.setReadOnly(True)      
        # self.console_mongodb.setFixedWidth(300)

        # add options to combo box
        self.website_combo.addItems(['Bilyonaryo', 'BusinessMirror', 'Manila Bulletin'])

        # add widgets to layout
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.label_web)
        row1_layout.addWidget(self.website_combo)
        row1_layout.addStretch()
        
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.label_sdate)
        row2_layout.addWidget(self.date_spicker)
        row2_layout.addStretch()

        row3_layout = QHBoxLayout()
        row3_layout.addWidget(self.label_edate)
        row3_layout.addWidget(self.date_epicker)
        row3_layout.addStretch()

        row4_layout = QHBoxLayout()
        row4_layout.addWidget(self.fetch_button)
        # row4_layout.addWidget(self.clear_button)
        row4_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(row1_layout)
        left_layout.addLayout(row2_layout)
        left_layout.addLayout(row3_layout)
        # left_layout.addWidget(self.fetch_button)
        # left_layout.addWidget(self.clear_button)
        left_layout.addStretch()

        right_layout = QVBoxLayout()
        # right_layout.addWidget(self.console_mongodb)
        right_layout.addWidget(self.fetch_button)
        right_layout.addWidget(self.download_button)
        right_layout.addStretch()
        
        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        layout.addStretch()

        self.mongodb_page.setLayout(layout)
        
        # Connect buttons
        self.fetch_button.clicked.connect(self.fetch_mongodata)
        # self.clear_button.clicked.connect(self.clear_console_mongodb)

        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["fetcher"]   # change to your db name

    def clear_console_mongodb(self):
        """Clear all logs in the console area."""
        self.console_mongodb.clear()
        
    def fetch_mongodata(self):
        """Fetch documents from MongoDB and show in console."""

        selected_item = self.website_combo.currentText()

        if selected_item == 'Bilyonaryo':
            url_pub = 'bilyonaryo.com'
        elif selected_item == 'BusinessMirror':
            url_pub = 'businessmirror.com.ph'
        elif selected_item == 'Manila Bulletin':
            url_pub = 'mb.com.ph'

        start_date = self.date_spicker.date()
        end_date = self.date_epicker.date()

        # Convert QDate → Python datetime
        start_date = datetime(
            start_date.year(), start_date.month(), start_date.day(), 0, 0, 0
        )
        end_date = datetime(
            end_date.year(), end_date.month(), end_date.day(), 23, 59, 59
        )

        collection = self.db['collected_url']

        try:
            docs = list(collection.find({
                "publication_date": {"$gte": start_date, "$lte": end_date},
                "url": {"$regex": f"{url_pub}"}
                }))
            
            # Convert cursor to DataFrame
            df = pd.DataFrame(docs)            
            
            # Save to CSV
            # df.to_csv(f"{selected_item}.csv", index=False, encoding="utf-8")

            # self.console_mongodb.appendPlainText("csv file saved")
                            
        except Exception as e:
            # self.console_mongodb.appendPlainText(f"Error: {e}")
            pass

        return

    # ----- Settings Area -----

    def init_settings_page(self):

        # 


        return

    

    def close_app(self):
        """Exit the application."""
        QApplication.instance().quit()

    def show_about(self):
        """Show About dialog."""
        QMessageBox.information(self, "About", "URL Fetcher v1.0\nBuilt with PySide6")
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleUI()
    window.show()
    sys.exit(app.exec())
