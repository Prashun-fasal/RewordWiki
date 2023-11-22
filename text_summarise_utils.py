import wikipediaapi
import openai
import re
import requests
from constants import *

def get_wikipedia_corpus(page_title):
    # Specify a user agent as per Wikipedia's User-Agent policy
    user_agent = "WikiExplorer/1.0 (prasun.ssvm@email.com)"

    headers = {'User-Agent': user_agent}
    
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(page_title)

    if page_py.exists():
        # Set the user agent in the headers
        response = requests.get(page_py.fullurl, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch page. Status code: {response.status_code}"
    else:
        return "Page not found."
def generate_summary_and_paraphrase(section_text):
    openai.api_key = OPENAI_KEY
    prompt = f"Summarize and paraphrase the following section:\n\n{section_text}"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use "text-davinci-003" for GPT-3.5 Turbo
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1,
    )

    return response.choices[0].text.strip()



def get_section_from_corpus(corpus, section_title):
    # Use regular expression to find the content under the specified section heading
    pattern = re.compile(f'^== {re.escape(section_title)} ==\n(.*?)(?:(?=\n==)|(?=$))', re.MULTILINE | re.DOTALL)
    match = pattern.search(corpus)

    if match:
        return match.group(1).strip()
    else:
        return f"Section '{section_title}' not found in the corpus."