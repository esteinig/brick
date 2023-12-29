import re
import html

# List of potentially dangerous SVG tags and attributes
DANGEROUS_TAGS = ['script', 'alert', 'onclick', 'onerror', 'onload']
DANGEROUS_ATTRS = ['href', 'xlink:href', 'style']

def sanitize_input(input_string: str, is_for_db: bool = False, is_for_svg: bool = False) -> str:
    # Basic HTML escape
    sanitized = html.escape(input_string)

    # Additional sanitization for SVG content
    if is_for_svg:
        sanitized = sanitize_svg_content(sanitized)

    # Additional sanitization for MongoDB queries
    if is_for_db:
        sanitized = sanitize_for_mongodb(sanitized)

    return sanitized

def sanitize_svg_content(input_string: str) -> str:
    for tag in DANGEROUS_TAGS:
        input_string = re.sub(f'<{tag}.*?>.*?</{tag}>', '', input_string, flags=re.IGNORECASE)
    for attr in DANGEROUS_ATTRS:
        input_string = re.sub(f'{attr}=".*?"', '', input_string, flags=re.IGNORECASE)
    return input_string

def sanitize_for_mongodb(input_string: str) -> str:
    # Replace MongoDB operator prefixes
    input_string = re.sub(r'^\$', '\uFF04', input_string)
    input_string = re.sub(r'^\{', '\uFF04', input_string)
    return input_string
