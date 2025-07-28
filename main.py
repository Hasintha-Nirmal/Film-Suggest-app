#!/usr/bin/env python3
"""
Entertainment Suggester - Smart Movie & TV Tracker

A comprehensive application to track watched movies and TV shows,
and get personalized recommendations based on your viewing history.

Features:
- Track watched content with detailed metadata
- Smart recommendations based on preferences
- Statistics and analytics
- TMDB API integration for automatic metadata
- Export/Import functionality
- Modern PyQt6 GUI

Author: AI Assistant
Version: 1.0.0
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    try:
        import PyQt6
    except ImportError:
        missing_deps.append('PyQt6')
    
    try:
        import requests
    except ImportError:
        missing_deps.append('requests')
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append('matplotlib')
    
    try:
        from fuzzywuzzy import fuzz
    except ImportError:
        missing_deps.append('fuzzywuzzy')
    
    try:
        import numpy
    except ImportError:
        missing_deps.append('numpy')
    
    try:
        import pandas
    except ImportError:
        missing_deps.append('pandas')
    
    return missing_deps

def show_setup_instructions():
    """Show setup instructions for missing dependencies"""
    missing = check_dependencies()
    
    if missing:
        app = QApplication(sys.argv)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Missing Dependencies")
        msg.setText("Some required dependencies are missing.")
        
        details = "Missing packages:\n" + "\n".join(f"- {dep}" for dep in missing)
        details += "\n\nTo install all dependencies, run:\n"
        details += "pip install -r requirements.txt\n\n"
        details += "Or install individually:\n"
        for dep in missing:
            details += f"pip install {dep}\n"
        
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        
        return False
    
    return True

def show_tmdb_setup_message():
    """Show TMDB API setup instructions"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("TMDB API Setup")
    msg.setText("Welcome to Entertainment Suggester!")
    
    details = """For the best experience with automatic metadata fetching and recommendations, 
you'll need a free TMDB API key.

To get your API key:
1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings > API
4. Request an API key (choose 'Developer')
5. Edit config.py and replace 'YOUR_TMDB_API_KEY_HERE' with your actual key

The app will work without an API key, but you'll need to enter movie/TV show details manually.

Click OK to continue..."""
    
    msg.setDetailedText(details)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

def main():
    """Main entry point"""
    print("Starting Entertainment Suggester...")
    
    # Check dependencies
    if not check_dependencies():
        if not show_setup_instructions():
            return 1
    
    try:
        # Import main window after dependency check
        from main_window import MainWindow
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Entertainment Suggester")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Entertainment Suggester")
        
        # Set application icon if available
        # app.setWindowIcon(QIcon('icon.png'))
        
        # Show TMDB setup message on first run
        if not os.path.exists('watchlist.db'):
            show_tmdb_setup_message()
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("Application started successfully!")
        print("Database location: watchlist.db")
        print("To exit, close the application window.")
        
        # Run application
        return app.exec()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())