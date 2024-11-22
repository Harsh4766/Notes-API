from flask import Flask, request, jsonify
import spacy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")

# Define a static dictionary for term definitions
term_definitions = {
    "React": "A JavaScript library for building user interfaces.",
    "Encryption": "The process of converting information or data into a code.",
    "NLP": "Natural Language Processing, a field of AI focused on language understanding."
}

@app.route('/process_note', methods=['POST'])
def process_note():
    data = request.json
    content = data.get('content', '')
    doc = nlp(content)

    key_terms = []
    
    # Extract key terms from SpaCy entities
    for ent in doc.ents:
        term = ent.text
        definition = term_definitions.get(term, "SpaCy identified entity")
        key_terms.append({"term": term, "definition": definition})

    # Match terms from the static dictionary
    for term in term_definitions.keys():
        if term.lower() in content.lower() and term not in [key["term"] for key in key_terms]:  # Case-insensitive check
            key_terms.append({"term": term, "definition": term_definitions[term]})
    
    return jsonify({"key_terms": key_terms})

if __name__ == '__main__':
    app.run(debug=True)
