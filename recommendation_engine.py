import sqlite3
import json
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re
from fuzzywuzzy import fuzz
from tmdb_api import TMDBApi

class RecommendationEngine:
    def __init__(self, db_manager, tmdb_api: TMDBApi):
        self.db = db_manager
        self.tmdb = tmdb_api
        self.genre_weights = self._calculate_genre_preferences()
        self.rating_threshold = 7.0  # Minimum rating to consider as "liked"
    
    def _calculate_genre_preferences(self) -> Dict[str, float]:
        """Calculate user's genre preferences based on watch history and ratings"""
        content = self.db.get_all_content(status='watched')
        genre_scores = defaultdict(list)
        
        for item in content:
            if item['genre'] and item['rating']:
                genres = [g.strip() for g in item['genre'].split(',')]
                for genre in genres:
                    genre_scores[genre].append(float(item['rating']))
        
        # Calculate weighted preferences
        preferences = {}
        for genre, ratings in genre_scores.items():
            avg_rating = sum(ratings) / len(ratings)
            watch_count = len(ratings)
            # Weight by both average rating and frequency
            preferences[genre] = (avg_rating * 0.7) + (min(watch_count / 10, 1.0) * 0.3)
        
        return preferences
    
    def get_recommendations(self, limit: int = 10) -> List[Dict]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Get recommendations from different sources
        recommendations.extend(self._get_genre_based_recommendations(limit // 3))
        recommendations.extend(self._get_similar_content_recommendations(limit // 3))
        recommendations.extend(self._get_trending_recommendations(limit // 3))
        
        # Remove duplicates and sort by score
        seen_titles = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['title'] not in seen_titles:
                seen_titles.add(rec['title'])
                unique_recommendations.append(rec)
        
        # Sort by score and return top recommendations
        unique_recommendations.sort(key=lambda x: x['score'], reverse=True)
        return unique_recommendations[:limit]
    
    def _get_genre_based_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations based on favorite genres"""
        recommendations = []
        
        # Get top genres
        top_genres = sorted(self.genre_weights.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for genre, weight in top_genres:
            # Get genre ID from TMDB
            genre_map = self.tmdb.get_genre_mapping()
            genre_id = None
            for gid, gname in genre_map.items():
                if gname.lower() == genre.lower():
                    genre_id = gid
                    break
            
            if genre_id:
                # Get movies and TV shows for this genre
                movies = self.tmdb.get_discover('movie', genres=[genre_id])
                tv_shows = self.tmdb.get_discover('tv', genres=[genre_id])
                
                for content in (movies + tv_shows)[:3]:  # Limit per genre
                    if not self._is_already_watched(content):
                        rec = self._format_recommendation(
                            content,
                            f"You enjoy {genre} content (avg rating: {weight:.1f})",
                            weight * 0.8
                        )
                        recommendations.append(rec)
        
        return recommendations
    
    def _get_similar_content_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations based on highly rated content"""
        recommendations = []
        
        # Get highly rated content
        watched_content = self.db.get_all_content(status='watched')
        highly_rated = [c for c in watched_content if c['rating'] and float(c['rating']) >= self.rating_threshold]
        
        # Sort by rating and get top items
        highly_rated.sort(key=lambda x: float(x['rating']), reverse=True)
        
        for content in highly_rated[:5]:  # Top 5 highly rated
            if content['tmdb_id']:
                content_type = 'movie' if content['type'] == 'movie' else 'tv'
                similar = self.tmdb.get_recommendations(content['tmdb_id'], content_type)
                
                for similar_content in similar[:2]:  # 2 recommendations per highly rated item
                    if not self._is_already_watched(similar_content):
                        reason = f"You rated '{content['title']}' {content['rating']}/10"
                        if content['director'] and similar_content.get('director'):
                            if self._has_common_people(content['director'], similar_content.get('director', '')):
                                reason += " - same director"
                        
                        rec = self._format_recommendation(
                            similar_content,
                            reason,
                            float(content['rating']) * 0.1
                        )
                        recommendations.append(rec)
        
        return recommendations
    
    def _get_trending_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations from trending content that matches user preferences"""
        recommendations = []
        
        trending = self.tmdb.get_trending('all', 'week')
        
        for content in trending:
            if not self._is_already_watched(content):
                # Check if genres match user preferences
                content_genres = content.get('genre_ids', [])
                genre_map = self.tmdb.get_genre_mapping()
                
                score = 0
                matching_genres = []
                
                for genre_id in content_genres:
                    genre_name = genre_map.get(genre_id, '')
                    if genre_name in self.genre_weights:
                        score += self.genre_weights[genre_name]
                        matching_genres.append(genre_name)
                
                if score > 0:  # Only recommend if there's genre overlap
                    reason = f"Trending this week"
                    if matching_genres:
                        reason += f" - matches your interest in {', '.join(matching_genres[:2])}"
                    
                    rec = self._format_recommendation(
                        content,
                        reason,
                        score * 0.6 + 0.3  # Trending bonus
                    )
                    recommendations.append(rec)
        
        return recommendations[:limit]
    
    def _is_already_watched(self, tmdb_content: Dict) -> bool:
        """Check if content is already in user's watch list"""
        watched_content = self.db.get_all_content()
        
        # Check by TMDB ID first
        tmdb_id = tmdb_content.get('id')
        if tmdb_id:
            for content in watched_content:
                if content['tmdb_id'] == tmdb_id:
                    return True
        
        # Check by title similarity
        title = tmdb_content.get('title') or tmdb_content.get('name', '')
        for content in watched_content:
            if fuzz.ratio(title.lower(), content['title'].lower()) > 85:
                return True
        
        return False
    
    def _format_recommendation(self, tmdb_content: Dict, reason: str, score: float) -> Dict:
        """Format TMDB content as recommendation"""
        content_type = 'movie' if 'title' in tmdb_content else 'tv'
        title = tmdb_content.get('title') or tmdb_content.get('name', '')
        
        return {
            'title': title,
            'type': content_type,
            'reason': reason,
            'score': score,
            'tmdb_id': tmdb_content.get('id'),
            'poster_url': f"{self.tmdb.image_base_url}{tmdb_content.get('poster_path')}" if tmdb_content.get('poster_path') else None,
            'overview': tmdb_content.get('overview', ''),
            'year': self._extract_year(tmdb_content),
            'rating': tmdb_content.get('vote_average', 0)
        }
    
    def _extract_year(self, tmdb_content: Dict) -> int:
        """Extract year from TMDB content"""
        date_field = tmdb_content.get('release_date') or tmdb_content.get('first_air_date', '')
        if date_field:
            try:
                return int(date_field[:4])
            except (ValueError, IndexError):
                pass
        return None
    
    def _has_common_people(self, people1: str, people2: str) -> bool:
        """Check if two people strings have common names"""
        if not people1 or not people2:
            return False
        
        names1 = set(name.strip().lower() for name in people1.split(','))
        names2 = set(name.strip().lower() for name in people2.split(','))
        
        return bool(names1.intersection(names2))
    
    def get_content_suggestions_by_title(self, title: str, limit: int = 5) -> List[Dict]:
        """Get suggestions when user searches for a specific title"""
        search_results = self.tmdb.search_content(title)
        suggestions = []
        
        for result in search_results[:limit]:
            if not self._is_already_watched(result):
                content_type = 'movie' if 'title' in result else 'tv'
                formatted = self._format_recommendation(
                    result,
                    "Search result",
                    result.get('vote_average', 0) / 10
                )
                suggestions.append(formatted)
        
        return suggestions
    
    def update_preferences(self):
        """Update genre preferences based on latest watch history"""
        self.genre_weights = self._calculate_genre_preferences()
    
    def get_recommendation_explanation(self, content_title: str) -> str:
        """Get detailed explanation for why content was recommended"""
        # This could be expanded to provide more detailed explanations
        # based on the recommendation algorithm used
        return f"Recommended based on your viewing history and preferences"