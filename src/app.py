from flask import Flask, request, jsonify, render_template
import PyPDF2
import database, embedding, src.llm as llm
import os

app = Flask(__name__)


@app.route("/")
def index():
    print("Rendering index.html template...")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    print("Starting file upload handler...")

    if "file" not in request.files:
        print("Error: No file uploaded")
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]

    if not file.filename.endswith(".pdf"):
        print("Error: File is not a PDF")
        return jsonify({"error": "File must be a PDF"}), 400

    try:
        print("Saving uploaded file temporarily...")
        # Save uploaded file temporarily
        temp_path = "temp.pdf"
        file.save(temp_path)
        print("File saved successfully")

        print("Chunking PDF into text segments...")
        # Chunk the PDF and get text chunks
        chunks = embedding.chunk_pdf(temp_path)
        print(f"Generated {len(chunks)} text chunks")

        print("Generating embeddings for chunks...")
        # Get embeddings for each chunk
        chunk_embeddings = embedding.embed_chunks_with_gcp(
            chunks,
            project_id="visual-notes-451016",
            credentials_path="visual-notes-451016-c7afef482d52.json",
        )
        print(f"Successfully generated {len(chunk_embeddings)} embeddings")

        # Create dictionary mapping chunks to their embeddings
        print(
            f"Creating dictionary mapping {len(chunks)} chunks to their embeddings..."
        )
        chunk_embedding_dict = dict(zip(chunks, chunk_embeddings))
        print("Successfully created chunk-embedding mapping dictionary")

        print("Initializing database and storing chunks...")
        # Initialize database and store chunks with embeddings
        database.create_index("visual-notes-451016", "us-central1")
        stored_vectors = database.store_chunks(chunk_embedding_dict)
        print(f"Successfully stored {len(stored_vectors)} chunks in database")

        print("Preparing text for topic extraction...")
        # Get full text from PDF for topic extraction
        pdf_text = "\n".join(chunks)

        print("Extracting key topics and subtopics...")
        # Extract key topics and subtopics
        topics_dict = llm.get_key_topics_with_subtopics(pdf_text)
        print(f"Extracted {len(topics_dict)} main topics")

        print("Generating Mermaid diagram...")
        # Generate Mermaid diagram
        mermaid_diagram = llm.generate_mermaid_diagram("Document Overview", topics_dict)
        print("Mermaid diagram generated successfully")
        print("\nMermaid Diagram:")
        print(mermaid_diagram)

        print("Cleaning up temporary file...")
        # Clean up temp file
        os.remove(temp_path)
        print("Temporary file removed")

        print("Returning successful response...")
        return jsonify({"success": True, "mermaid_diagram": mermaid_diagram})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # Clean up temp file if it exists
        if os.path.exists("temp.pdf"):
            print("Cleaning up temporary file after error...")
            os.remove("temp.pdf")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask application in debug mode...")
    app.run(debug=True)
