import requests
import wikipediaapi
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