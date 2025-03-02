import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import io
from text_extractor import TextExtractor

class PDFProcessor:
    def __init__(self):
        self.extractor = TextExtractor()

    def process_pdf(self, pdf_bytes):
        try:
            # Create PDF reader object
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()

            # Process each page
            extracted_data = []
            unscanned_pages = []
            full_text = []

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                full_text.append(text)

                # Extract information
                slip_name = self.extractor.extract_slip_name(text)
                data = {
                    'page': page_num + 1,
                    'sin': self.extractor.extract_sin(text),
                    'slip_name': slip_name,
                    'issuer_name': self.extractor.extract_issuer_name(text),
                    'taxpayer_name': self.extractor.extract_taxpayer_name(text),
                    'text': text  # Include the raw text for custom field detection
                }

                if slip_name == 'Unrecognized':
                    unscanned_pages.append(data)
                else:
                    extracted_data.append(data)

                # Add page to writer
                writer.add_page(page)

                # Add outline (previously bookmark)
                outline_title = (
                    f"{data['slip_name']} - "
                    f"{data['issuer_name'] or 'Unknown Issuer'}"
                )
                writer.add_outline_item(outline_title, page_num)

            # Create output PDF
            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            return output_stream, extracted_data, unscanned_pages, " ".join(full_text)

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def validate_pdf(self, pdf_bytes):
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            return len(reader.pages) > 0
        except:
            return False