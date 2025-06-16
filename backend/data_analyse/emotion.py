import warnings
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

def main(database, start_time, end_time, keyword):
    nltk.download('vader_lexicon')
    # def main(database, start_time, end_time, keyword):
    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # 1 Connect to Elasticsearch
    es = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        basic_auth=("elastic", "elastic"),
        verify_certs=False
    )

    for index_name in database:
        filter_tag = keyword

        warnings.filterwarnings("ignore")

        # 2 Scanning index
        records = []

        query_body = {"query": {"match": {"tags": filter_tag}}} if filter_tag else {"query": {"match_all": {}}}

        docs = scan(
            es,
            index=index_name,
            query=query_body,
            _source=["created_at", "content"],
            size=5000,
            preserve_order=False
        )

        for doc in tqdm(docs, desc="Scanning index"):
            src = doc["_source"]
            text = (src.get("content") or "").strip()
            if not text:
                continue

            # Convert timestamp to pandas datetime
            timestamp = pd.to_datetime(src["created_at"], errors="coerce", utc=True)
            if pd.isna(timestamp):
                continue

            # Calculate sentiment score
            compound = sia.polarity_scores(text)["compound"]
            if compound > 0.05:
                label = "Positive"
            elif compound < -0.05:
                label = "Negative"
            else:
                label = "Neutral"

            records.append({"date": timestamp.date(), "compound": compound, "label": label})

    if not records:
        raise ValueError("No documents retrieved. Please check index name/filter conditions.")

    df = pd.DataFrame(records)

    # 3 Plot pie chart: Sentiment distribution

    sent_counts = Counter(df["label"])
    sentiment_distribution = {
        "Positive": sent_counts["Positive"],
        "Neutral":  sent_counts["Neutral"],
        "Negative": sent_counts["Negative"]
    }
    labels = list(sentiment_distribution.keys())
    values = list(sentiment_distribution.values())

    # plt.figure(figsize=(5, 5))
    # plt.pie(
    #     [sent_counts["Positive"], sent_counts["Neutral"], sent_counts["Negative"]],
    #     labels=["Positive", "Neutral", "Negative"],
    #     colors=['green', 'gray', 'red'],
    #     autopct="%1.1f%%",
    #     startangle=140,
    # )
    # plt.title("Sentiment Distribution for AI-related Posts")
    # plt.tight_layout()
    # plt.show()

    # # 4 Plot line chart: Daily average sentiment
    daily = df.groupby("date")["compound"].mean().sort_index()
    daily_dict = {
        "times": [d for d in daily.index],
        "values": daily.tolist()
    }

    # plt.figure(figsize=(10, 4))
    # daily.plot(marker="o", linewidth=1)
    # plt.title("Daily Average Sentiment (Compound Score)")
    # plt.ylabel("Average Compound")
    # plt.xlabel("Date")
    # plt.grid(alpha=0.3)
    # plt.tight_layout()
    # plt.show()
    return {
        "pie": {
            "labels": labels,
            "values": values
        },
        "line": daily_dict
    }

    '''
    # 5 Plot line chart: Daily average sentiment(Last 12 months)
    cutoff = daily.index.max() - pd.Timedelta(days=365)
    daily_12m = daily[daily.index >= cutoff]

    plt.figure(figsize=(10, 4))
    daily_12m.plot(marker="o", linewidth=1)
    plt.title("Daily Average Sentiment (Last 12 Months)")
    plt.ylabel("Average Compound")
    plt.xlabel("Date")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    '''
