from flask import Flask, render_template, request, jsonify
import openai
import os
import logging

# Set up OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def get_page_summary(url):
    # TODO: Extract text content from the URL using a library like BeautifulSoup or similar.
    page_content = ...  # This should contain the main text content from the URL.

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Summarize the following content from the website {url}: {page_content}",
        max_tokens=150
    )

    return response.choices[0].text.strip()


@app.route('/summarize', methods=['POST'])
def summarize_url():
    url = request.json.get('url')
    summary = get_page_summary(url)
    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True)
