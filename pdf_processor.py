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
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()

                # Extract information
                data = {
                    'page': page_num + 1,
                    'sin': self.extractor.extract_sin(text),
                    'slip_name': self.extractor.extract_slip_name(text),
                    'issuer_name': self.extractor.extract_issuer_name(text),
                    'taxpayer_name': self.extractor.extract_taxpayer_name(text)
                }
                extracted_data.append(data)

                # Add page to writer
                writer.add_page(page)

                # Add bookmarks
                if data['slip_name']:
                    writer.add_bookmark(
                        f"{data['slip_name']} - {data['issuer_name'] or 'Unknown Issuer'}",
                        page_num
                    )

            # Create output PDF
            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            return output_stream, extracted_data

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def validate_pdf(self, pdf_bytes):
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            return len(reader.pages) > 0
        except:
            return False
