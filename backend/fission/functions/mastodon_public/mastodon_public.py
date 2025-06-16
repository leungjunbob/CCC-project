from mastodon import Mastodon
import json
import time
import logging
from elasticsearch8 import Elasticsearch



def main() -> str:
    logging.basicConfig(level=logging.INFO)
    start_time = time.time()
    m = Mastodon(api_base_url='https://mastodon.au')
    es_client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    last_id = get_last_id(es_client)
    all_posts = []
    
    page = 0
    MAX_POSTS = 1000

    while len(all_posts) < MAX_POSTS:
        posts = m.timeline_public(
            limit=40,
            max_id=last_id
        )
        if not posts:
            break

        all_posts.extend(posts)
        last_id = posts[-1]['id']
        page += 1
        logging.info(f'Fetched page {page}, total posts so far: {len(all_posts)}')
        time.sleep(1)  # comply with rate limit
    cleaned_posts = [extract_main_info(p) for p in all_posts]
    success = 0
    for post in cleaned_posts :
        try:
            es_client.index(index="mastodon_public", id=post["id"], body=post)
            success += 1
        except Exception as e:
            logging.error(f" Failed to index {post['id']}: {str(e)}")
    if last_id:
        save_last_id(es_client, last_id)
    elapsed_time = time.time() - start_time

    return f"Indexed {success} posts to mastodon_public in {elapsed_time:.2f} seconds"
     

def extract_main_info(post):
    return {
        "id": post.get("id"),
        "created_at": post.get("created_at"),
        "url": post.get("url"),
        "content": post.get("content", ""),
        "author_username": post.get("account", {}).get("username"),
        "author_display_name": post.get("account", {}).get("display_name"),
        "tags": [tag["name"] for tag in post.get("tags", [])],
        "media_urls": [media["url"] for media in post.get("media_attachments", []) if media.get("type") == "image"]
    }

def get_last_id(es_client):
    try:
        res = es_client.get(index="mastodon_public_last_id", id="last_id")
        return res["_source"]["last_id"]
    except Exception:
        return None  # first time fetching



def save_last_id(es_client, last_id):
    es_client.index(
        index="mastodon_public_last_id",
        id="last_id",
        body={
            "last_id": last_id
           
        }
    )






