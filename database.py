import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "watchlist.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Movies and TV shows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('movie', 'tv')),
                genre TEXT,
                language TEXT,
                rating REAL,
                platform TEXT,
                date_watched TEXT,
                duration INTEGER,
                director TEXT,
                actors TEXT,
                year INTEGER,
                tmdb_id INTEGER,
                poster_url TEXT,
                overview TEXT,
                status TEXT DEFAULT 'watched' CHECK (status IN ('watched', 'want_to_watch')),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT,
                weight REAL DEFAULT 1.0,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Recommendations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                reason TEXT,
                score REAL,
                tmdb_id INTEGER,
                poster_url TEXT,
                overview TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_content(self, content_data: Dict) -> int:
        """Add a movie or TV show to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO content (
                title, type, genre, language, rating, platform, date_watched,
                duration, director, actors, year, tmdb_id, poster_url, overview, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            content_data.get('title'),
            content_data.get('type'),
            content_data.get('genre'),
            content_data.get('language'),
            content_data.get('rating'),
            content_data.get('platform'),
            content_data.get('date_watched'),
            content_data.get('duration'),
            content_data.get('director'),
            content_data.get('actors'),
            content_data.get('year'),
            content_data.get('tmdb_id'),
            content_data.get('poster_url'),
            content_data.get('overview'),
            content_data.get('status', 'watched')
        ))
        
        content_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return content_id
    
    def get_all_content(self, status: str = None) -> List[Dict]:
        """Get all content from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM content WHERE status = ? ORDER BY date_watched DESC", (status,))
        else:
            cursor.execute("SELECT * FROM content ORDER BY date_watched DESC")
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def update_content(self, content_id: int, content_data: Dict) -> bool:
        """Update content in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ", ".join([f"{key} = ?" for key in content_data.keys()])
        values = list(content_data.values()) + [content_id]
        
        cursor.execute(f"UPDATE content SET {set_clause} WHERE id = ?", values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_content(self, content_id: int) -> bool:
        """Delete content from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM content WHERE id = ?", (content_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_stats(self) -> Dict:
        """Get viewing statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Most watched genre
        cursor.execute("""
            SELECT genre, COUNT(*) as count 
            FROM content 
            WHERE status = 'watched' AND genre IS NOT NULL
            GROUP BY genre 
            ORDER BY count DESC 
            LIMIT 1
        """)
        top_genre = cursor.fetchone()
        
        # Total hours watched
        cursor.execute("""
            SELECT SUM(duration) as total_minutes 
            FROM content 
            WHERE status = 'watched' AND duration IS NOT NULL
        """)
        total_minutes = cursor.fetchone()[0] or 0
        total_hours = total_minutes / 60
        
        # Total content watched
        cursor.execute("SELECT COUNT(*) FROM content WHERE status = 'watched'")
        total_watched = cursor.fetchone()[0]
        
        # Average rating
        cursor.execute("""
            SELECT AVG(rating) as avg_rating 
            FROM content 
            WHERE status = 'watched' AND rating IS NOT NULL
        """)
        avg_rating = cursor.fetchone()[0] or 0
        
        # Genre distribution
        cursor.execute("""
            SELECT genre, COUNT(*) as count 
            FROM content 
            WHERE status = 'watched' AND genre IS NOT NULL
            GROUP BY genre 
            ORDER BY count DESC
        """)
        genre_distribution = cursor.fetchall()
        
        conn.close()
        
        return {
            'top_genre': top_genre[0] if top_genre else 'N/A',
            'total_hours': round(total_hours, 1),
            'total_watched': total_watched,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'genre_distribution': genre_distribution
        }
    
    def export_data(self) -> Dict:
        """Export all data for backup"""
        return {
            'content': self.get_all_content(),
            'export_date': datetime.now().isoformat()
        }
    
    def import_data(self, data: Dict) -> bool:
        """Import data from backup"""
        try:
            for content in data.get('content', []):
                # Remove id to avoid conflicts
                content_copy = content.copy()
                content_copy.pop('id', None)
                content_copy.pop('created_at', None)
                self.add_content(content_copy)
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False