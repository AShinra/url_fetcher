import sys
import io
import contextlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QPlainTextEdit, QHBoxLayout, QMessageBox, QStackedWidget, QDateEdit, QSizePolicy, QLineEdit, QTextEdit, QGridLayout
)
from PySide6.QtCore import Qt, QDate
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import json
from url_fetcher import fetcher
from common import connect_to_mongodb



class SimpleUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Fetcher")
        self.setGeometry(100, 100, 300, 300)

        # initialize db
        self.client = connect_to_mongodb()
        self.db = self.client["fetcher"]

        # --- Central widget (QStackedWidget to switch pages) ---
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # --- Pages ---
        self.fetcher_page = QWidget()
        self.dashboard_page = QWidget()
        self.mongodb_page = QWidget()
        self.edit_settings_page = QWidget()
        self.add_settings_page = QWidget()

        self.init_fetcher_page()
        self.init_dashboard_page()
        self.init_mongodb_page()
        self.init_edit_settings_page()
        self.init_add_settings_page()

        self.stacked_widget.addWidget(self.fetcher_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.mongodb_page)
        self.stacked_widget.addWidget(self.edit_settings_page)
        self.stacked_widget.addWidget(self.add_settings_page)

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
        open_add_settings_action = settings_menu.addAction('Add')
        open_add_settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.add_settings_page))
        open_edit_settings_action = settings_menu.addAction('Edit')
        open_edit_settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.edit_settings_page))

        # open_settings_action = settings_menu.addAction("Edit")

        # open_settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_page))

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
            fetcher_number = fetcher_setting[selected_item][-1]
            fetcher(fetcher_data, fetcher_number)
            
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

    def init_edit_settings_page(self):

        # self.client = connect_to_mongodb()
        # self.db = self.client["fetcher"]
        collection = self.db["publication_settings"]
        items = list(collection.find())

        # get the publication list
        pub_list = [item['pub_name'] for item in items]
        
        # create widgets
        self.pub_label = QLabel('Publication', self,) #label for publication combobox
        self.pub_label.setFixedWidth(100)
        
        self.pub_combo = QComboBox(self) #create publication combobox
        self.pub_combo.setFixedWidth(200)
        self.pub_combo.setStyleSheet("border: 2px solid orange;")
        self.pub_combo.addItems(pub_list) #add publications to conbobox options

        self.select_button = QPushButton('Select', self) #create select button
        self.select_button.setFixedWidth(200)

        self.update_button = QPushButton('Update', self) #create select button
        self.update_button.setFixedWidth(200)

        self.label_url = QLabel('URL', self)
        self.textbox_url = QLineEdit()

        self.label_container = QLabel('Container Selector', self)
        self.textbox_container = QLineEdit()

        self.label_title = QLabel('Title Selector', self)
        self.textbox_title = QLineEdit()

        self.label_fetcherno = QLabel('Fetcher', self)
        self.textbox_fetcherno = QLineEdit()
        self.textbox_fetcherno.setFixedWidth(30)

        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()      
        bl_layout = QVBoxLayout()
        br_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        layout = QVBoxLayout()

        left_layout.addWidget(self.pub_label)
        left_layout.addStretch()

        right_layout.addWidget(self.pub_combo)
        right_layout.addWidget(self.select_button)
        right_layout.addStretch()

        bl_layout.addWidget(self.label_url)
        bl_layout.addWidget(self.label_container)
        bl_layout.addWidget(self.label_title)
        bl_layout.addWidget(self.label_fetcherno)

        br_layout.addWidget(self.textbox_url)
        br_layout.addWidget(self.textbox_container)
        br_layout.addWidget(self.textbox_title)
        br_layout.addWidget(self.textbox_fetcherno)
        br_layout.addWidget(self.update_button)

        bottom_layout.addLayout(bl_layout)
        bottom_layout.addLayout(br_layout)

        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        top_layout.addStretch()

        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        layout.addStretch()

        self.edit_settings_page.setLayout(layout)

        # button behavior
        self.select_button.clicked.connect(self.select_publication_setting)
        self.update_button.clicked.connect(self.update_publication_setting)

        return
    
    def select_publication_setting(self):
        """Load selected settings"""
        collection = self.db['publication_settings']
        docs = list(collection.find({'pub_name':self.pub_combo.currentText()}))
        self.textbox_url.setText(docs[0]['fetcher_url'])
        self.textbox_container.setText(docs[0]['selector_container'])
        self.textbox_title.setText(docs[0]['selector_title'])
        self.textbox_fetcherno.setText(str(docs[0]['fetcher_no']))

    def update_publication_setting(self):
        """Update publication setting"""
        url = self.textbox_url.text()
        container = self.textbox_container.text()
        title = self.textbox_title.text()
        fetcherno = int(self.textbox_fetcherno.text())
        
        collection = self.db['publication_settings']
        query_text = self.pub_combo.currentText()
        query = {'pub_name':query_text}

        new_values = {'$set':{
            'fetcher_url':url,
            'selector_container':container,
            'selector_title':title,
            'fetcher_no':fetcherno
        }}

        result = collection.update_one(query, new_values)
        
        if result.modified_count > 0:
            QMessageBox.information(self, "Success", "Document updated successfully!")
        elif result.matched_count > 0:
            QMessageBox.warning(self, "No Change", "Document found, but no changes were made.")
        else:
            QMessageBox.critical(self, "Error", "No matching document found.")

    def init_add_settings_page(self):
        # create widgets
        # ---Labels---
        label_pub = QLabel('PUBLICATION', self)
        label_pub.setAlignment(Qt.AlignCenter)
        label_pub.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_pub.setFixedWidth(150)

        label_url = QLabel('URL', self)
        label_url.setAlignment(Qt.AlignCenter)
        label_url.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_url.setFixedWidth(150)

        label_selectors = QLabel('SELECTORS', self)
        label_selectors.setAlignment(Qt.AlignCenter)
        label_selectors.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_selectors.setFixedWidth(150)

        label_container = QLabel('CONTAINER', self)
        label_container.setAlignment(Qt.AlignCenter)
        label_container.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_container.setFixedWidth(150)

        label_title = QLabel('TITLE', self)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_title.setFixedWidth(150)

        label_fetcherno = QLabel('FETCHER NO.', self)
        label_fetcherno.setAlignment(Qt.AlignCenter)
        label_fetcherno.setStyleSheet("border: 2px solid gray; color: cyan; font-weight: bold")
        label_fetcherno.setFixedWidth(150)

        # ---Textboxes---
        self.tb_pub = QLineEdit()
        self.tb_url = QLineEdit()
        self.tb_container = QLineEdit()
        self.tb_title = QLineEdit()
        self.combo_fetcherno = QComboBox(self)
        self.combo_fetcherno.setFixedWidth(40)
        self.combo_fetcherno.addItems([str(i) for i in range(1, 11)])
        # ---Buttons---
        btn_add = QPushButton('ADD CONFIGURATION', self)
        btn_clear = QPushButton('CLEAR', self)

        # create layout containers
        main_layout = QVBoxLayout()
        container_layout = QGridLayout()
        bottom_layout = QHBoxLayout()
        
        # add widgets to layout
        container_layout.addWidget(label_pub, 0, 0)
        container_layout.addWidget(self.tb_pub, 0, 1)
        container_layout.addWidget(label_url, 1, 0)
        container_layout.addWidget(self.tb_url, 1, 1)
        container_layout.addWidget(label_selectors, 2, 0)
        container_layout.addWidget(label_container, 3, 0)
        container_layout.addWidget(self.tb_container, 3, 1)
        container_layout.addWidget(label_title, 4, 0)
        container_layout.addWidget(self.tb_title, 4, 1)
        container_layout.addWidget(label_fetcherno, 5, 0)
        container_layout.addWidget(self.combo_fetcherno, 5, 1)

        bottom_layout.addWidget(btn_add)
        bottom_layout.addWidget(btn_clear)
        # container_layout.addWidget(btn_add, 6, 1)
        # container_layout.addWidget(btn_clear, 7, 1)
        
        main_layout.addLayout(container_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        self.add_settings_page.setLayout(main_layout)

        btn_add.clicked.connect(self.add_configuration)
        btn_clear.clicked.connect(self.clear_fields)
    
    def add_configuration(self):
        """Add new configuration"""
        pub = self.tb_pub.text()
        url = self.tb_url.text()
        container = self.tb_container.text()
        title = self.tb_title.text()
        fetcherno = int(self.combo_fetcherno.currentText())

        if pub=='' or url=='' or container=='' or title=='':
            QMessageBox.critical(self, "Error", "Some fields are blank")
        else:
            collection = self.db['publication_settings']

            document = {
                'fetcher_no':fetcherno,
                'fetcher_url':url,
                'pub_name':pub,
                'selector_container':container,
                'selector_title':title
            }

            if not collection.find_one({"pub_name": pub}):
                result = collection.insert_one(document)
                QMessageBox.information(self, "Success", "New configuration added")                
            else:
                QMessageBox.warning(self, "Existing", f"There is an existing configuration for {pub}")


    def clear_fields(self):
        """clear all fields"""
        self.tb_pub.clear()
        self.tb_container.clear()
        self.tb_title.clear()
        self.tb_url.clear()

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
