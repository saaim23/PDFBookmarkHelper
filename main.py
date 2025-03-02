import streamlit as st
import io
from pdf_processor import PDFProcessor
import openai

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_chat_response(prompt, context):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant analyzing tax documents. Here's the context from the PDF: {context}"},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def main():
    st.set_page_config(
        page_title="Victoria PDF Helper",
        page_icon="📄",
        layout="wide"
    )

    # Title and Description
    st.title("Victoria PDF Helper")
    st.markdown("""
    Upload your tax slip PDFs to automatically:
    - Detect key information
    - Add bookmarks
    - Process multiple pages
    - Chat with your documents
    """)

    # Initialize states
    initialize_chat_history()

    # Initialize PDF processor
    processor = PDFProcessor()

    # Check for OpenAI API key
    if 'OPENAI_API_KEY' not in st.secrets:
        st.warning("Please set up your OpenAI API key to enable chat functionality.")
        with st.expander("Configure API Key"):
            api_key = st.text_input("Enter your OpenAI API key:", type="password")
            if api_key:
                openai.api_key = api_key
                st.success("API key configured!")

    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Read file
        pdf_bytes = uploaded_file.read()

        # Validate PDF
        if not processor.validate_pdf(pdf_bytes):
            st.error("Invalid PDF file. Please upload a valid PDF document.")
            return

        try:
            with st.spinner("Processing PDF..."):
                # Process PDF
                processed_pdf, extracted_data, unscanned_pages, full_text = processor.process_pdf(pdf_bytes)

                # Add search functionality
                with st.sidebar:
                    st.header("Find in PDF")
                    search_term = st.text_input("Enter text to find:")
                    if search_term:
                        st.subheader("Search Results")
                        found = False
                        for page_num, page_data in enumerate(extracted_data + unscanned_pages):
                            text = page_data.get('text', '')
                            sentences = text.split('.')
                            for sentence in sentences:
                                if search_term.lower() in sentence.lower():
                                    found = True
                                    st.write(f"**Page {page_data['page']}:**")
                                    st.write(f"{sentence.strip()}.")
                                    st.markdown("---")

                        if not found:
                            st.info(f"No matches found for '{search_term}'")

                # Create tabs for different sections
                tabs = st.tabs(["Recognized Slips", "Unscanned Pages", "Chat with PDF"])

                # Tab 1: Recognized Slips
                with tabs[0]:
                    st.subheader("Recognized Tax Slips")
                    for page_data in extracted_data:
                        with st.expander(f"Page {page_data['page']} - {page_data['slip_name']}"):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("**Slip Type:**", page_data['slip_name'])
                                st.write("**SIN:**", page_data['sin'] or "Not detected")

                            with col2:
                                st.write("**Issuer Name:**", page_data['issuer_name'] or "Not detected")
                                st.write("**Taxpayer Name:**", page_data['taxpayer_name'] or "Not detected")

                # Tab 2: Unscanned Pages
                with tabs[1]:
                    st.subheader("Unscanned Pages")
                    if unscanned_pages:
                        for page_data in unscanned_pages:
                            with st.expander(f"Page {page_data['page']}"):
                                st.write("This page couldn't be automatically categorized.")
                                st.write("**Found Information:**")
                                if page_data['sin']:
                                    st.write("- SIN:", page_data['sin'])
                                if page_data['issuer_name']:
                                    st.write("- Issuer:", page_data['issuer_name'])
                                if page_data['taxpayer_name']:
                                    st.write("- Taxpayer:", page_data['taxpayer_name'])
                    else:
                        st.info("All pages were successfully categorized!")

                # Tab 3: Chat with PDF
                with tabs[2]:
                    st.subheader("Chat with your PDF")
                    if 'OPENAI_API_KEY' in st.secrets or openai.api_key:
                        user_question = st.text_input("Ask a question about your tax documents:")
                        if user_question:
                            with st.spinner("Getting response..."):
                                response = get_chat_response(user_question, full_text)
                                st.write("**Answer:**", response)
                    else:
                        st.warning("Please configure your OpenAI API key to use the chat feature.")

                # Download button for processed PDF
                st.download_button(
                    label="Download Processed PDF",
                    data=processed_pdf,
                    file_name="processed_tax_slips.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. Upload your tax slip PDF
        2. Wait for processing
        3. Review extracted information
        4. Search for specific text
        5. Chat with your documents
        6. Download the processed PDF

        **Note:** The processed PDF will include:
        - Bookmarks for each slip
        - Extracted information
        """)

        st.header("Supported Tax Slips")
        st.markdown("""
        - T4 (Statement of Remuneration Paid)
        - T4A (Statement of Pension)
        - T5 (Statement of Investment Income)
        - T3 (Statement of Trust Income)
        - T5008 (Statement of Securities Transactions)
        - T1135 (Foreign Income Verification)
        - Capital Gains/Realized Gain Summary
        - Tax Return Summary
        """)

    # Add watermark at the bottom of the page
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #888;'>Made with pyaar by saaim ❤️</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()