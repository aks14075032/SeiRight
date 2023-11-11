import re
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Initialize the GPT-2 model for text generation
nlp = pipeline("summarization", model="facebook/bart-large-cnn")


def fetch_and_process_text(url: str) -> str:
    """
    Fetch and process text content from a given URL by removing HTML tags.

    Parameters:
    - url (str): The URL to fetch text content from.

    Returns:
    str: Processed text content with HTML tags removed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove HTML tags and get the text
        text = ' '.join(soup.stripped_strings)
        return text
    except Exception as e:
        return str(e)


def process_chunk(chunk: str, chunk_number: int, chunk_type: str) -> str:
    """
    Process a text chunk using the GPT-2 model for summarization.

    Parameters:
    - chunk (str): The text chunk to be processed.
    - chunk_number (int): The index of the chunk.
    - chunk_type (str): The type of the chunk (e.g., 'policy' or 'webpage').

    Returns:
    str: The summarized text of the chunk.
    """
    response = nlp(chunk, max_length=min(len(chunk), 80))
    print(f"Processed {chunk_type} chunk {chunk_number}")
    return response[0]['summary_text']


def analyze_compliance_parallel(policy_chunks: list, webpage_chunks: list) -> tuple:
    """
    Analyze compliance in parallel by processing chunks of policy and webpage text.

    Parameters:
    - policy_chunks (list): List of policy text chunks.
    - webpage_chunks (list): List of webpage text chunks.

    Returns:
    tuple: Combined policy text and combined webpage text.
    """
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        policy_chunk_args = [(chunk, idx, 'policy') for idx, chunk in enumerate(policy_chunks, start=1)]
        webpage_chunk_args = [(chunk, idx, 'webpage') for idx, chunk in enumerate(webpage_chunks, start=1)]

        generated_policy_chunks = list(executor.map(process_chunk, *zip(*policy_chunk_args)))
        generated_webpage_chunks = list(executor.map(process_chunk, *zip(*webpage_chunk_args)))

    combined_policy_text = ' '.join(generated_policy_chunks)
    combined_webpage_text = ' '.join(generated_webpage_chunks)

    return combined_policy_text, combined_webpage_text


def analyze_compliance(policy_url: str, webpage_url: str) -> any:
    """
    Analyze compliance between a policy and a webpage.

    Parameters:
    - policy_url (str): URL of the policy.
    - webpage_url (str): URL of the webpage.

    Returns:
    list: List of non-compliant results.
    """
    non_compliant_results = []

    try:
        policy_text = fetch_and_process_text(policy_url)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch policy text: ' + str(e)})

    try:
        webpage_text = fetch_and_process_text(webpage_url)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch webpage content: ' + str(e)})

    # Split the policy_text into chunks
    chunk_size = 1024
    policy_chunks = [policy_text[i:i + chunk_size] for i in range(0, len(policy_text), chunk_size)]

    # Split the webpage_text into chunks
    webpage_chunks = [webpage_text[i:i + chunk_size] for i in range(0, len(webpage_text), chunk_size)]

    combined_policy_text, combined_webpage_text = analyze_compliance_parallel(policy_chunks, webpage_chunks)

    if not re.search(combined_policy_text, combined_webpage_text, re.IGNORECASE):
        non_compliant_results.append(combined_webpage_text)

    return non_compliant_results


@app.route('/check_compliance', methods=['POST'])
def check_compliance_endpoint():
    """
    API endpoint to check compliance between a policy and a webpage.

    Expects a JSON payload with 'policy_url' and 'webpage_url'.
    Returns a JSON response with 'non_compliant_results' or 'error'.
    """
    try:
        data = request.get_json()
        policy_url = data.get('policy_url')
        webpage_url = data.get('webpage_url')

        if policy_url and webpage_url:
            non_compliant_results = analyze_compliance(policy_url, webpage_url)
            print('Non-compliant results:', non_compliant_results)
            return jsonify({'non_compliant_results': non_compliant_results})
        else:
            return jsonify({'error': 'policy_url and webpage_url parameters are missing'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
