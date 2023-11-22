from constants import *
import openai
openai.api_key = OPENAI_KEY
import openai
import requests
import wikipediaapi
import replicate


def fetch_wikipedia_content(title, sections):
    user_agent = "YourAppName/1.0 (your@email.com)"  # Replace with your application name and contact email
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})

    # Fetch Wikipedia content
    wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={title}&explaintext=1"
    response = session.get(wiki_url)
    data = response.json()
    
    # Extract page content
    page = next(iter(data['query']['pages'].values()))

    # Check if the page is a disambiguation page
    if 'missing' in page:
        print(f"The provided title '{title}' does not exist on Wikipedia.")
        return {}
    elif 'disambiguation' in page:
        print(f"The provided title '{title}' is a disambiguation page. Please choose a more specific title.")
        return {}

    section_texts = {}
    for section in sections:
        if section.lower() in page['extract'].lower():
            section_texts[section] = page['extract']
    print(section_texts)

    return section_texts

# def paraphrase_with_gpt3(text):
#     # Use the OpenAI API to paraphrase the text
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=text,
#         temperature=0.7,
#         max_tokens=150
#     )
#     return response['choices'][0]['text'].strip()

def paraphrase_with_gpt3(text):
    output = replicate.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    input={"prompt": text[:4096]+' please summarise above text'}
)
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    # for item in output:
    #     # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
    #     print(item, end="")
    return output

def main():
    # Input Wikipedia article title and sections to extract
    article_title = input("Enter Wikipedia article title: ")
    sections_to_extract = input("Enter comma-separated sections to extract: ").split(',')

    # Fetch Wikipedia content
    sections_content = fetch_wikipedia_content(article_title, sections_to_extract)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++',sections_content)
    exit()
    if not sections_content:
        return  # Exit if there's an issue with the provided title

    # Paraphrase and summarize each section
    for section, content in sections_content.items():
        paraphrased_text = paraphrase_with_gpt3(content)
        print(f"\nOriginal {section}:\n{content}\n")
        print(f"Paraphrased {section}:\n{paraphrased_text}\n")

if __name__ == "__main__":
    main()
