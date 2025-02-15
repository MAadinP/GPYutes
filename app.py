from flask import Flask, request, jsonify, render_template
import PyPDF2
from openai import OpenAI  # Import the new OpenAI client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key = api_key)

app = Flask(__name__)

def get_key_topics(text):
    """Send extracted text to Claude to get key topics."""
    prompt = f"""
    Extract the key topics from the following text:
    {text}
    
    Please return only the topics as a comma-separated list.
    """
    
    # Use the new chat completions API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    
    # Extract the response content
    extracted_topics = response.choices[0].message.content
    return [topic.strip() for topic in extracted_topics.split(",") if topic.strip()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    
    file = request.files['file']

    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Get key topics from the extracted text
            key_topics = get_key_topics(text)

            return jsonify({"text": text, "key_topics": key_topics})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400

if __name__ == '__main__':
    app.run(debug=True)