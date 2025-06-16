import warnings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


def main(database, start_time, end_time, keyword):
        # 1 Connect to Elasticsearch
    es = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        basic_auth=("elastic", "elastic"),
        verify_certs=False
    )
    for index_name in database:

        warnings.filterwarnings("ignore")

        # 2 Scanning index
        dates = []

        docs = scan(
            es,
            index=index_name,
            query={"query": {"match": {"tags": "ai"}}},
            _source=["created_at"],
            size=5000,
            preserve_order=False
        )

        for doc in tqdm(docs, desc="Scanning index"):
            # Convert timestamp to pandas datetime
            timestamp = pd.to_datetime(doc["_source"]["created_at"], errors="coerce", utc=True)
            if pd.notna(timestamp):
                dates.append(timestamp)

    # 3 Aggregate to daily frequency and filter last year
    s = pd.Series(1, index=dates)
    daily = s.resample("D").sum().sort_index().fillna(0)  # Daily count with zero-padding

    # Filter for most recent year
    last_year = daily[daily.index >= (daily.index.max() - pd.Timedelta(days=365))]

    time_list  = [dt.date().isoformat() for dt in last_year.index]
    count_list = last_year.tolist()

    # 4. Time Series Visualization
    # plt.figure(figsize=(10, 5))
    # last_year.plot()
    # plt.title("Daily Posts with Tag 'AI' (Last 12 Months)")
    # plt.xlabel("Date")
    # plt.ylabel("Post Count")
    # plt.tight_layout()
    # plt.show()

    # 5. Text Output
    # Identify top-8 peaks
    peaks = last_year.sort_values(ascending=False).head(8)
    # print("\n=== Top peak dates in last 12 months ===")
    # for ts, cnt in peaks.items():
    #     print(f"{ts.date()}  —  {cnt}")

    peaks_list = [
        {"date": ts.date().isoformat(), "count": int(cnt)}
        for ts, cnt in peaks.items()
    ]

    return {
        "line": {"times": time_list, "values": count_list},
        "peaks": peaks_list
    }