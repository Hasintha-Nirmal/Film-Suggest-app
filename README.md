# Entertainment Suggester 🎬📺

A smart application to track all the movies and TV series you've watched, and get personalized recommendations based on your viewing preferences.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📝 Content Tracking
- **Add watched movies and TV shows** with comprehensive details:
  - Title, genre, language, personal rating (0-10)
  - Platform (Netflix, Prime Video, Disney+, etc.)
  - Date watched, duration, year
  - Director/creator and main actors
  - Plot overview
- **Automatic metadata fetching** from TMDB API
- **Search integration** - just type a title and get all details automatically
- **Watchlist management** - mark content as "Want to Watch"

### 🎯 Smart Recommendations
- **Personalized suggestions** based on:
  - Your favorite genres and themes
  - Highly rated content in your history
  - Similar user preferences patterns
  - New and trending releases in your interest areas
- **Clear reasoning** for each suggestion (e.g., "You liked 'Dark', so we suggest '1899' – same creators and similar tone")
- **Multiple recommendation sources**:
  - Genre-based recommendations
  - Similar content analysis
  - Trending content matching your preferences

### 📊 Statistics & Analytics
- **Viewing statistics**:
  - Total content watched
  - Hours spent watching
  - Average personal rating
  - Most-watched genre
- **Visual analytics**:
  - Genre distribution charts
  - Viewing patterns over time
  - Rating trends

### 💾 Data Management
- **Permanent storage** in local SQLite database
- **Export/Import functionality** for backup and sharing
- **Data persistence** - your data is always safe

### 🎨 Modern Interface
- **Clean, modern GUI** built with PyQt6
- **Tabbed interface** for easy navigation:
  - 📺 Watched Content
  - 📋 Watchlist
  - 🎯 Recommendations
  - 📊 Statistics
- **Responsive design** with intuitive controls
- **Real-time updates** and auto-refresh

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**:
   ```bash
   git clone <repository-url>
   cd ent-sugesstor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### First-Time Setup

1. **TMDB API Key (Recommended)**:
   - Go to [TMDB](https://www.themoviedb.org/) and create a free account
   - Navigate to Settings > API and request an API key
   - Edit `config.py` and replace `YOUR_TMDB_API_KEY_HERE` with your actual key
   - This enables automatic metadata fetching and better recommendations

2. **Start adding content**:
   - Click "➕ Add Content" in the Watched tab
   - Use the search feature to automatically fill details
   - Or manually enter information

## 📖 User Guide

### Adding Content

1. **Automatic Method** (with TMDB API):
   - Click "➕ Add Content"
   - Type the movie/show title in the search box
   - Click "Search" to auto-fill details
   - Adjust personal rating, platform, and date
   - Click "OK" to save

2. **Manual Method**:
   - Click "➕ Add Content"
   - Fill in all fields manually
   - Click "OK" to save

### Managing Your Watchlist

- **Add to Watchlist**: Use recommendations or manually add content with status "Want to Watch"
- **Mark as Watched**: Select content in Watchlist tab and click "✅ Mark as Watched"
- **Remove from Watchlist**: Select and click "❌ Remove"

### Getting Recommendations

- Navigate to the "🎯 Recommendations" tab
- Click "Refresh" to get new suggestions
- Each recommendation shows:
  - Title and basic info
  - Reason for recommendation
  - TMDB rating
  - Plot overview
- Click "Add to Watchlist" to save interesting suggestions

### Viewing Statistics

- Go to "📊 Statistics" tab to see:
  - Key metrics (total watched, hours, average rating, top genre)
  - Genre distribution chart
  - Visual analytics of your viewing habits

### Data Management

- **Export**: Click "📤 Export" to save your data as JSON
- **Import**: Click "📥 Import" to restore from a backup file
- **Database**: Your data is stored in `watchlist.db` (SQLite)

## 🛠️ Technical Details

### Architecture

- **GUI Framework**: PyQt6 for modern, cross-platform interface
- **Database**: SQLite for local data storage
- **API Integration**: TMDB API for movie/TV metadata
- **Recommendation Engine**: Custom algorithm analyzing user preferences
- **Charts**: Matplotlib for statistical visualizations

### File Structure

```
ent-sugesstor/
├── main.py                    # Application launcher
├── main_window.py             # Main GUI application
├── database.py                # Database management
├── tmdb_api.py               # TMDB API integration
├── recommendation_engine.py   # Smart recommendation system
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── watchlist.db              # SQLite database (created on first run)
```

### Dependencies

- **PyQt6**: Modern GUI framework
- **requests**: HTTP library for API calls
- **matplotlib**: Plotting and charts
- **numpy**: Numerical computations
- **pandas**: Data manipulation
- **fuzzywuzzy**: Fuzzy string matching
- **python-Levenshtein**: String similarity algorithms

## 🔧 Configuration

### TMDB API Setup

1. Get your free API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Edit `config.py`:
   ```python
   TMDB_API_KEY = "your_actual_api_key_here"
   ```

### Database Location

By default, the database is stored as `watchlist.db` in the application directory. To change this, modify the `DatabaseManager` initialization in `main_window.py`:

```python
self.db = DatabaseManager("path/to/your/database.db")
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- **Bug Reports**: Found a bug? Please create an issue with details
- **Feature Requests**: Have an idea? Let us know!
- **Code Contributions**: Fork the repo and submit a pull request
- **Documentation**: Help improve this README or add code comments

### Development Setup

1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TMDB**: For providing the excellent movie and TV database API
- **PyQt6**: For the powerful GUI framework
- **Python Community**: For the amazing ecosystem of libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check this README for common solutions
2. Look through existing issues in the repository
3. Create a new issue with detailed information about your problem

## 🔮 Future Enhancements

Potential features for future versions:

- **Cloud Sync**: Sync data across multiple devices
- **Social Features**: Share recommendations with friends
- **Advanced Analytics**: More detailed viewing statistics
- **Mobile App**: Companion mobile application
- **Streaming Integration**: Direct links to streaming platforms
- **AI-Powered Reviews**: Automatic review generation
- **Calendar Integration**: Track viewing schedules

---

**Happy watching! 🍿**

*Made with ❤️ for movie and TV enthusiasts*