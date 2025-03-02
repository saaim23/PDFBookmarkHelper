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
        # Enhanced Canadian tax slip patterns
        slip_patterns = {
            'T4': r'T4\s*(Statement of Remuneration Paid)?',
            'T4A': r'T4A\s*(Statement of Pension|Statement of Pension, Retirement, Annuity)',
            'T5': r'T5\s*(Statement of Investment Income)',
            'T3': r'T3\s*(Statement of Trust Income)',
            'T5008': r'T5008\s*(Statement of Securities Transactions)',
            'T1135': r'T1135\s*(Foreign Income Verification Statement)',
            'T2200': r'T2200\s*(Declaration of Conditions of Employment)',
            'T2202': r'T2202\s*(Tuition and Enrolment Certificate)',
            'T5013': r'T5013\s*(Statement of Partnership Income)',
            'Capital Gains': r'(Capital Gains|Realized Gain)\s*(Summary|Statement)',
            'RRSP': r'RRSP\s*(Contribution Receipt|Statement)',
            'Summary': r'(Tax Return Summary|T1 Summary|Summary of.*Returns)',
            'T777': r'T777\s*(Statement of Employment Expenses)',
            'T2125': r'T2125\s*(Statement of Business Activities)'
        }

        for slip_type, pattern in slip_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return slip_type
        return 'Unrecognized'

    @staticmethod
    def extract_issuer_name(text):
        # Enhanced business identifiers
        patterns = [
            r'(?:Issuer|Payer|Employer|Institution)[:]\s*([^\n]*)',
            r'(?:Company|Business|Fund) Name[:]\s*([^\n]*)',
            r'(?:From|By)[:]\s*([^\n]*\b(?:Inc|Ltd|Corp|Limited|Bank|Trust|Services)\b[^\n]*)',
            r'(?:Issued by|Prepared by)[:]\s*([^\n]*)',
            r'\b(?:CRA Business Number|Business Number)[:]\s*\d{9}[A-Z]{2}\d{4}\s*([^\n]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_taxpayer_name(text):
        # Enhanced recipient/employee name patterns
        patterns = [
            r'(?:Recipient|Employee|Individual|Taxpayer)[\s]*Name[:]\s*([^\n]*)',
            r'(?:Last Name|Surname)[\s]*,[\s]*(?:First Name|Given Name)[:]\s*([^\n]*)',
            r'(?:Name of|To)[:]\s*([^\n]*)',
            r'(?:Beneficiary|Client)[\s]*Name[:]\s*([^\n]*)',
            r'\b(?:First name|Last name)[:]\s*([^\n]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_tax_year(text):
        # Look for tax year
        patterns = [
            r'(?:Tax Year|Year|Taxation Year)[:]\s*(\d{4})',
            r'\b(20\d{2})\s*(?:Tax Year|Year)\b',
            r'\bFor\s*(20\d{2})\b'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def extract_text_for_chat(text):
        # Clean and format text for chat context
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        return cleaned_text