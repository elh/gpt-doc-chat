import sys
import os
import datetime
import argparse
from dotenv import load_dotenv
import openai

MODEL = "text-davinci-003"
LOGS_DIRECTORY = "logs/query_single_doc"

BASE_PROMPT = "Given the following DOCUMENTATION please answer the following QUESTION."

def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    parser = argparse.ArgumentParser(description='Answer questions based on a provided document')
    parser.add_argument('--doc', type=str, default="", help='doc file to prompt with')             # explicitly configured
    parser.add_argument('--question', type=str, default="", help='your question about the docs')
    parser.add_argument('--prompt', type=str, default="", help='Customized prompt to be prepended to base system prompt (optional)')
    args = parser.parse_args()
    if args.question == "" or args.doc == "":
        print("ERROR: Doc file and question is required.")
        sys.exit(1)

    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)
    now = datetime.datetime.now()
    log_file_name = LOGS_DIRECTORY + "/" + str(now.strftime("%Y_%m_%d_%H.%M.%S")) + ".txt"

    # hardcoded file + prompt
    f = open(args.doc, "r")
    file = f.read()

    prompt = args.prompt + "." + BASE_PROMPT
    prompt += "\n\nDOCUMENTATION:\n" + file
    prompt += "\n\nQUESTION:\n" + args.question + "\n\nANSWER:"
    print(prompt)

    resp = openai.Completion.create(model=MODEL, prompt=prompt, max_tokens=256)
    output = resp.get("choices", [{}])[0].get("text", "").lstrip('\n').lstrip(' ')
    if output == "":
        print("ERROR: No response from OpenAI 🤖\n" + resp)
        sys.exit(1)
    total_tokens = resp.get("usage", {}).get("total_tokens", 0)

    print(output)
    print("\n----------\n" + str(total_tokens) + " tokens. model: " + MODEL)

    open(log_file_name, 'w').write(prompt + "\n" + output + "\n\n----------\n" + str(total_tokens) + " tokens. model: " + MODEL) # full reset of file

if __name__ == "__main__":
    main()
