import re
from typing import Dict, Optional

class CustomPatternManager:
    def __init__(self):
        # Default patterns for common fields
        self.patterns: Dict[str, str] = {
            'amount': r'\$\s*[\d,]+\.?\d*',
            'date': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            'account_number': r'Account\s*#?\s*:\s*(\d+)',
            'box_number': r'Box\s*(\d+)',
            'box_amount': r'Box\s*\d+\s*:\s*(\$?\s*[\d,]+\.?\d*)',
        }
    
    def add_pattern(self, name: str, pattern: str) -> bool:
        """Add a new custom pattern."""
        try:
            # Validate pattern by testing compilation
            re.compile(pattern)
            self.patterns[name] = pattern
            return True
        except re.error:
            return False
    
    def remove_pattern(self, name: str) -> bool:
        """Remove a custom pattern."""
        if name in self.patterns:
            del self.patterns[name]
            return True
        return False
    
    def extract_field(self, text: str, pattern_name: str) -> Optional[str]:
        """Extract field using named pattern."""
        if pattern_name not in self.patterns:
            return None
        
        match = re.search(self.patterns[pattern_name], text)
        return match.group(1) if match and match.groups() else match.group(0) if match else None
    
    def extract_all_fields(self, text: str) -> Dict[str, str]:
        """Extract all defined fields from text."""
        results = {}
        for name, pattern in self.patterns.items():
            match = self.extract_field(text, name)
            if match:
                results[name] = match
        return results
