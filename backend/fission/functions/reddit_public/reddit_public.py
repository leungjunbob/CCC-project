import json
import time
import logging
from elasticsearch8 import Elasticsearch
import praw
import datetime


def main() -> str:
    logging.basicConfig(level=logging.INFO)
    reddit = praw.Reddit(
        client_id='MGoZRwTjWkAxFf6UyxanYw',
        client_secret='Z2sHgoR0IlJhRKrY3KXbqhnswD3V7Q',
        user_agent='soap drama (by /u/Ok_Candidate9451)',
        username='Ok_Candidate9451',
        password='Aa112233'
    )
   
    es_client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    
    subreddits = [ 'australia', 'australian','AustralianPolitics', 'auslegal', 'AustralianNSFW',
                  'brisbane', 'sydney', 'melbourne', 'adelaide', 'perth', 'hobart',
                  'canberra', 'Darwin', 'AusFinance', 'AFL', 'nrl']
    POST_LIMIT = 50
    all_items = []
    for sub in subreddits:
        print(f" fetchinng {sub} now")
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.new(limit=POST_LIMIT):
                all_items.append({
                    'subreddit': sub,
                    'id': post.id,
                    'created_utc': datetime.datetime.fromtimestamp(post.created_utc).isoformat(),
                    'title': post.title,
                    'content': post.selftext,
                    'author': str(post.author),
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'depth': 0
                })
                print(f"fetch {len(all_items)} posts")
                
            print(f"Completed {sub} fetch.")
            time.sleep(1)  # comply with rate limit

        except Exception as e:
            print(f" Error fetching {sub}: {e}")

    success = 0
    for post in all_items:
        try:
            es_client.index(index="reddit_public", id=post["id"], body=post)
            success += 1
        except Exception as e:
            logging.error(f" Failed to index {post['id']}: {str(e)}")

    return f" Indexed {success} posts to reddit_public"


