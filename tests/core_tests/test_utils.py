import pytest

from brick.utils import sanitize_input, sanitize_for_mongodb, sanitize_svg_content
from brick.utils import DANGEROUS_ATTRS, DANGEROUS_TAGS

# Tests for sanitize_input

def test_sanitize_input_basic_html():
    input_string = "<div>Test & <b>bold</b></div>"
    expected_output = "&lt;div&gt;Test &amp; &lt;b&gt;bold&lt;/b&gt;&lt;/div&gt;"
    assert sanitize_input(input_string) == expected_output

def test_sanitize_input_svg_tag():
    input_string = "<svg><script>alert('xss')</script></svg>"
    assert "<script>" not in sanitize_input(input_string, is_for_svg=True)

def test_sanitize_input_svg_attr():
    input_string = '<svg><circle href="javascript:alert(\'XSS\')"/></svg>'
    assert 'href=' not in sanitize_input(input_string, is_for_svg=True)

def test_sanitize_input_for_db():
    input_string = "{$ne: null}"
    assert sanitize_input(input_string, is_for_db=True) != input_string

# Tests for sanitize_svg_content

def test_sanitize_svg_content_remove_dangerous_tags():
    for tag in DANGEROUS_TAGS:
        input_string = f"<svg><{tag}></{tag}></svg>"
        assert sanitize_svg_content(input_string) == "<svg></svg>"

def test_sanitize_svg_content_remove_dangerous_attrs():
    for attr in DANGEROUS_ATTRS:
        input_string = f'<svg><circle {attr}="dangerous"/></svg>'
        assert attr not in sanitize_svg_content(input_string)

# Tests for sanitize_for_mongodb

def test_sanitize_for_mongodb_dollar_prefix():
    assert sanitize_for_mongodb("$set") == "\uFF04set"

def test_sanitize_for_mongodb_brace_prefix():
    assert sanitize_for_mongodb("{test: 'value'}") == "\uFF04test: 'value'}"

# Test escaping does not affect normal content
def test_sanitize_no_effect_on_normal_content():
    input_string = "Normal string with no special characters"
    assert sanitize_input(input_string) == input_string

# Test input with both DB and SVG sanitization
def test_sanitize_both_db_and_svg():
    input_string = "<svg><script>alert('xss')</script></svg>{$ne: null}"
    svg_sanitized = sanitize_svg_content(input_string)
    both_sanitized = sanitize_input(input_string, is_for_svg=True, is_for_db=True)
    assert svg_sanitized != both_sanitized
    assert "<script>" not in both_sanitized
    # assert "{$" not in both_sanitized

# Edge cases
    
def test_sanitize_empty_string():
    assert sanitize_input("") == ""

def test_sanitize_non_string_input():
    with pytest.raises(TypeError):
        sanitize_input(None)

def test_sanitize_input_only_dangerous_content():
    input_string = "<script>alert('XSS')</script>"
    sanitized = sanitize_input(input_string, is_for_svg=True)
    assert sanitized == ""

def test_sanitize_input_unicode_characters():
    input_string = "测试 <script>alert('XSS')</script> 🚀"
    sanitized = sanitize_input(input_string, is_for_svg=True)
    assert "测试" in sanitized
    assert "🚀" in sanitized
    assert "<script>" not in sanitized

# SVG

def test_sanitize_input_mixed_content():
    input_string = "<div onclick='alert(1)'>Hello {$ne: null}<svg><script></script></svg></div>"
    sanitized = sanitize_input(input_string, is_for_svg=True, is_for_db=True)
    assert "<script>" not in sanitized
    assert "onclick=" not in sanitized
    # assert "{$" not in sanitized

def test_sanitize_input_malformed_tags():
    input_string = "<sv<script>g>alert('XSS')</sv</script>g>"
    sanitized = sanitize_input(input_string, is_for_svg=True)
    assert "<script>" not in sanitized
    assert "</script>" not in sanitized

def test_sanitize_svg_content_valid_attributes():
    input_string = '<svg><circle cx="50" cy="50" r="40" stroke="black" /></svg>'
    sanitized = sanitize_svg_content(input_string)
    assert 'cx="50"' in sanitized
    assert 'stroke="black"' in sanitized

# def test_sanitize_svg_content_nested_dangerous_tags():
#     input_string = "<svg><script><script>alert('xss')</script></script></svg>"
#     assert sanitize_svg_content(input_string) == "<svg></svg>"

# Mongo

# def test_sanitize_for_mongodb_normal_text():
#     input_string = "This is a $text with curly {braces}"
#     sanitized = sanitize_for_mongodb(input_string)
#     assert sanitized == input_string

# def test_sanitize_for_mongodb_multiple_operators():
#     input_string = "{$set: {$ne: null}}"
#     sanitized = sanitize_for_mongodb(input_string)
#     assert sanitized.count("\uFF04") == 2

# def test_sanitize_for_mongodb_various_positions():
#     input_string = "normal {$set} text $end"
#     sanitized = sanitize_for_mongodb(input_string)
#     assert "\uFF04set" in sanitized
#     assert "\uFF04end" in sanitized

