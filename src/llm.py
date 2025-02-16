from openai import OpenAI
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_key_topics_with_subtopics(text):
    """Extract main topics first, then generate subtopics for each main topic."""

    # Step 1: Extract main topics
    main_topics_prompt = f"""
    Extract the main topics from the following text. Return them as a comma-separated list.
    
    Text:
    {text}
    """
    main_topics_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": main_topics_prompt}],
    )

    main_topics = [
        t.strip()
        for t in main_topics_response.choices[0].message.content.split(",")
        if t.strip()
    ]

    if not main_topics:
        return {}  # Return empty dict if no main topics found

    # Step 2: Generate subtopics for each main topic
    topics_with_subtopics = {}

    for topic in main_topics:
        subtopics_prompt = f"""
        Generate detailed subtopics for the following main topic. Return them as a comma-separated list.
        
        Main Topic:
        {topic}
        """
        subtopics_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": subtopics_prompt}],
        )

        subtopics = [
            s.strip()
            for s in subtopics_response.choices[0].message.content.split(",")
            if s.strip()
        ]
        topics_with_subtopics[topic] = subtopics

    return topics_with_subtopics


def sanitize_id(text):
    """Sanitize topic names for Mermaid syntax."""
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    sanitized = re.sub(r"\s+", "_", sanitized.strip())
    return sanitized


def sanitize_text(text):
    """Sanitize text content for Mermaid labels."""
    # Escape special characters that could break Mermaid syntax
    return text.replace('"', "&quot;").replace("(", "&#40;").replace(")", "&#41;")


def generate_mermaid_diagram(title, topics_dict, direction="LR"):
    """Generate a Mermaid mindmap-style diagram with sanitized text."""
    if not topics_dict:
        return f"graph {direction}\n    root[{sanitize_text(title)}]\n    root --> no_topics[No key topics found]"

    mermaid_syntax = f"graph {direction}\n"
    mermaid_syntax += f"    root[{sanitize_text(title)}]\n"

    for key_topic, subtopics in topics_dict.items():
        key_topic_id = sanitize_id(key_topic)
        mermaid_syntax += f'    root --> {key_topic_id}["{sanitize_text(key_topic)}"]\n'

        for subtopic in subtopics:
            subtopic_id = sanitize_id(subtopic)
            mermaid_syntax += (
                f'    {key_topic_id} --> {subtopic_id}["{sanitize_text(subtopic)}"]\n'
            )

    return mermaid_syntax
