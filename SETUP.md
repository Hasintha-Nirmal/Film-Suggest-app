# Quick Setup Guide 🚀

This guide will help you get Entertainment Suggester up and running in just a few minutes!

## 📋 Prerequisites

- **Python 3.8 or higher** ([Download here](https://python.org/downloads/))
- **Internet connection** (for TMDB API and package installation)
- **Windows, macOS, or Linux**

## 🔧 Installation

### Option 1: Automatic Setup (Recommended)

**Windows:**
```bash
# Double-click run_app.bat or run in Command Prompt:
run_app.bat
```

**macOS/Linux:**
```bash
# Make the script executable and run:
chmod +x run_app.sh
./run_app.sh
```

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## 🔑 TMDB API Setup (Optional but Recommended)

For automatic movie/TV show metadata and better recommendations:

1. **Get a free API key:**
   - Go to [TMDB](https://www.themoviedb.org/)
   - Create a free account
   - Go to Settings → API
   - Request an API key (choose "Developer")

2. **Configure the key:**
   - Open `config.py` in a text editor
   - Replace `YOUR_TMDB_API_KEY_HERE` with your actual API key
   - Save the file

   ```python
   # In config.py
   TMDB_API_KEY = "your_actual_api_key_here"
   ```

## 🎬 First Steps

1. **Start the application** using one of the methods above
2. **Add your first movie/show:**
   - Click "➕ Add Content" in the Watched tab
   - Search for a title (if TMDB is configured) or enter manually
   - Fill in your rating and platform
   - Click "OK"

3. **Explore features:**
   - **📺 Watched:** View and manage your watched content
   - **📋 Watchlist:** Keep track of what you want to watch
   - **🎯 Recommendations:** Get personalized suggestions
   - **📊 Statistics:** See your viewing analytics

## 🔧 Troubleshooting

### Common Issues

**"Python is not recognized"**
- Make sure Python is installed and added to your system PATH
- Try using `python3` instead of `python`

**"No module named 'PyQt6'"**
- Run: `pip install -r requirements.txt`
- If using conda: `conda install pyqt`

**"TMDB API error"**
- Check your internet connection
- Verify your API key is correct in `config.py`
- The app works without API key, just with limited features

**Application won't start**
- Check Python version: `python --version` (needs 3.8+)
- Try running: `python test_app.py` to diagnose issues

### Getting Help

1. **Check the main README.md** for detailed documentation
2. **Run the test script:** `python test_app.py`
3. **Check error messages** in the terminal/command prompt
4. **Create an issue** in the repository with error details

## 🎯 Quick Tips

- **Use search:** When adding content, use the search feature to auto-fill details
- **Rate everything:** Your ratings help generate better recommendations
- **Check recommendations:** Visit the Recommendations tab after adding several rated items
- **Export regularly:** Use the Export feature to backup your data
- **Explore statistics:** The Statistics tab shows interesting insights about your viewing habits

## 📱 Usage Examples

### Adding a Movie
1. Click "➕ Add Content"
2. Type "The Matrix" in search box
3. Click "Search" (auto-fills details)
4. Set your rating: 9.0
5. Select platform: "Netflix"
6. Click "OK"

### Getting Recommendations
1. Add and rate at least 3-5 movies/shows
2. Go to "🎯 Recommendations" tab
3. Click "Refresh" to get new suggestions
4. Click "Add to Watchlist" for interesting recommendations

### Viewing Statistics
1. Go to "📊 Statistics" tab
2. See your total hours watched, favorite genres, etc.
3. View the genre distribution chart

---

**That's it! You're ready to start tracking and discovering great content! 🍿**

For more detailed information, see the main [README.md](README.md) file.