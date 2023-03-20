# gpt-doc-chat 📎

GPT-powered, conversational search of documents
1. Put a set of documents in a directory. Note: each file should be less than 4K tokens. e.g.`my_dir/`.
2. Generate and save the embeddings of those documents in a csv file e.g. `python embed.py --docs_dir my_dir` -> `data/embeddings/my_dir.csv`.
3. Ask natural language questions of the documents! e.g. `python query-docs.py --embedding_csv data/embeddings/my_dir.csv --question "Did my account change on March 14th change my cost?" --prompt "You are a helpful customer service AI."`. This can also be served as a web API with `server.py`.

This is a vanilla implementation of GPT semantic search and chat completion I did as hands-on learning. This is naive but surprisingly functional, so I am on the LLM hype train.

### Setup
Make sure `OPENAI_API_KEY` env var is set or provided via `.env` file.
```
pip install -r requirements.txt
```

### Answer questions based on document embeddings ⭐️

Query against a corpus of documents that is larger than the GPT token limit. We first preprocess the documents by generating embedding vectors and storing them. When a new query comes in, we embed it using the same model and run a local cosine similarity ranking to find the most relevant documents. We merge as many of those relevant documents as we can under the token limit into the the prompt. We then send the final prompt to GPT for completion.

```bash
python query-docs.py --embedding_csv data/embeddings/faq.csv --question "Did my account change on March 14th change my cost?" --prompt "You are a helpful customer service AI."

python query_docs.py -h
# usage: query_docs.py [-h] [--embedding_csv EMBEDDING_CSV] [--question QUESTION] [--prompt PROMPT]

# Answer questions based on a corpus of documents

# options:
#   -h, --help            show this help message and exit
#   --embedding_csv EMBEDDING_CSV
#                         embedding csv file
#   --question QUESTION   your question about the docs
#   --prompt PROMPT       Customized prompt to be prepended to base system prompt (optional)
```

I also have a `query-docs_completions.py` version uses the older and more expensive `text-davinci-003` model and completions API, instead of chat APIs. The benefit to that approach is that it respects sysytem prompts much more.

I also have a simple, janky server that wraps the `query-docs.py` script for prototyping web integrations: `server.py`

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
python semantic_search.py --embedding_csv "data/embeddings/data_faq.csv" --query "is this telemedicine only?"

python semantic_search.py -h
# usage: semantic_search.py [-h] [--embedding_csv EMBEDDING_CSV] [--query QUERY]

# options:
#   -h, --help            show this help message and exit
#   --embedding_csv EMBEDDING_CSV
#                         embedding csv file
#   --query QUERY         query to semantic search
```

### Answer questions based on a single provided document

This takes a specific document to feed in as prompt context. The document must fit cleanly in the total token limit for the used model.

```bash
python query_single_doc.py --prompt "You are a helpful customer service assistant AI." --doc "data/faq.md" --question "How can i contact a human?"

python query_single_doc.py -h
# usage: query_single_doc.py [-h] [--doc DOC] [--question QUESTION] [--prompt PROMPT]

# options:
#   -h, --help           show this help message and exit
#   --doc DOC            doc file to prompt with
#   --question QUESTION  your question about the docs
#   --prompt PROMPT      Customized prompt to be prepended to base system prompt (optional)
```

## Chat

### Chat with AI

Each response extends the context of the conversation (until we hit a token limit).

```bash
python chat_cli.py --mode "therapy"

python chat_cli.py -h
# usage: chat_cli.py [-h] [--mode MODE]

# options:
#   -h, --help   show this help message and exit
#   --mode MODE  modes: therapy, finance
```
