from db_connection import get_astra_session
from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_post_type_metrics(days: int = 30) -> List[Dict[str, Any]]:
    """Get metrics grouped by post type for the last N days"""
    try:
        session, _ = get_astra_session()
        if not session:
            logger.error("Failed to establish database connection")
            return generate_mock_data()

        # Calculate the timestamp for N days ago
        start_date = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        # Query posts
        result = session.execute(
            "SELECT * FROM social_media_posts WHERE created_at >= ?",
            {"created_at": start_date}
        )
        
        if not result or 'data' not in result:
            logger.warning("No data returned from database")
            return generate_mock_data()

        # Process the results
        metrics_by_type = defaultdict(lambda: {
            'post_type': '',
            'total_posts': 0,
            'avg_likes': 0,
            'avg_comments': 0,
            'avg_shares': 0,
            'avg_reach': 0,
            'avg_impressions': 0,
            'avg_engagement': 0,
            'avg_ctr': 0,
            'avg_watch_time': 0
        })

        for post in result.get('data', []):
            post_type = post.get('post_type', 'unknown')
            metrics = metrics_by_type[post_type]
            metrics['post_type'] = post_type
            metrics['total_posts'] += 1
            metrics['avg_likes'] += post.get('likes', 0)
            metrics['avg_comments'] += post.get('comments', 0)
            metrics['avg_shares'] += post.get('shares', 0)
            metrics['avg_reach'] += post.get('reach', 0)
            metrics['avg_impressions'] += post.get('impressions', 0)
            metrics['avg_engagement'] += post.get('engagement', 0)
            metrics['avg_ctr'] += post.get('click_through_rate', 0)
            metrics['avg_watch_time'] += post.get('watch_time', 0)

        # Calculate averages
        for metrics in metrics_by_type.values():
            total_posts = metrics['total_posts']
            if total_posts > 0:
                for key in metrics:
                    if key != 'post_type' and key != 'total_posts':
                        metrics[key] = round(metrics[key] / total_posts, 2)

        return list(metrics_by_type.values())

    except Exception as e:
        logger.error(f"Error fetching post metrics: {str(e)}")
        return generate_mock_data()

def get_trending_hashtags(limit: int = 5) -> List[Dict[str, Any]]:
    """Get trending hashtags based on engagement"""
    try:
        session, _ = get_astra_session()
        if not session:
            logger.error("Failed to establish database connection")
            return generate_mock_hashtags()

        # Query hashtags
        result = session.execute("SELECT * FROM post_hashtags")
        
        if not result or 'data' not in result:
            logger.warning("No hashtag data returned from database")
            return generate_mock_hashtags()

        # Process the results
        hashtag_stats = defaultdict(lambda: {
            'hashtag': '',
            'usage_count': 0,
            'total_engagement': 0,
            'avg_engagement': 0
        })

        for hashtag_data in result.get('data', []):
            hashtag = hashtag_data.get('hashtag', '')
            if not hashtag:
                continue
                
            stats = hashtag_stats[hashtag]
            stats['hashtag'] = hashtag
            stats['usage_count'] += 1
            stats['total_engagement'] += hashtag_data.get('engagement', 0)

        # Calculate averages and prepare final list
        trending_hashtags = []
        for stats in hashtag_stats.values():
            if stats['usage_count'] > 0:
                stats['avg_engagement'] = round(stats['total_engagement'] / stats['usage_count'], 2)
                trending_hashtags.append(stats)

        # Sort by engagement and limit results
        return sorted(trending_hashtags, key=lambda x: x['avg_engagement'], reverse=True)[:limit]

    except Exception as e:
        logger.error(f"Error fetching trending hashtags: {str(e)}")
        return generate_mock_hashtags()

def generate_mock_data() -> List[Dict[str, Any]]:
    """Generate mock data for testing"""
    return [
        {
            'post_type': 'photo',
            'total_posts': 40,
            'avg_likes': 120,
            'avg_comments': 25,
            'avg_shares': 15,
            'avg_reach': 1200,
            'avg_impressions': 1500,
            'avg_engagement': 10.5,
            'avg_ctr': 3.2,
            'avg_watch_time': 0
        },
        {
            'post_type': 'video',
            'total_posts': 30,
            'avg_likes': 180,
            'avg_comments': 35,
            'avg_shares': 25,
            'avg_reach': 1800,
            'avg_impressions': 2200,
            'avg_engagement': 12.8,
            'avg_ctr': 4.1,
            'avg_watch_time': 45.5
        },
        {
            'post_type': 'text',
            'total_posts': 30,
            'avg_likes': 75,
            'avg_comments': 15,
            'avg_shares': 8,
            'avg_reach': 800,
            'avg_impressions': 1000,
            'avg_engagement': 8.2,
            'avg_ctr': 2.8,
            'avg_watch_time': 0
        }
    ]

def generate_mock_hashtags() -> List[Dict[str, Any]]:
    """Generate mock hashtag data for testing"""
    return [
        {'hashtag': 'tech', 'usage_count': 25, 'total_engagement': 1250, 'avg_engagement': 50.0},
        {'hashtag': 'ai', 'usage_count': 20, 'total_engagement': 900, 'avg_engagement': 45.0},
        {'hashtag': 'innovation', 'usage_count': 15, 'total_engagement': 600, 'avg_engagement': 40.0},
        {'hashtag': 'future', 'usage_count': 12, 'total_engagement': 420, 'avg_engagement': 35.0},
        {'hashtag': 'coding', 'usage_count': 10, 'total_engagement': 300, 'avg_engagement': 30.0}
    ] 