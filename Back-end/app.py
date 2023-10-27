from flask import Flask, render_template, request, jsonify
import openai
import os
import logging
import requests
from bs4 import BeautifulSoup

# Initialize the OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def get_page_summary(url):
    """
    Fetch the content of the given URL and summarize it using OpenAI.
    
    Args:
    - url (str): The webpage URL to be summarized.

    Returns:
    - str: The summarized content or an error message.
    """
    try:
        # Fetch the webpage content using the requests library
        response = requests.get(url)
        # Raise an exception if there was an HTTP error
        response.raise_for_status()

        # Parse the webpage content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style tags to clean the content
        for script in soup(['script', 'style']):
            script.extract()
        page_content = " ".join(soup.stripped_strings)

    except requests.RequestException as e:
        return f"Error fetching content from the URL: {e}"

    try:
        # Get a summary of the content using OpenAI's GPT-3.5-turbo engine
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"Summarize the following content from the website {url}: {page_content}",
            max_tokens=150
        )
        return response.choices[0].text.strip()

    except openai.error.OpenAIError as e:
        return f"Error getting summary from OpenAI: {e}"

@app.route('/summarize', methods=['POST'])
def summarize_url():
    """
    Flask route to handle the POST request for summarizing a webpage.

    Request:
    - JSON body containing a 'url' field with the webpage URL.

    Response:
    - JSON body containing either:
      - 'summary' field with the summarized content.
      - 'error' field with an error message.
    """
    url = request.json.get('url')
    summary = get_page_summary(url)
    if summary.startswith("Error"):
        return jsonify({'error': summary}), 400
    return jsonify({'summary': summary})

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
