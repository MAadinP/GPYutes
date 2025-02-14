from flask import Flask, request, jsonify, render_template
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded. "}), 400
    
    file = request.files['file']

    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    else:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)