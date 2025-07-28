import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import get_tmdb_api_key

class TMDBApi:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_tmdb_api_key()
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    def search_content(self, query: str, content_type: str = "multi") -> List[Dict]:
        """Search for movies or TV shows"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/search/{content_type}"
        params = {
            "api_key": self.api_key,
            "query": query,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return []
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a movie"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "append_to_response": "credits"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return None
    
    def get_tv_details(self, tv_id: int) -> Optional[Dict]:
        """Get detailed information about a TV show"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/tv/{tv_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "append_to_response": "credits"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return None
    
    def get_recommendations(self, content_id: int, content_type: str) -> List[Dict]:
        """Get recommendations based on a specific movie or TV show"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/{content_type}/{content_id}/recommendations"
        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return []
    
    def get_trending(self, media_type: str = "all", time_window: str = "week") -> List[Dict]:
        """Get trending movies and TV shows"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/trending/{media_type}/{time_window}"
        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return []
    
    def get_discover(self, content_type: str, genres: List[int] = None, year: int = None) -> List[Dict]:
        """Discover movies or TV shows based on criteria"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/discover/{content_type}"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "sort_by": "popularity.desc"
        }
        
        if genres:
            params["with_genres"] = ",".join(map(str, genres))
        if year:
            if content_type == "movie":
                params["year"] = year
            else:
                params["first_air_date_year"] = year
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return []
    
    def format_content_data(self, tmdb_data: Dict, content_type: str) -> Dict:
        """Format TMDB data for our database"""
        if content_type == "movie":
            return {
                "title": tmdb_data.get("title", ""),
                "type": "movie",
                "genre": ", ".join([g["name"] for g in tmdb_data.get("genres", [])]),
                "language": tmdb_data.get("original_language", ""),
                "year": int(tmdb_data.get("release_date", "0000")[:4]) if tmdb_data.get("release_date") else None,
                "duration": tmdb_data.get("runtime"),
                "director": self._get_director(tmdb_data.get("credits", {})),
                "actors": self._get_main_actors(tmdb_data.get("credits", {})),
                "tmdb_id": tmdb_data.get("id"),
                "poster_url": f"{self.image_base_url}{tmdb_data.get('poster_path')}" if tmdb_data.get("poster_path") else None,
                "overview": tmdb_data.get("overview", "")
            }
        else:  # TV show
            return {
                "title": tmdb_data.get("name", ""),
                "type": "tv",
                "genre": ", ".join([g["name"] for g in tmdb_data.get("genres", [])]),
                "language": tmdb_data.get("original_language", ""),
                "year": int(tmdb_data.get("first_air_date", "0000")[:4]) if tmdb_data.get("first_air_date") else None,
                "duration": tmdb_data.get("episode_run_time", [0])[0] if tmdb_data.get("episode_run_time") else None,
                "director": self._get_creator(tmdb_data),
                "actors": self._get_main_actors(tmdb_data.get("credits", {})),
                "tmdb_id": tmdb_data.get("id"),
                "poster_url": f"{self.image_base_url}{tmdb_data.get('poster_path')}" if tmdb_data.get("poster_path") else None,
                "overview": tmdb_data.get("overview", "")
            }
    
    def _get_director(self, credits: Dict) -> str:
        """Extract director from credits"""
        crew = credits.get("crew", [])
        directors = [person["name"] for person in crew if person.get("job") == "Director"]
        return ", ".join(directors[:3])  # Limit to 3 directors
    
    def _get_creator(self, tmdb_data: Dict) -> str:
        """Extract creator from TV show data"""
        creators = tmdb_data.get("created_by", [])
        return ", ".join([creator["name"] for creator in creators[:3]])
    
    def _get_main_actors(self, credits: Dict) -> str:
        """Extract main actors from credits"""
        cast = credits.get("cast", [])
        main_actors = [actor["name"] for actor in cast[:5]]  # Top 5 actors
        return ", ".join(main_actors)
    
    def get_genre_mapping(self) -> Dict[int, str]:
        """Get genre ID to name mapping"""
        if not self.api_key:
            return {}
        
        genre_map = {}
        
        # Get movie genres
        try:
            url = f"{self.base_url}/genre/movie/list"
            params = {"api_key": self.api_key, "language": "en-US"}
            response = requests.get(url, params=params)
            response.raise_for_status()
            movie_genres = response.json().get("genres", [])
            
            # Get TV genres
            url = f"{self.base_url}/genre/tv/list"
            response = requests.get(url, params=params)
            response.raise_for_status()
            tv_genres = response.json().get("genres", [])
            
            # Combine both
            all_genres = movie_genres + tv_genres
            for genre in all_genres:
                genre_map[genre["id"]] = genre["name"]
                
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
        
        return genre_map