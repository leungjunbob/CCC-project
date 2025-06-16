# Notebook Version
To ensure the notebook wigets run properly, you need to make sure your notebook version is below 7.X.X which can support the Nbextensions.

To do this, type the following command in your terminal, or in your anaconda env terminal.

``` bash
pip install notebook==6.1.5
pip install --upgrade "jupyter-server<2.0.0"
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

Reference:
https://stackoverflow.com/questions/49647705/jupyter-nbextensions-does-not-appear


# Usage:
Open the jupyter notebook, and click the "Restart the kernel, and re-run the whole notebook button".

Remaining again: The notebook must enable nbextensions otherwise it doesn't work.


# Communicating with backend functions:
``` bash
    # topic.value = one of [topic1: User post count, topic2: Cross-analysis of AI and other topics, topic3: AI topic popularity analysis, topic4: Sentiment analysis across time]
    # databases.value = one or more of ['mastodon_ai','mastodon_public','mastodon_weather'] 
    # start_time = instance of datetime.date()
    # end_time = instance of datetime.date()
    # keyword = a string, such as "ai"
``` 
payload is a dict send to backend

result is a json recieve from backend

It is better to return the data using the same name as in this front-end program, otherwise needs to write extra logic to convert it.

## Topic1: User post count:
``` bash
    payload = {
        "topic": topics.value,
        "database": list(databases.value),
        "start_time": str(start_time.value),
        "end_time": str(end_time.value)
    }
    result = {
        "labels": list(str), # The name of user
        "values": list(float)  # Their number of posts
    }
``` 

## topic2: Cross-analysis of AI and other topics:
``` bash
    payload = {
        "topic": topics.value,
        "database": list(databases.value),
        "start_time": str(start_time.value),
        "end_time": str(end_time.value)
    }
    result = {
        "labels": list(str), # The name of tag
        "values": list(float)  # Their number of posts in this tag
    }
``` 

## topic3: AI topic popularity analysis:
``` bash
    payload = {
        "topic": topics.value,
        "database": list(databases.value),
        "start_time": str(start_time.value),
        "end_time": str(end_time.value)
    }
    result = {
        "times": list(str), # The date
        "values": list(float)  # Their sentiment values
    }
``` 

## topic4: Sentiment analysis across time:
``` bash
    payload = {
        "topic": topics.value,
        "database": list(databases.value),
        "start_time": str(start_time.value),
        "end_time": str(end_time.value),
        "keyword": keyword.value
    }
    result = {
        "labels": list(str), # The sentiment category (positive, negative, neutral)
        "times": list(str), # The date
        "values": list(float)  # Their sentiment values
    }
``` 

