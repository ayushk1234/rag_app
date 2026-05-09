import os
from openai import OpenAI
from dotenv import load_dotenv

from app.vector_store import search_chunks
from app.prompts import SYSTEM_PROMPT

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Build context from the search results
def build_context(search_results):

    documents = search_results["documents"][0]
    metadatas = search_results["metadatas"][0]

    context_parts = []
    citations = []

    for doc, metadata in zip(documents, metadatas):

        source = metadata["source"]
        page = metadata["page"]

        context_parts.append(
            f"""
            Source: {source}
            Page: {page}

            Content:
            {doc}
            """
        )

        citations.append(
            f"{source} (Page {page})"
        )

    context = "\n\n".join(context_parts)

    return context, citations

# RAG pipeline
def ask_question(query):
    

    # Step 1: Retrieve relevant chunks
    search_results = search_chunks(query)

    # Step 2: Build context
    context, citations = build_context(search_results)

    # Step 3: Create user prompt
    user_prompt = f"""
    Context:
    {context}

    Question:
    {query}
    """

    # Step 4: Generate answer
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    # If the LLM says it couldn't find the info, don't show citations
    if "I could not find this information in the uploaded documents" in answer:
        citations = []

    return {
        "answer": answer,
        "citations": list(set(citations))
    }

