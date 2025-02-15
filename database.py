import os
from pinecone import Pinecone, ServerlessSpec

# Set Pinecone API Key
PINECONE_API_KEY = "pcsk_31rYzN_AUViJhrUhb4yHwVazNmisnTP4z1cT7jSoCJnH3xNPKB8LEDpKJHcC34LuP7Hmak"  # Replace with your actual API key

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name
INDEX_NAME = "visualnotes"

# Check if the index exists, if not, create it
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=128,  # Set the dimensionality of your embeddings
        metric="euclidean",  # Options: "euclidean", "cosine", "dotproduct"
        spec=ServerlessSpec(
            cloud="aws",  # Use the appropriate cloud provider
            region="us-east-1",  # Replace with your preferred region
        ),
    )


pc = Pinecone(api_key="YOUR_API_KEY")

# Define a sample dataset where each item has a unique ID, text, and category
data = [
    {
        "id": "rec1",
        "text": "Apples are a great source of dietary fiber, which supports digestion and helps maintain a healthy gut.",
        "category": "digestive system",
    },
    {
        "id": "rec2",
        "text": "Apples originated in Central Asia and have been cultivated for thousands of years, with over 7,500 varieties available today.",
        "category": "cultivation",
    },
    {
        "id": "rec3",
        "text": "Rich in vitamin C and other antioxidants, apples contribute to immune health and may reduce the risk of chronic diseases.",
        "category": "immune system",
    },
    {
        "id": "rec4",
        "text": "The high fiber content in apples can also help regulate blood sugar levels, making them a favorable snack for people with diabetes.",
        "category": "endocrine system",
    },
]

# Convert the text into numerical vectors that Pinecone can index
embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[d["text"] for d in data],
    parameters={"input_type": "passage", "truncate": "END"},
)

# Connect to the index
index = pc.Index(INDEX_NAME)

# Sample vector data to insert
vectors = [
    ("id-1", [0.1] * 128),  # Example vector of dimension 128
    ("id-2", [0.2] * 128),
    ("id-3", [0.3] * 128),
]

# Insert vectors into Pinecone
index.upsert(vectors)

print(f"Inserted {len(vectors)} vectors into '{INDEX_NAME}'.")

# Query example: Searching with a sample vector
query_result = index.query(vector=[0.1] * 128, top_k=2, include_metadata=True)
print("Query Result:", query_result)

# List all indexes
print("Available Indexes:", pc.list_indexes().names())
