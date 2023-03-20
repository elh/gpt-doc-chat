import os
import sys
from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json

from query_docs import query_docs
from semantic_search import semantic_search

app = Flask(__name__)
CORS(app)

'''
This is a jank, un-generalized demo. Start a webserver that queries the docs
`EMBEDDING_CSV=vectors.csv DOCS_JSON=docs.json python server.py`

POST /query
{"query": "In what countries is this service available?"}
'''

def url_to_title(url):
    words = url.lstrip('/').split('-')
    title = ' '.join([word.capitalize() for word in words])
    return title.replace('#', ': ').replace('_', ' ')

@app.route('/query', methods=['POST'])
def query():
    data = request.json

    if data is None:
        response_data = {'status': 'error', 'message': 'No data received'}
        return response_data, 400
    if "query" not in data:
        response_data = {'status': 'error', 'message': '"query" is required'}
        return response_data, 400

    response = query_docs(os.getenv("EMBEDDING_CSV"), data['query'], os.getenv("PROMPT") if os.getenv("PROMPT") is not None else "")

    # WARN: ############################################################################################################
    # this is not generalized. I want to return additional context that is not standard in the embeddings file
    # soln: cheat with a lookup
    df = pd.read_csv(os.getenv("EMBEDDING_CSV"))
    df["embedding"] = df.embedding.apply(eval).apply(np.array)
    search_results = semantic_search(df, data['query'], n=1)

    # jank
    for i in search_results.index:
        file_name = search_results['file_name'][i]
        file_content = search_results['content'][i]
        break

    docs_json = json.load(open(os.getenv("DOCS_JSON")))
    if file_name not in docs_json:
        response_data = {'status': 'error', 'message': 'file_name not found in docs_json'}
        return response_data, 500

    link = docs_json[file_name]
    file_title = url_to_title(link)

    ####################################################################################################################

    response_data = {
        'response': response,
        # additional context
        'reference_title': file_title,
        'reference_text': file_content,
        'link': link
    }
    return response_data, 200

if __name__ == '__main__':
    if os.getenv("EMBEDDING_CSV") is None:
        print("ERROR: EMBEDDING_CSV is required")
        sys.exit(1)
    # additional context about the documents
    if os.getenv("DOCS_JSON") is None:
        print("ERROR: DOCS_JSON is required")
        sys.exit(1)
    app.run(debug=True)
