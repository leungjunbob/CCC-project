import warnings
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

def main(database, start_time, end_time, keyword):

    # 1 Connect to Elasticsearch
    # es = Elasticsearch(
    #     "https://localhost:9200",
    #     basic_auth=("elastic", "elastic"),
    #     verify_certs=False          
    # )
    es = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        basic_auth=("elastic", "elastic"),
        verify_certs=False          
    )   

    for index_name in database:
        filter_tag  = keyword        # Only analyze posts with this tag
        top_n = 10          # Display the top 10 active users, which can be adjusted as needed

        warnings.filterwarnings("ignore")

        post_counter   = Counter()             # Count the number of posts by users
        display_lookup = defaultdict(Counter)  # Count the nicknames used
        tag_lookup     = defaultdict(Counter)  # Count the frequency of tags
        all_dates      = []                    # Post time

        # 2 Scanning the Index
        docs = scan(
            es,
            index=index_name,
            query={"query": {"match": {"tags": filter_tag}}},
            _source=["author_username", "author_display_name", "tags", "created_at"],
            size=5000,
            preserve_order=False
        )

        for doc in tqdm(docs, desc="Scanning the Index"):
            src  = doc["_source"]
            # Convert timestamp to pandas datetime
            timestamp = pd.to_datetime(src["created_at"], errors="coerce", utc=True)
            if pd.notna(timestamp):
                all_dates.append(timestamp)

            user = src.get("author_username")
            if not user:
                continue
            post_counter[user] += 1
            nick = (src.get("author_display_name") or "").strip()
            if nick:
                display_lookup[user][nick] += 1
            tags = src.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            tag_lookup[user].update([t.lower() for t in tags])

        # 3 Output top-n active user portraits
        top_users = []
        # print(f"{'Username':<25} {'Nick name':<25} {'Number of posts':<25} {'Top3 tag':<50}")
        # print("-" * 100)
        for user, cnt in post_counter.most_common(top_n):
            nick = display_lookup[user].most_common(1)[0][0] \
                if display_lookup[user] else ""
            top_tags = ", ".join(t for t, _ in tag_lookup[user].most_common(3))
            # print(f"{user:<25} {nick:<25} {cnt:<25} {top_tags:<50}")
            top_users.append({
                "username": user,
                "nickname": nick,
                "post_count": cnt,
                "top_tags": top_tags
            })

        # 4 plot Weekday vs Weekend
        df = pd.DataFrame({"timestamp": all_dates})
        df["hour"] = df["timestamp"].dt.hour
        df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5   # 5=Sat, 6=Sun

        hourly = (
            df.groupby(["is_weekend", "hour"])
            .size()
            .unstack(level=0)
            .fillna(0)
            .rename(columns={False: "Weekday", True: "Weekend"})
        )

        # plt.figure(figsize=(10, 5))
        # hourly["Weekday"].plot(label="Weekday", marker="o", linewidth=2)
        # hourly["Weekend"].plot(label="Weekend", marker="s", linewidth=2)

        # plt.title(f"Hourly Posting Trend for Tag '{filter_tag.upper()}' (Weekday vs Weekend)")
        # plt.xlabel("Hour of Day")
        # plt.ylabel("Average Posts")
        # plt.xticks(range(0, 24))
        # plt.legend()
        # plt.grid(alpha=0.3)
        # plt.tight_layout()
        # plt.show()
        hourly_json = hourly.to_json(orient='split')
        response = {
            "top_users": top_users,
            "hourly": hourly_json
        }
        return response