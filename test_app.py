#!/usr/bin/env python3
"""
Test script for Entertainment Suggester

This script performs basic tests to ensure the application components work correctly.
"""

import sys
import os
import tempfile
from datetime import datetime

def test_database():
    """Test database functionality"""
    print("Testing database functionality...")
    
    try:
        from database import DatabaseManager
        
        # Use temporary database for testing
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db = DatabaseManager(db_path)
        
        # Test adding content
        test_content = {
            'title': 'Test Movie',
            'type': 'movie',
            'genre': 'Action, Drama',
            'language': 'English',
            'rating': 8.5,
            'platform': 'Netflix',
            'date_watched': '2024-01-01',
            'duration': 120,
            'director': 'Test Director',
            'actors': 'Test Actor 1, Test Actor 2',
            'year': 2023,
            'overview': 'A test movie for testing purposes.',
            'status': 'watched'
        }
        
        content_id = db.add_content(test_content)
        print(f"✓ Added test content with ID: {content_id}")
        
        # Test retrieving content
        all_content = db.get_all_content()
        assert len(all_content) == 1
        assert all_content[0]['title'] == 'Test Movie'
        print("✓ Retrieved content successfully")
        
        # Test updating content
        success = db.update_content(content_id, {'rating': 9.0})
        assert success
        updated_content = db.get_all_content()
        assert updated_content[0]['rating'] == 9.0
        print("✓ Updated content successfully")
        
        # Test statistics
        stats = db.get_stats()
        assert stats['total_watched'] == 1
        assert stats['total_hours'] == 2.0  # 120 minutes = 2 hours
        print("✓ Statistics calculated correctly")
        
        # Test export/import
        export_data = db.export_data()
        assert 'content' in export_data
        assert len(export_data['content']) == 1
        print("✓ Export functionality works")
        
        # Clean up
        os.unlink(db_path)
        print("✓ Database tests passed!")
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False
    
    return True

def test_tmdb_api():
    """Test TMDB API functionality"""
    print("\nTesting TMDB API functionality...")
    
    try:
        from tmdb_api import TMDBApi
        from config import is_tmdb_configured
        
        api = TMDBApi()
        
        if not is_tmdb_configured():
            print("⚠ TMDB API key not configured - testing with mock data")
            # Test that methods return empty results gracefully
            results = api.search_content("test")
            assert results == []
            print("✓ API gracefully handles missing key")
        else:
            print("✓ TMDB API key configured")
            # Could add actual API tests here if key is available
        
        # Test data formatting
        mock_movie_data = {
            'id': 123,
            'title': 'Test Movie',
            'genres': [{'name': 'Action'}, {'name': 'Drama'}],
            'original_language': 'en',
            'release_date': '2023-01-01',
            'runtime': 120,
            'overview': 'Test overview',
            'poster_path': '/test.jpg',
            'credits': {
                'crew': [{'name': 'Test Director', 'job': 'Director'}],
                'cast': [{'name': 'Test Actor'}]
            }
        }
        
        formatted = api.format_content_data(mock_movie_data, 'movie')
        assert formatted['title'] == 'Test Movie'
        assert formatted['type'] == 'movie'
        assert 'Action' in formatted['genre']
        print("✓ Data formatting works correctly")
        
        print("✓ TMDB API tests passed!")
        
    except Exception as e:
        print(f"✗ TMDB API test failed: {e}")
        return False
    
    return True

def test_recommendation_engine():
    """Test recommendation engine"""
    print("\nTesting recommendation engine...")
    
    try:
        from database import DatabaseManager
        from tmdb_api import TMDBApi
        from recommendation_engine import RecommendationEngine
        
        # Use temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db = DatabaseManager(db_path)
        api = TMDBApi()
        rec_engine = RecommendationEngine(db, api)
        
        # Add some test data
        test_contents = [
            {
                'title': 'Action Movie 1',
                'type': 'movie',
                'genre': 'Action, Thriller',
                'rating': 8.0,
                'status': 'watched',
                'date_watched': '2024-01-01'
            },
            {
                'title': 'Comedy Show 1',
                'type': 'tv',
                'genre': 'Comedy',
                'rating': 7.5,
                'status': 'watched',
                'date_watched': '2024-01-02'
            }
        ]
        
        for content in test_contents:
            db.add_content(content)
        
        # Test preference calculation
        rec_engine.update_preferences()
        assert len(rec_engine.genre_weights) > 0
        print("✓ Genre preferences calculated")
        
        # Test recommendation generation (will be empty without API key)
        recommendations = rec_engine.get_recommendations(5)
        assert isinstance(recommendations, list)
        print("✓ Recommendations generated (may be empty without API key)")
        
        # Clean up
        os.unlink(db_path)
        print("✓ Recommendation engine tests passed!")
        
    except Exception as e:
        print(f"✗ Recommendation engine test failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import (
            get_tmdb_api_key, is_tmdb_configured, get_database_path,
            get_app_info, DEFAULT_PLATFORMS, DEFAULT_GENRES
        )
        
        # Test configuration functions
        api_key = get_tmdb_api_key()
        configured = is_tmdb_configured()
        db_path = get_database_path()
        app_info = get_app_info()
        
        assert isinstance(configured, bool)
        assert isinstance(db_path, str)
        assert 'name' in app_info
        assert 'version' in app_info
        assert len(DEFAULT_PLATFORMS) > 0
        assert len(DEFAULT_GENRES) > 0
        
        print(f"✓ TMDB configured: {configured}")
        print(f"✓ Database path: {db_path}")
        print(f"✓ App info: {app_info['name']} v{app_info['version']}")
        print("✓ Configuration tests passed!")
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False
    
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing module imports...")
    
    required_modules = [
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'requests',
        'matplotlib.pyplot',
        'numpy',
        'pandas',
        'fuzzywuzzy'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠ Missing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All required modules available!")
    return True

def main():
    """Run all tests"""
    print("Entertainment Suggester - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_tmdb_api,
        test_recommendation_engine
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        return 0
    else:
        print("⚠ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())