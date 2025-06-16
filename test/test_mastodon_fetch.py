from mastodon import Mastodon
import logging

def test_mastodon_fetch():
    logging.basicConfig(level=logging.INFO)
    
    try:
        m = Mastodon(api_base_url='https://mastodon.au')

        posts = m.timeline_hashtag(hashtag="AI", limit=5)

        if posts and isinstance(posts, list):
            print(f"✅ successfully fetch {len(posts)} Mastodon posts with hashtag 'AI'")
            for i, post in enumerate(posts):
                print(f"{i+1}. @{post['account']['username']}: {post['content'][:50]}...")
        else:
            print("No posts were obtained")
    except Exception as e:
        print(f"error message: {e}")