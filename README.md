# gpt-park 📎

### Setup
`pip install -r requirements.txt`

### Chat with AI
```bash
python chat-cli.py --mode therapy
python chat-cli.py -h # for more options
```

### Answer questions based on some data
```bash
python docs.py --system_prompt "You are a helpful customer service assistant AI." --doc "docs/faq.md" --question "How can i contact a human?"

python docs.py -h
# usage: docs.py [-h] [--doc DOC] [--question QUESTION] [--prompt PROMPT]

# options:
#   -h, --help           show this help message and exit
#   --doc DOC            doc file to prompt with
#   --question QUESTION  your question about the docs
#   --prompt PROMPT      Customized prompt to be prepended to base system prompt (optional)
```

### Embed documents into a csv file
```bash
python embed.py --docs_dir "data/faq"
# python embed.py -h
# usage: embed.py [-h] [--docs_dir DOCS_DIR]

# options:
#   -h, --help           show this help message and exit
#   --docs_dir DOCS_DIR  dir of docs to embed
```
