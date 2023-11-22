import requests
import replicate
import wikipedia
import streamlit as st

def fetch_sections(title):
    base_url = "https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        'action': 'parse',
        'format': 'json',
        'page': title,
        'prop': 'sections'
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        data = response.json()

        # Check if the request was successful
        if 'error' in data:
            raise Exception(f"Error: {data['error']['info']}")

        # Extract sections from the response
        sections = data['parse']['sections']

        return [d['line'] for d in sections if 'line' in d]
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_wikipedia_section(title, section_title):
    user_agent = "RephraseWiki/1.0 x@gmail.com"  # Replace with your app's information

    wikipedia.set_user_agent(user_agent)

    try:
        # Fetch the summary of the entire page
        full_summary = wikipedia.summary(title)

        # Find the starting index of the section
        section_start = full_summary.find(section_title)

        # Find the ending index of the section
        next_section_start = full_summary.find("==", section_start + 1)
        section_end = next_section_start if next_section_start != -1 else len(full_summary)

        return full_summary[section_start:section_end].strip()
    except wikipedia.exceptions.DisambiguationError as e:
        st.write(f"Ambiguous title: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError as e:
        st.write(f"HTTP request timed out: {e}")
    except wikipedia.exceptions.PageError as e:
        st.write(f"Page not found: {e}")

def paraphrase_with_llma(text, desired_processing):
    return replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt": f'{text} please {desired_processing} above text'},
    )

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

    return {
        section: page['extract']
        for section in sections
        if section.lower() in page['extract'].lower()
    }

