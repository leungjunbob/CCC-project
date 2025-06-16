from flask import Flask, request, jsonify
import topn
import tag
import hotTopic
import emotion


app = Flask(__name__)

function_map = {
    "topic1: User post count": topn.main,
    "topic2: Cross-analysis of AI and other topics": tag.main,
    "topic3: AI topic popularity analysis": hotTopic.main,
    "topic4: Sentiment analysis across time": emotion.main,
}

@app.route('/api/run', methods=['POST'])
def run_function():
    data = request.get_json()
    print(data)
    topic = data.get('topic', [])
    database = data.get('database', []),
    start_time = data.get('start_time', [])
    end_time = data.get('end_time', [])
    keyword = data.get('keyword', [])

    try:
        result = function_map[topic](database, start_time, end_time, keyword)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)