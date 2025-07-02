import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = sys.argv
    verbose = False
    flags = [
        "--verbose",
    ]
    for flag in flags:
        if flag in sys.argv:
            verbose = True
            prompt.pop(prompt.index(flag))
    user_prompt = ""
    if len(prompt) < 2:
        print("No prompt was given")
        sys.exit(1)
    else:
        user_prompt = " ".join(prompt[1:])
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response(client, messages, user_prompt, verbose)

def response(client, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    else:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()