import sys
import json
from datetime import datetime, date
from typing import Dict, List
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit, QLabel,
    QDialog, QFormLayout, QDialogButtonBox, QMessageBox, QFileDialog,
    QProgressBar, QSplitter, QFrame, QScrollArea, QGridLayout,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor, QIcon
import requests
from database import DatabaseManager
from tmdb_api import TMDBApi
from recommendation_engine import RecommendationEngine
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class ContentDialog(QDialog):
    def __init__(self, parent=None, content_data=None, tmdb_api=None):
        super().__init__(parent)
        self.content_data = content_data or {}
        self.tmdb_api = tmdb_api
        self.setWindowTitle("Add/Edit Content")
        self.setModal(True)
        self.resize(500, 600)
        self.setup_ui()
        
        if content_data:
            self.populate_fields()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for movie/TV show...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_content)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["movie", "tv"])
        self.genre_input = QLineEdit()
        self.language_input = QLineEdit()
        self.rating_input = QDoubleSpinBox()
        self.rating_input.setRange(0, 10)
        self.rating_input.setSingleStep(0.1)
        self.platform_combo = QComboBox()
        self.platform_combo.setEditable(True)
        self.platform_combo.addItems([
            "Netflix", "Amazon Prime", "Disney+", "HBO Max", "Hulu",
            "Apple TV+", "Paramount+", "Cinema", "Other"
        ])
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 1000)
        self.duration_input.setSuffix(" min")
        self.director_input = QLineEdit()
        self.actors_input = QLineEdit()
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2030)
        self.year_input.setValue(datetime.now().year)
        self.overview_input = QTextEdit()
        self.overview_input.setMaximumHeight(100)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["watched", "want_to_watch"])
        
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Type:", self.type_combo)
        form_layout.addRow("Genre:", self.genre_input)
        form_layout.addRow("Language:", self.language_input)
        form_layout.addRow("Rating (0-10):", self.rating_input)
        form_layout.addRow("Platform:", self.platform_combo)
        form_layout.addRow("Date Watched:", self.date_input)
        form_layout.addRow("Duration:", self.duration_input)
        form_layout.addRow("Director/Creator:", self.director_input)
        form_layout.addRow("Actors:", self.actors_input)
        form_layout.addRow("Year:", self.year_input)
        form_layout.addRow("Overview:", self.overview_input)
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def search_content(self):
        query = self.search_input.text().strip()
        if not query or not self.tmdb_api:
            return
        
        results = self.tmdb_api.search_content(query)
        if results:
            # Show first result
            result = results[0]
            content_type = 'movie' if 'title' in result else 'tv'
            
            # Get detailed information
            if content_type == 'movie':
                details = self.tmdb_api.get_movie_details(result['id'])
            else:
                details = self.tmdb_api.get_tv_details(result['id'])
            
            if details:
                formatted_data = self.tmdb_api.format_content_data(details, content_type)
                self.populate_from_tmdb(formatted_data)
    
    def populate_from_tmdb(self, data):
        self.title_input.setText(data.get('title', ''))
        self.type_combo.setCurrentText(data.get('type', 'movie'))
        self.genre_input.setText(data.get('genre', ''))
        self.language_input.setText(data.get('language', ''))
        if data.get('year'):
            self.year_input.setValue(data['year'])
        if data.get('duration'):
            self.duration_input.setValue(data['duration'])
        self.director_input.setText(data.get('director', ''))
        self.actors_input.setText(data.get('actors', ''))
        self.overview_input.setText(data.get('overview', ''))
    
    def populate_fields(self):
        self.title_input.setText(self.content_data.get('title', ''))
        self.type_combo.setCurrentText(self.content_data.get('type', 'movie'))
        self.genre_input.setText(self.content_data.get('genre', ''))
        self.language_input.setText(self.content_data.get('language', ''))
        if self.content_data.get('rating'):
            self.rating_input.setValue(float(self.content_data['rating']))
        self.platform_combo.setCurrentText(self.content_data.get('platform', ''))
        if self.content_data.get('date_watched'):
            date_obj = datetime.strptime(self.content_data['date_watched'], '%Y-%m-%d').date()
            self.date_input.setDate(QDate(date_obj))
        if self.content_data.get('duration'):
            self.duration_input.setValue(self.content_data['duration'])
        self.director_input.setText(self.content_data.get('director', ''))
        self.actors_input.setText(self.content_data.get('actors', ''))
        if self.content_data.get('year'):
            self.year_input.setValue(self.content_data['year'])
        self.overview_input.setText(self.content_data.get('overview', ''))
        self.status_combo.setCurrentText(self.content_data.get('status', 'watched'))
    
    def get_data(self):
        return {
            'title': self.title_input.text(),
            'type': self.type_combo.currentText(),
            'genre': self.genre_input.text(),
            'language': self.language_input.text(),
            'rating': self.rating_input.value() if self.rating_input.value() > 0 else None,
            'platform': self.platform_combo.currentText(),
            'date_watched': self.date_input.date().toString('yyyy-MM-dd'),
            'duration': self.duration_input.value() if self.duration_input.value() > 0 else None,
            'director': self.director_input.text(),
            'actors': self.actors_input.text(),
            'year': self.year_input.value(),
            'overview': self.overview_input.toPlainText(),
            'status': self.status_combo.currentText()
        }

class StatsWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setup_ui()
        self.update_stats()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Stats cards
        cards_layout = QGridLayout()
        
        self.total_watched_label = QLabel("0")
        self.total_hours_label = QLabel("0.0")
        self.avg_rating_label = QLabel("0.0")
        self.top_genre_label = QLabel("N/A")
        
        # Style the labels
        for label in [self.total_watched_label, self.total_hours_label, 
                     self.avg_rating_label, self.top_genre_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2196F3;
                    padding: 10px;
                    border: 2px solid #E3F2FD;
                    border-radius: 8px;
                    background-color: #F5F5F5;
                }
            """)
        
        cards_layout.addWidget(QLabel("Total Watched:"), 0, 0)
        cards_layout.addWidget(self.total_watched_label, 1, 0)
        cards_layout.addWidget(QLabel("Hours Watched:"), 0, 1)
        cards_layout.addWidget(self.total_hours_label, 1, 1)
        cards_layout.addWidget(QLabel("Average Rating:"), 0, 2)
        cards_layout.addWidget(self.avg_rating_label, 1, 2)
        cards_layout.addWidget(QLabel("Top Genre:"), 0, 3)
        cards_layout.addWidget(self.top_genre_label, 1, 3)
        
        layout.addLayout(cards_layout)
        
        # Chart
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def update_stats(self):
        stats = self.db.get_stats()
        
        self.total_watched_label.setText(str(stats['total_watched']))
        self.total_hours_label.setText(f"{stats['total_hours']}h")
        self.avg_rating_label.setText(f"{stats['avg_rating']}/10")
        self.top_genre_label.setText(stats['top_genre'])
        
        # Update chart
        self.update_chart(stats['genre_distribution'])
    
    def update_chart(self, genre_data):
        self.figure.clear()
        
        if not genre_data:
            return
        
        ax = self.figure.add_subplot(111)
        genres = [item[0] for item in genre_data[:8]]  # Top 8 genres
        counts = [item[1] for item in genre_data[:8]]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(genres)))
        bars = ax.bar(genres, counts, color=colors)
        
        ax.set_title('Genre Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Genres')
        ax.set_ylabel('Count')
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        self.figure.tight_layout()
        self.canvas.draw()

class RecommendationWidget(QWidget):
    def __init__(self, recommendation_engine):
        super().__init__()
        self.rec_engine = recommendation_engine
        self.setup_ui()
        self.load_recommendations()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Smart Recommendations")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_recommendations)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        layout.addLayout(header_layout)
        
        # Recommendations scroll area
        scroll = QScrollArea()
        self.recommendations_widget = QWidget()
        self.recommendations_layout = QVBoxLayout(self.recommendations_widget)
        scroll.setWidget(self.recommendations_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def load_recommendations(self):
        # Clear existing recommendations
        for i in reversed(range(self.recommendations_layout.count())):
            self.recommendations_layout.itemAt(i).widget().setParent(None)
        
        recommendations = self.rec_engine.get_recommendations(10)
        
        for rec in recommendations:
            rec_widget = self.create_recommendation_widget(rec)
            self.recommendations_layout.addWidget(rec_widget)
        
        self.recommendations_layout.addStretch()
    
    def create_recommendation_widget(self, rec):
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet("""
            QFrame {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
                background-color: white;
            }
        """)
        
        layout = QHBoxLayout(widget)
        
        # Content info
        info_layout = QVBoxLayout()
        
        title_label = QLabel(f"{rec['title']} ({rec.get('year', 'N/A')})")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        type_label = QLabel(f"Type: {rec['type'].title()}")
        type_label.setStyleSheet("color: #666;")
        
        reason_label = QLabel(f"Why: {rec['reason']}")
        reason_label.setStyleSheet("color: #1976D2; font-style: italic;")
        reason_label.setWordWrap(True)
        
        if rec.get('rating'):
            rating_label = QLabel(f"TMDB Rating: {rec['rating']:.1f}/10")
            rating_label.setStyleSheet("color: #4CAF50;")
            info_layout.addWidget(rating_label)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(type_label)
        info_layout.addWidget(reason_label)
        
        if rec.get('overview'):
            overview_label = QLabel(rec['overview'][:200] + "..." if len(rec['overview']) > 200 else rec['overview'])
            overview_label.setWordWrap(True)
            overview_label.setStyleSheet("color: #555; font-size: 12px;")
            info_layout.addWidget(overview_label)
        
        layout.addLayout(info_layout)
        
        # Add to watchlist button
        add_btn = QPushButton("Add to Watchlist")
        add_btn.setMaximumWidth(120)
        add_btn.clicked.connect(lambda: self.add_to_watchlist(rec))
        layout.addWidget(add_btn)
        
        return widget
    
    def add_to_watchlist(self, rec):
        # Add recommendation to want_to_watch list
        content_data = {
            'title': rec['title'],
            'type': rec['type'],
            'year': rec.get('year'),
            'tmdb_id': rec.get('tmdb_id'),
            'poster_url': rec.get('poster_url'),
            'overview': rec.get('overview'),
            'status': 'want_to_watch',
            'date_watched': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.rec_engine.db.add_content(content_data)
        QMessageBox.information(self, "Success", f"'{rec['title']}' added to your watchlist!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entertainment Suggester - Smart Movie & TV Tracker")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components
        self.db = DatabaseManager()
        self.tmdb_api = TMDBApi()
        self.rec_engine = RecommendationEngine(self.db, self.tmdb_api)
        
        self.setup_ui()
        self.setup_style()
        
        # Auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(30000)  # Refresh every 30 seconds
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Watched content tab
        self.watched_tab = self.create_watched_tab()
        self.tabs.addTab(self.watched_tab, "📺 Watched")
        
        # Watchlist tab
        self.watchlist_tab = self.create_watchlist_tab()
        self.tabs.addTab(self.watchlist_tab, "📋 Watchlist")
        
        # Recommendations tab
        self.recommendations_tab = RecommendationWidget(self.rec_engine)
        self.tabs.addTab(self.recommendations_tab, "🎯 Recommendations")
        
        # Stats tab
        self.stats_tab = StatsWidget(self.db)
        self.tabs.addTab(self.stats_tab, "📊 Statistics")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_watched_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Content")
        add_btn.clicked.connect(self.add_content)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.clicked.connect(self.edit_content)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_content)
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self.export_data)
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self.import_data)
        
        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addWidget(edit_btn)
        toolbar_layout.addWidget(delete_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addWidget(import_btn)
        
        layout.addLayout(toolbar_layout)
        
        # Table
        self.watched_table = QTableWidget()
        self.watched_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.watched_table)
        
        self.load_watched_content()
        
        return widget
    
    def create_watchlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        mark_watched_btn = QPushButton("✅ Mark as Watched")
        mark_watched_btn.clicked.connect(self.mark_as_watched)
        
        remove_btn = QPushButton("❌ Remove")
        remove_btn.clicked.connect(self.remove_from_watchlist)
        
        toolbar_layout.addWidget(mark_watched_btn)
        toolbar_layout.addWidget(remove_btn)
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # Table
        self.watchlist_table = QTableWidget()
        self.watchlist_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.watchlist_table)
        
        self.load_watchlist_content()
        
        return widget
    
    def setup_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QTabWidget::pane {
                border: 1px solid #C0C0C0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QTableWidget {
                gridline-color: #E0E0E0;
                background-color: white;
                alternate-background-color: #F9F9F9;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def load_watched_content(self):
        content = self.db.get_all_content(status='watched')
        self.populate_table(self.watched_table, content)
    
    def load_watchlist_content(self):
        content = self.db.get_all_content(status='want_to_watch')
        self.populate_table(self.watchlist_table, content)
    
    def populate_table(self, table, content):
        if not content:
            table.setRowCount(0)
            table.setColumnCount(0)
            return
        
        headers = ['ID', 'Title', 'Type', 'Genre', 'Rating', 'Platform', 'Date', 'Year']
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(content))
        
        for row, item in enumerate(content):
            table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            table.setItem(row, 1, QTableWidgetItem(item['title'] or ''))
            table.setItem(row, 2, QTableWidgetItem(item['type'] or ''))
            table.setItem(row, 3, QTableWidgetItem(item['genre'] or ''))
            table.setItem(row, 4, QTableWidgetItem(str(item['rating']) if item['rating'] else ''))
            table.setItem(row, 5, QTableWidgetItem(item['platform'] or ''))
            table.setItem(row, 6, QTableWidgetItem(item['date_watched'] or ''))
            table.setItem(row, 7, QTableWidgetItem(str(item['year']) if item['year'] else ''))
        
        # Hide ID column
        table.hideColumn(0)
        
        # Resize columns
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for i in range(2, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
    
    def add_content(self):
        dialog = ContentDialog(self, tmdb_api=self.tmdb_api)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.add_content(data)
            self.refresh_data()
            self.statusBar().showMessage(f"Added '{data['title']}'")
    
    def edit_content(self):
        current_table = self.get_current_table()
        if not current_table:
            return
        
        current_row = current_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row to edit.")
            return
        
        content_id = int(current_table.item(current_row, 0).text())
        content = self.db.get_all_content()
        content_data = next((c for c in content if c['id'] == content_id), None)
        
        if content_data:
            dialog = ContentDialog(self, content_data, self.tmdb_api)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                self.db.update_content(content_id, data)
                self.refresh_data()
                self.statusBar().showMessage(f"Updated '{data['title']}'")
    
    def delete_content(self):
        current_table = self.get_current_table()
        if not current_table:
            return
        
        current_row = current_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row to delete.")
            return
        
        content_id = int(current_table.item(current_row, 0).text())
        title = current_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_content(content_id)
            self.refresh_data()
            self.statusBar().showMessage(f"Deleted '{title}'")
    
    def mark_as_watched(self):
        current_row = self.watchlist_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row to mark as watched.")
            return
        
        content_id = int(self.watchlist_table.item(current_row, 0).text())
        title = self.watchlist_table.item(current_row, 1).text()
        
        # Update status to watched
        self.db.update_content(content_id, {
            'status': 'watched',
            'date_watched': datetime.now().strftime('%Y-%m-%d')
        })
        
        self.refresh_data()
        self.statusBar().showMessage(f"Marked '{title}' as watched")
    
    def remove_from_watchlist(self):
        current_row = self.watchlist_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")
            return
        
        content_id = int(self.watchlist_table.item(current_row, 0).text())
        title = self.watchlist_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Remove",
            f"Are you sure you want to remove '{title}' from watchlist?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_content(content_id)
            self.refresh_data()
            self.statusBar().showMessage(f"Removed '{title}' from watchlist")
    
    def get_current_table(self):
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            return self.watched_table
        elif current_tab == 1:
            return self.watchlist_table
        return None
    
    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "watchlist_backup.json", "JSON Files (*.json)"
        )
        
        if file_path:
            data = self.db.export_data()
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Success", "Data exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Data", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if self.db.import_data(data):
                    self.refresh_data()
                    QMessageBox.information(self, "Success", "Data imported successfully!")
                else:
                    QMessageBox.critical(self, "Error", "Import failed!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Import failed: {str(e)}")
    
    def refresh_data(self):
        self.load_watched_content()
        self.load_watchlist_content()
        self.stats_tab.update_stats()
        self.rec_engine.update_preferences()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Entertainment Suggester")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()