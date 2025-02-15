from google.cloud import aiplatform
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter


def embed_chunks_with_gcp(chunks, project_id, location="us-central1"):
    """
    Given a list of text chunks, use GCP's 'textembedding-gecko@001' model
    to generate embeddings.

    :param chunks: List of strings (text chunks).
    :param project_id: Your GCP project ID.
    :param location: The region (e.g. 'us-central1') where the model is hosted.
    :return: A list of embedding vectors (list of floats) corresponding to each chunk.
    """
    # 1. Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # 2. Load the pre-trained text embedding model
    #    You can also pass a custom endpoint if needed.
    embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(
        "textembedding-gecko@001"
    )

    # 3. Get embeddings for all chunks in a single batch
    #    The model can accept a list of strings.
    #    (For large lists, you may want to batch them in smaller subsets.)
    embedding_results = embedding_model.get_embeddings(chunks)

    # 4. Convert the results to a list of vectors
    #    Each 'embedding' is a dictionary with 'values' (the vector)
    embeddings = []
    for result in embedding_results:
        vector = result.values  # The embedding vector (list of floats)
        embeddings.append(vector)

    return embeddings


def chunk_pdf(
    pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 100
) -> list[str]:
    """
    1. Extracts text from all pages of a PDF file.
    2. Uses a hybrid approach (semantic + chunk limits) via LangChain's RecursiveCharacterTextSplitter.
    3. Returns a list of chunk strings.

    :param pdf_path: Path to the PDF file.
    :param chunk_size: Max number of characters allowed in a chunk.
    :param chunk_overlap: Number of characters to overlap between consecutive chunks.
    :return: A list of chunk strings.
    """

    # 1. Read the PDF content
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Clean up the text (optional: remove extra spaces, etc.)
                text = text.strip()
                all_text.append(text)

    # Combine all pages into one big string
    pdf_text = "\n\n".join(all_text)

    # 2. Create a RecursiveCharacterTextSplitter with multiple separators
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # The order of separators matters: tries \n\n first, then \n, then periods, etc.
        separators=["\n\n", "\n", ".", " ", ""],
    )

    # 3. Split the text into chunks
    chunks = text_splitter.split_text(pdf_text)

    return chunks


# Example usage:
if __name__ == "__main__":
    pdf_file_path = "example.pdf"  # Replace with your PDF file
    chunks = chunk_pdf(pdf_file_path, chunk_size=1000, chunk_overlap=100)

    print(f"Total chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i} (length={len(chunk)}) ---")
        print(chunk[:200], "...")  # Print the first 200 characters for brevity
        print()

    # Example usage:
    # 1) Assume you've already chunked your PDF text:
    # chunks = [
    #     "This is the first chunk from the PDF ...",
    #     "This is the second chunk from the PDF ...",
    #     # ...
    # ]

    # 2) Embed with GCP
    project_id = "aiengine-451014"  # Replace with your actual project
    vectors = embed_chunks_with_gcp(chunks, project_id)

    print(f"Generated {len(vectors)} embeddings.")
    print("First embedding vector:", vectors[0][:10], "...")  # print first 10 dims
