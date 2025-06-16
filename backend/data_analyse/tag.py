import warnings
from collections import Counter
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from wordcloud import WordCloud

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
        tag_counter = Counter()

        docs = scan(
            es,
            index=index_name,
            query={"query": {"match_all": {}}},
            _source=["tags"],
            size=5000,
            preserve_order=False
        )

        for doc in tqdm(docs, desc="Processing documents"):
            tags = doc["_source"].get("tags", [])
            if isinstance(tags, str):
                tag_counter[tags] += 1
            else:
                tag_counter.update(tags)

    print(f"Total extracted {sum(tag_counter.values()):,} tags, {len(tag_counter):,} unique tags")

    # 3 Create DataFrame for analysis
    df_tags = pd.DataFrame(tag_counter.items(), columns=["tag", "freq"])
    df_tags.sort_values("freq", ascending=False, inplace=True)
    df_tags.reset_index(drop=True, inplace=True)

    # 4 Because the statistics are related topics with ai tags, the ai tag with the highest frequency is excluded
    most_common_tag, highest_freq = tag_counter.most_common(1)[0]
    del tag_counter[most_common_tag]
    # df_tags = pd.DataFrame(tag_counter.items(), columns=["tag", "freq"])\
    #             .sort_values("freq", ascending=False)\
    #             .reset_index(drop=True)
    sorted_items = sorted(tag_counter.items(), key=lambda x:x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    return {
        "labels": labels,
        "values": values
    }
    # 5 Visualization
    # 5-1 Bar Chart: Top 20 Tags
    # top_n = 20
    # label = df_tags["tag"].values()
    # value = df_tags["freq"].values()
    # print(label, value)
    # plt.figure(figsize=(10, 6))
    # plt.bar(df_tags["tag"][:top_n], df_tags["freq"][:top_n])
    # plt.xticks(rotation=45, ha="right")
    # plt.title(f"Top {top_n} Most Frequent AI-Related Tags")
    # plt.ylabel("Frequency")
    # plt.tight_layout()
    # plt.show()

    # 5-2 Word Cloud: All Tags
    # wc = WordCloud(
    #     width=1000,
    #     height=600,
    #     background_color="white"
    # )
    # wc.generate_from_frequencies(tag_counter)
    # print(tag_counter)

    # plt.figure(figsize=(12, 7))
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.title("Word Cloud of AI-Related Tags")
    # plt.show()
