from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

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

def image_gen(prompt):
    """Generate an image based on the PDF and dictionary."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    return response.data[0].url


    
