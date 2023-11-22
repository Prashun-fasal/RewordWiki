from constants import *
import openai
from text_summarise_utils import *
openai.api_key = OPENAI_KEY
import openai
import requests
import replicate
import streamlit as st



def main():
    # Input Wikipedia article title and sections to extract
    st.header("RephraseWiki")
    article_title = st.text_input("Enter Wikipedia article title: ")
    try:
        sections_in_corpus = fetch_sections(article_title)
        sections_to_extract = st.sidebar.radio("Select the section you want to summarise or paraphrase ", sections_in_corpus)
        st.write(f'You selected "{sections_to_extract}" section to further processing text for the article titled "{article_title}"')
        text_from_specific_section = fetch_wikipedia_section(article_title, sections_to_extract)
        decision_input = st.radio('How do you want to move further:',('see original text','Summarise the section', 'Paraphrase the section'))
        if 'see original text' in decision_input:
            st.write(f'"text from "{sections_to_extract}" :{text_from_specific_section}"')
        if 'Summarise the section' in decision_input:
            st.write(f'Your summarised text for section : "{sections_to_extract}"')
            summarised_text = paraphrase_with_llma(text_from_specific_section, 'summarise')
            summary = list(summarised_text)
            st.write(' '.join(summary))
        if 'Paraphrase the section' in decision_input:
            st.write(f'Your Paraphrased text for section : "{sections_to_extract}"')
            paraphrased_text = paraphrase_with_llma(text_from_specific_section, 'paraphrase')
            paraphrased = list(paraphrased_text)
            st.write(' '.join(paraphrased))
    except Exception as e:
        st.write(f'Getting error : {e}')

if __name__ == "__main__":
    main()
