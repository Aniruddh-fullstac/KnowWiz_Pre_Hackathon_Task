from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import uuid
from datetime import datetime, timedelta
import random

# Load token from JSON file
with open('social-media-analytics-token.json', 'r') as f:
    token_data = json.load(f)

# Configure cloud connection
cloud_config = {
    'secure_connect_bundle': 'secure-connect-social-media-analytics.zip'
}

# Use token-based authentication
auth_provider = PlainTextAuthProvider(
    token_data['clientId'],
    token_data['token']
)

# Connect to the cluster
print("Connecting to cluster...")
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Set the keyspace
keyspace = "social_media_analytics"
print(f"Using keyspace: {keyspace}")
session.set_keyspace(keyspace)

# Prepare mock data
post_types = ['carousel', 'reel', 'static']
now = datetime.now()

# Create mock posts
for i in range(30):  # Create 30 mock posts
    post_type = random.choice(post_types)
    post_id = uuid.uuid4()
    created_at = now - timedelta(days=random.randint(0, 30))
    
    # Insert post
    insert_query = """
    INSERT INTO social_media_posts (post_id, post_type, created_at)
    VALUES (%s, %s, %s)
    """
    session.execute(insert_query, (post_id, post_type, created_at))
    
    # Update counters with random engagement numbers
    likes = random.randint(50, 1000)
    shares = random.randint(10, 200)
    comments = random.randint(5, 100)
    
    update_query = """
    UPDATE social_media_posts
    SET likes = likes + ?, shares = shares + ?, comments = comments + ?
    WHERE post_id = ?
    """
    session.execute(update_query, (likes, shares, comments, post_id))
    print(f"Inserted post {i+1}/30: {post_type} with {likes} likes, {shares} shares, {comments} comments")

print("\nMock data insertion complete!")

# Verify data
print("\nSample of inserted data:")
rows = session.execute("SELECT * FROM social_media_posts LIMIT 5")
for row in rows:
    print(row)

cluster.shutdown() 