import re

class TextExtractor:
    @staticmethod
    def extract_sin(text):
        # Look for 9-digit number pattern (Canadian SIN)
        sin_pattern = r'\b\d{3}\s*\d{3}\s*\d{3}\b'
        match = re.search(sin_pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_slip_name(text):
        # Common Canadian tax slip patterns
        slip_patterns = {
            'T4': r'T4\s*(Statement of Remuneration Paid)?',
            'T4A': r'T4A\s*(Statement of Pension)',
            'T5': r'T5\s*(Statement of Investment Income)',
            'T3': r'T3\s*(Statement of Trust Income)',
            'T5008': r'T5008\s*(Statement of Securities Transactions)',
            'T1135': r'T1135\s*(Foreign Income Verification Statement)',
            'Capital Gains': r'(Capital Gains|Realized Gain)\s*(Summary|Statement)',
            'Summary': r'(Tax Return Summary|T1 Summary|Summary of.*Returns)'
        }

        for slip_type, pattern in slip_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return slip_type
        return 'Unrecognized'

    @staticmethod
    def extract_issuer_name(text):
        # Look for common business identifiers
        patterns = [
            r'(?:Issuer|Payer|Employer|Institution)[:]\s*([^\n]*)',
            r'(?:Company|Business|Fund) Name[:]\s*([^\n]*)',
            r'(?:From|By)[:]\s*([^\n]*\b(?:Inc|Ltd|Corp|Limited|Bank)\b[^\n]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_taxpayer_name(text):
        # Look for recipient/employee name
        patterns = [
            r'(?:Recipient|Employee|Individual|Taxpayer)[\s]*Name[:]\s*([^\n]*)',
            r'(?:Last Name|Surname)[\s]*,[\s]*(?:First Name|Given Name)[:]\s*([^\n]*)',
            r'(?:Name of|To)[:]\s*([^\n]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_text_for_chat(text):
        # Clean and format text for chat context
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        return cleaned_text