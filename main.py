import streamlit as st
import io
from pdf_processor import PDFProcessor

def main():
    st.set_page_config(
        page_title="Tax Slip PDF Processor",
        page_icon="📄",
        layout="wide"
    )

    st.title("Canadian Tax Slip PDF Processor")
    st.markdown("""
    Upload your tax slip PDFs to automatically:
    - Detect key information
    - Add bookmarks
    - Process multiple pages
    """)

    # Initialize PDF processor
    processor = PDFProcessor()

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
                processed_pdf, extracted_data = processor.process_pdf(pdf_bytes)

                # Display extracted information
                st.subheader("Extracted Information")
                for page_data in extracted_data:
                    with st.expander(f"Page {page_data['page']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Slip Type:**", page_data['slip_name'] or "Not detected")
                            st.write("**SIN:**", page_data['sin'] or "Not detected")
                        
                        with col2:
                            st.write("**Issuer Name:**", page_data['issuer_name'] or "Not detected")
                            st.write("**Taxpayer Name:**", page_data['taxpayer_name'] or "Not detected")

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
        4. Download the processed PDF
        
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
        """)

if __name__ == "__main__":
    main()
