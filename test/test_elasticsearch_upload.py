from mastodon import Mastodon
import json
import time
import logging
from elasticsearch8 import Elasticsearch
def test_elasticsearch_upload():
    logging.basicConfig(level=logging.INFO)
    m = Mastodon(api_base_url='https://mastodon.au')
    es_client = Elasticsearch(
        'https://127.0.0.1:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    
    test_doc = {
        "id": "111111111111111",
        "created_at": "2023-10-01T12:00:00Z",
        "url": "https://mastodon.au/@test/1234567890",
        "content": "This is a test Mastodon post.",
        "author_username": "test_user",
        "author_display_name": "test_user",
        "tags": ["test", "AI"],
        "media_urls": []
    }
    
    res = es_client.index(index="mastodon_ai", id="111111111111111", body=test_doc)
    print(f" Upload status: {res['result']}")