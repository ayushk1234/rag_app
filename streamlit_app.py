import os
import streamlit as st

from app.pdf_parser import process_pdf
from app.vector_store import store_chunks
from app.rag import ask_question


# Create upload directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "data",
    "uploads"
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

#page configuration
st.set_page_config(
    page_title="Document Q&A App",
    layout="wide"
)

#streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "show_success" not in st.session_state:
    st.session_state.show_success = False




# Sidebar for document uploading
with st.sidebar:

    st.title("Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.uploader_key}"
    )


    if st.session_state.show_success:
        st.success("Documents processed successfully!")
        st.session_state.show_success = False

    process_button = st.button(
        "Process Documents"
    )

    if process_button:

        if not uploaded_files:

            st.warning("Please upload at least one PDF.")

        else:

            all_chunks = []
            all_saved_paths = []

            with st.spinner("Processing documents..."):

                for uploaded_file in uploaded_files:

                    # Saving file
                    print("uploaded file",uploaded_file.name)
                    save_path = os.path.abspath(os.path.join(
                        UPLOAD_DIR,
                        uploaded_file.name
                    ))

                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    print("Saved file path:", save_path)
                    all_saved_paths.append(save_path)
                

                # Process all PDFs
                all_chunks = process_pdf(all_saved_paths)

                # Store in vector DB
                store_chunks(all_chunks)


            st.session_state.documents_processed = True
            st.session_state.uploader_key += 1
            st.session_state.show_success = True
            st.rerun()



# Page Title
st.title("Document Q&A Chatbot")

if not st.session_state.documents_processed:

    st.info("Kindly upload and process PDFs to begin .")

else:

    # Display previous messages 
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Display citations if assistant message
            if (message["role"] == "assistant"and "citations" in message):

                st.markdown("### Sources")

                for citation in message["citations"]:
                    st.markdown(f"- {citation}")


    # Chat input
    user_query = st.chat_input(
        "Ask a question about the documents..."
    )

    if user_query:

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner("Generating answer..."):

                response = ask_question(user_query)

                answer = response["answer"]

                citations = response["citations"]

                st.markdown(answer)

                st.markdown("### Sources")

                for citation in citations:
                    st.markdown(f"- {citation}")

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "citations": citations
        })