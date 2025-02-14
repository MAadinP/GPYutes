from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('upload.html', error="No file uploaded.")
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return render_template('upload.html', error="No file selected.")
        
        if file and file.filename.endswith('.pdf'):
            # Read the PDF file
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            return render_template('display.html', text=text)
        else:
            return render_template('upload.html', error="Invalid file type. Please upload a PDF.")
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)