from flask import Flask, request, jsonify
import spacy
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")

# Dictionary API configuration
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def fetch_definition_from_api(term):
    """
    Fetch the first definition of a term using the Dictionary API.
    """
    try:
        response = requests.get(f"{DICTIONARY_API_URL}{term}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                definitions = data[0].get("meanings", [])
                if definitions:
                    # Extract the first definition from the meanings list
                    first_meaning = definitions[0]
                    if "definitions" in first_meaning and first_meaning["definitions"]:
                        return first_meaning["definitions"][0]["definition"]
        return "Definition not available via API."
    except Exception as e:
        print(f"Error fetching definition from API: {e}")
        return "Error fetching definition from API."

@app.route('/process_note', methods=['POST'])
def process_note():
    """
    Process the content from the request, extract terms using SpaCy, and fetch their definitions.
    """
    data = request.json
    content = data.get('content', '')
    doc = nlp(content)

    key_terms = []

    # Extract key terms from SpaCy entities and fetch their definitions
    for ent in doc.ents:
        term = ent.text
        definition = fetch_definition_from_api(term)
        print(definition)
        key_terms.append({"term": term, "definition": definition})
    
    return jsonify({"key_terms": key_terms})

if __name__ == '__main__':
    app.run(debug=True)
