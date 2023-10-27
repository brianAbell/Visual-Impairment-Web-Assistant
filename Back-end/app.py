from flask import Flask, render_template, request, jsonify
import openai
import os
import logging
import requests
from bs4 import BeautifulSoup

# Set up OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def get_page_summary(url):
    try:
        # Get the content of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content from the webpage
        for script in soup(['script', 'style']):
            script.extract()
        page_content = " ".join(soup.stripped_strings)

    except requests.RequestException as e:
        return f"Error fetching content from the URL: {e}"

    try:
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
    url = request.json.get('url')
    summary = get_page_summary(url)
    if summary.startswith("Error"):
        return jsonify({'error': summary}), 400
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
