from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import re
import torch
import spacy
from scipy.spatial.distance import cosine
import tempfile
from faster_whisper import WhisperModel

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_audio' # You need to create thos folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Determine the device to run the model on
model_size = "medium"
model1 = WhisperModel(model_size, device="cpu", compute_type="int8")

# Load the Spacy model for semantic analysis
nlp = spacy.load("de_core_news_md")

def transcribe(file_path, model_size):
    # Dynamic model initialization based on model_size
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # Transcribe the audio file
    segments, _ = model.transcribe(file_path, beam_size=5)
    # Concatenate the transcribed segments
    transcribed_text = " ".join(segment.text for segment in segments)
    return transcribed_text

def normalize_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()  # Convert to lowercase

# Function to calculate semantic similarity
def calculate_semantic_similarity(text1, text2):
    doc1 = nlp(normalize_text(text1))
    doc2 = nlp(normalize_text(text2))
    similarity = doc1.similarity(doc2)
    return similarity * 100  # Convert to percentage

def detailed_word_comparison(expected_text, transcribed_text):
    # Directly extract words from the original texts
    expected_words = expected_text.split()
    transcribed_words = transcribed_text.split()

    result = []
    i, j = 0, 0
    while i < len(expected_words) or j < len(transcribed_words):
        # Perform normalization only for comparison
        normalized_expected = normalize_text(expected_words[i]) if i < len(expected_words) else None
        normalized_transcribed = normalize_text(transcribed_words[j]) if j < len(transcribed_words) else None

        if i < len(expected_words) and j < len(transcribed_words):
            if normalized_expected == normalized_transcribed:
                result.append({'type': 'correct', 'word': transcribed_words[j]})
                i += 1
                j += 1
            else:
                result.append({'type': 'mismatch', 'expected': expected_words[i], 'transcribed': transcribed_words[j]})
                i += 1
                j += 1
        elif i < len(expected_words):
            result.append({'type': 'missing', 'word': expected_words[i]})
            i += 1
        else:
            result.append({'type': 'extra', 'word': transcribed_words[j]})
            j += 1
    return result

@app.route('/transcribe', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file in the request.'}), 400

    file = request.files['file']
    if file.filename == '' or file.filename.isspace():
        return jsonify({'error': 'No selected file name.'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    
    model_size = request.form.get('model_size', 'medium')  # Default to 'medium'
    transcribed_text= transcribe(save_path, model_size)

    # Clean up the saved audio file
    os.remove(save_path)
   
    response_data = {'transcribed_text': transcribed_text}

    analysis_type = request.form.get('analysis_type')  # Extract the type of analysis here
    expected_text = request.form.get('expected_text')  # Extract the expected text

    if analysis_type == 'wordByWord' and expected_text:
        word_diff = detailed_word_comparison(expected_text, transcribed_text)
        response_data['word_diff'] = word_diff
    elif analysis_type == 'semantic' and expected_text:
        semantic_similarity = calculate_semantic_similarity(transcribed_text, expected_text)
        response_data['semantic_similarity'] = f"{semantic_similarity:.2f}%"

    return jsonify(response_data), 200

@app.route('/ping', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def ping():
    return jsonify({'message': 'Server is reachable!'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
