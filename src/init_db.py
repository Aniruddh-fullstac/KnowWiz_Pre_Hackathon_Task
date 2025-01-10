from db_connection import get_astra_session, execute_schema
import logging
from datetime import datetime, timedelta
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables(session) -> bool:
    """Create the required tables in the database"""
    try:
        # Create social_media_posts table
        posts_table = """
        CREATE TABLE IF NOT EXISTS social_media_posts (
            id uuid PRIMARY KEY,
            post_type text,
            content text,
            created_at timestamp,
            likes int,
            comments int,
            shares int,
            reach int,
            impressions int,
            engagement float,
            click_through_rate float,
            watch_time float
        )
        """
        if not execute_schema(session, posts_table):
            logger.error("Failed to create social_media_posts table")
            return False

        # Create post_hashtags table
        hashtags_table = """
        CREATE TABLE IF NOT EXISTS post_hashtags (
            post_id uuid,
            hashtag text,
            created_at timestamp,
            engagement float,
            PRIMARY KEY (post_id, hashtag)
        )
        """
        if not execute_schema(session, hashtags_table):
            logger.error("Failed to create post_hashtags table")
            return False

        logger.info("Successfully created database tables")
        return True

    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        return False

def insert_sample_data(session) -> bool:
    """Insert sample data into the database"""
    try:
        # Sample post types and their characteristics
        post_types = ['photo', 'video', 'text']
        base_metrics = {
            'photo': {'likes': 100, 'comments': 20, 'shares': 15},
            'video': {'likes': 150, 'comments': 30, 'shares': 25},
            'text': {'likes': 50, 'comments': 10, 'shares': 5}
        }

        # Sample hashtags
        hashtags = ['tech', 'ai', 'innovation', 'future', 'coding']

        # Generate posts for the last 30 days
        now = datetime.now()
        for i in range(30):
            for post_type in post_types:
                # Create post
                post_id = uuid.uuid4()
                created_at = now - timedelta(days=i, hours=i%24)
                
                # Add some randomness to metrics
                metrics = base_metrics[post_type].copy()
                engagement = (metrics['likes'] + metrics['comments'] * 2 + metrics['shares'] * 3) / 100
                
                post_query = """
                INSERT INTO social_media_posts (
                    id, post_type, content, created_at, likes, comments, shares,
                    reach, impressions, engagement, click_through_rate, watch_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                session.execute(post_query, (
                    post_id,
                    post_type,
                    f"Sample {post_type} post content",
                    created_at,
                    metrics['likes'],
                    metrics['comments'],
                    metrics['shares'],
                    metrics['likes'] * 10,  # reach
                    metrics['likes'] * 12,  # impressions
                    engagement,
                    engagement * 0.3,  # click_through_rate
                    45.0 if post_type == 'video' else 0.0  # watch_time
                ))

                # Add hashtags for this post
                for hashtag in hashtags[:3]:  # Use first 3 hashtags for each post
                    hashtag_query = """
                    INSERT INTO post_hashtags (post_id, hashtag, created_at, engagement)
                    VALUES (%s, %s, %s, %s)
                    """
                    session.execute(hashtag_query, (
                        post_id,
                        hashtag,
                        created_at,
                        engagement
                    ))

        logger.info("Successfully inserted sample data")
        return True

    except Exception as e:
        logger.error(f"Error inserting sample data: {str(e)}")
        return False

def main():
    """Initialize the database with tables and sample data"""
    try:
        # Get database session
        session, cluster = get_astra_session()
        if not session:
            logger.error("Failed to establish database connection")
            return

        # Create tables
        if not create_tables(session):
            logger.error("Failed to create tables")
            return

        # Insert sample data
        if not insert_sample_data(session):
            logger.error("Failed to insert sample data")
            return

        logger.info("Database initialization completed successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

    finally:
        if cluster:
            cluster.shutdown()

if __name__ == "__main__":
    main() 