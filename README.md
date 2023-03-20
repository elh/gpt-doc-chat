# gpt-park 📎

### Setup
Make sure `OPENAI_API_KEY` env var is set or provided via `.env` file.
```
pip install -r requirements.txt
```

### Chat with AI

Each response carries over the context of the conversation (until we hit a token limit).

```bash
python chat-cli.py --mode "therapy"

python chat-cli.py -h
# usage: chat-cli.py [-h] [--mode MODE]

# options:
#   -h, --help   show this help message and exit
#   --mode MODE  modes: therapy, finance
```

### Answer questions based on a single provided document

This takes a specific document to feed in as prompt context. The document must fit cleanly in the total token limit for the used model.

```bash
python query-single-doc.py --prompt "You are a helpful customer service assistant AI." --doc "data/faq.md" --question "How can i contact a human?"

python query-single-doc.py -h
# usage: query-single-doc.py [-h] [--doc DOC] [--question QUESTION] [--prompt PROMPT]

# options:
#   -h, --help           show this help message and exit
#   --doc DOC            doc file to prompt with
#   --question QUESTION  your question about the docs
#   --prompt PROMPT      Customized prompt to be prepended to base system prompt (optional)
```

### Answer questions based on document embeddings

TODO: We have all the elements now!

### Embed documents into a csv file
```bash
python embed.py --docs_dir "data/faq"

python embed.py -h
# usage: embed.py [-h] [--docs_dir DOCS_DIR]

# options:
#   -h, --help           show this help message and exit
#   --docs_dir DOCS_DIR  dir of docs to embed
```

### Semantic search with embeddings
```bash
python semantic-search.py --embedding_csv "data/embeddings/data_faq.csv" --query "is this telemedicine only?"

python semantic-search.py -h
# usage: semantic-search.py [-h] [--embedding_csv EMBEDDING_CSV] [--query QUERY]

# options:
#   -h, --help            show this help message and exit
#   --embedding_csv EMBEDDING_CSV
#                         embedding csv file
#   --query QUERY         query to semantic search
```
