#!/usr/bin/env python3
"""
Configuration file for Entertainment Suggester

This file contains application settings and configuration options.
Modify these values to customize the application behavior.
"""

# TMDB API Configuration
# Get your free API key from: https://www.themoviedb.org/settings/api
# Replace the placeholder below with your actual API key
TMDB_API_KEY = "4442a3c5164c166f59a9c39c70633dfb"

# Database Configuration
DATABASE_PATH = "watchlist.db"

# Application Settings
APP_NAME = "Entertainment Suggester"
APP_VERSION = "1.0.0"

# Recommendation Engine Settings
RECOMMENDATION_LIMIT = 10
RATING_THRESHOLD = 7.0  # Minimum rating to consider as "liked"
TRENDING_WEIGHT = 0.3   # Weight for trending content in recommendations
GENRE_WEIGHT = 0.7      # Weight for genre preferences in recommendations

# UI Settings
AUTO_REFRESH_INTERVAL = 30000  # milliseconds (30 seconds)
TABLE_REFRESH_ON_EDIT = True
SHOW_SETUP_MESSAGE = True  # Show TMDB setup message on first run

# Export/Import Settings
DEFAULT_EXPORT_FILENAME = "watchlist_backup.json"
INCLUDE_METADATA_IN_EXPORT = True

# Chart and Statistics Settings
MAX_GENRES_IN_CHART = 8
CHART_COLOR_SCHEME = "Set3"  # Matplotlib color scheme

# Platform Options (for dropdown in Add Content dialog)
DEFAULT_PLATFORMS = [
    "Netflix",
    "Amazon Prime Video",
    "Disney+",
    "HBO Max",
    "Hulu",
    "Apple TV+",
    "Paramount+",
    "Peacock",
    "Discovery+",
    "Cinema",
    "Blu-ray/DVD",
    "Other"
]

# Language Options
DEFAULT_LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Chinese",
    "Hindi",
    "Portuguese",
    "Russian",
    "Other"
]

# Genre Options (will be supplemented by TMDB API if available)
DEFAULT_GENRES = [
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Science Fiction",
    "Thriller",
    "War",
    "Western"
]

# Validation Settings
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 200
MIN_YEAR = 1900
MAX_YEAR = 2030
MIN_DURATION = 1  # minutes
MAX_DURATION = 1000  # minutes
MIN_RATING = 0.0
MAX_RATING = 10.0

# Debug Settings
DEBUG_MODE = False
LOG_API_REQUESTS = False
VERBOSE_RECOMMENDATIONS = False

# Feature Flags
ENABLE_TMDB_INTEGRATION = True
ENABLE_RECOMMENDATIONS = True
ENABLE_STATISTICS = True
ENABLE_EXPORT_IMPORT = True
ENABLE_AUTO_REFRESH = True

# Error Messages
ERROR_MESSAGES = {
    "no_tmdb_key": "TMDB API key not configured. Some features may be limited.",
    "api_error": "Error connecting to TMDB API. Please check your internet connection.",
    "database_error": "Database error occurred. Please check file permissions.",
    "import_error": "Error importing data. Please check file format.",
    "export_error": "Error exporting data. Please check file permissions."
}

# Success Messages
SUCCESS_MESSAGES = {
    "content_added": "Content added successfully!",
    "content_updated": "Content updated successfully!",
    "content_deleted": "Content deleted successfully!",
    "data_exported": "Data exported successfully!",
    "data_imported": "Data imported successfully!",
    "marked_watched": "Marked as watched successfully!"
}

# Help Text
HELP_TEXT = {
    "tmdb_setup": """
To enable automatic metadata fetching:
1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings > API
4. Request an API key
5. Edit config.py and set TMDB_API_KEY
""",
    "rating_system": """
Rating System:
- 0-2: Poor
- 3-4: Below Average
- 5-6: Average
- 7-8: Good
- 9-10: Excellent
""",
    "recommendations": """
Recommendations are based on:
- Your genre preferences
- Highly rated content
- Similar content analysis
- Trending releases
"""
}

def get_tmdb_api_key():
    """Get the TMDB API key from configuration"""
    return TMDB_API_KEY if TMDB_API_KEY != "YOUR_TMDB_API_KEY_HERE" else None

def is_tmdb_configured():
    """Check if TMDB API key is properly configured"""
    return get_tmdb_api_key() is not None

def get_database_path():
    """Get the database file path"""
    return DATABASE_PATH

def get_app_info():
    """Get application information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION
    }