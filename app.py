from flask import Flask, request, jsonify, render_template
import PyPDF2
import database, embedding, llm

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file uploaded. "}), 400

    # file = request.files['file']

    # if file and file.filename.endswith('.pdf'):
    #     try:
    #         pdf_reader = PyPDF2.PdfReader(file)
    #         text = ""
    #         for page_num in range(len(pdf_reader.pages)):
    #             page = pdf_reader.pages[page_num]
    #             text += page.extract_text()

    #         return jsonify({"text": text})
    #     except Exception as e:
    #         return jsonify({"error": str(e)}), 500

    # else:
    #     return jsonify({"error": str(e)}), 500

    pdf_embeddings = embedding.embed_text(pdf)
    database.create_index()
    database.store(pdf_embeddings)
    key_topics = llm.createquery(pdf)
    query_embeddings = embedding.embed_text(key_topics)
    food_for_image_gen = database.query(query_embeddings)

    image_gen(food_for_image_gen)


if __name__ == "__main__":
    app.run(debug=True)
