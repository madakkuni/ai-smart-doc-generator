import re

class Sanitizer:
    def __init__(self):
        # Regular expressions for sensitive data
        self.patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'api_key': r'(?i)(?:key|token|api_key|secret|password|pwd)\s*[=:]\s*[\'"]?([a-zA-Z0-9_\-]{8,})[\'"]?',
            'jwt': r'ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*'
        }

    def sanitize(self, text: str) -> str:
        if not isinstance(text, str):
            return text
            
        sanitized_text = text
        
        # Mask emails
        sanitized_text = re.sub(self.patterns['email'], '[REDACTED_EMAIL]', sanitized_text)
        
        # Mask URLs
        sanitized_text = re.sub(self.patterns['url'], '[REDACTED_URL]', sanitized_text)
        
        # Mask API keys and passwords
        def mask_secret(match):
            full_match = match.group(0)
            secret = match.group(1)
            return full_match.replace(secret, '[REDACTED_SECRET]')
            
        sanitized_text = re.sub(self.patterns['api_key'], mask_secret, sanitized_text)
        
        # Mask JWTs
        sanitized_text = re.sub(self.patterns['jwt'], '[REDACTED_JWT]', sanitized_text)
        
        return sanitized_text

sanitizer = Sanitizer()

def sanitize_content(content: str) -> str:
    return sanitizer.sanitize(content)
