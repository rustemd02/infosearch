from flask import Flask, request, jsonify
from task5 import vector_search

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/search', methods=['POST'])
def perform_search():
    query = request.json.get('query')
    search_results = vector_search.search(query)
    return jsonify(search_results)


if __name__ == "__main__":
    app.run(debug=True)
