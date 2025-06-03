# Comprehensive Guide to Creating Custom Domain Extractors

## Introduction

Custom domain extractors are specialized functions designed to extract data (such as outstanding shares or stock prices) from specific websites. This guide provides a structured approach to creating robust extractors that work across an entire domain, not just for specific example URLs.

## CRITICAL WARNING ⚠️

**The #1 mistake in creating custom extractors is focusing only on example URLs!**

Custom extractors MUST work for ALL URLs from a domain, not just the specific examples provided. Your implementation must generalize to handle the entire domain's URL patterns and page structures.

## Step-by-Step Guide to Creating a Custom Extractor

### 1. Understand the Domain Structure

Before writing any code:
- Analyze multiple pages from the domain (at least 5-7 different URLs)
- Identify common patterns in the page structure
- Note variations in layouts across different sections of the site
- Understand how the target data (e.g., outstanding shares) is presented

### 2. Design a Multi-Tiered Extraction Strategy

Never rely on a single method! Implement at least 3-4 different extraction approaches:

**Tier 1: Targeted Element Search**
- Look for specific labels, IDs, or class names that typically contain the data
- Use XPath or CSS selectors to target these elements
- Include variations of selectors to handle different page layouts

**Tier 2: Structural Pattern Analysis**
- Look for common structural patterns (tables, key-value pairs, etc.)
- Parse parent-child relationships to find associated values
- Check for specific patterns in element hierarchies

**Tier 3: Text Pattern Matching**
- Use regex patterns to search the entire page text
- Include multiple regex variations to handle different text formats
- Consider international number formats (commas, periods, spaces)

**Tier 4: Fallback Mechanisms**
- For critical domains, include hardcoded values as a last resort
- Map specific URL patterns to known values when available
- Document the source and date of these hardcoded values

### 3. Implement Robust Exception Handling

Error handling is critical for production reliability:
- Catch exceptions at every level of the extraction process
- Log detailed error information for debugging
- Provide meaningful error messages in the return value
- Handle common issues like stale elements and timing problems

### 4. Test Thoroughly Across Multiple URLs

Create a dedicated test script that:
- Tests with at least 5-7 different URLs from the domain
- Includes URLs with different layouts and content structures
- Measures success rate across all URLs
- Documents any special cases or limitations

### 5. Code Structure Best Practices

Structure your extractor function with these sections:

```python
def extract_domain_shares(driver, url):
    """
    Custom extractor for domain.com URLs
    Designed to work on ALL domain.com URLs, not just specific patterns
    Pattern: https://domain.com/[section]/[subsection]
    """
    try:
        # 1. Setup and preparation
        logging.info(f"Using Domain custom extractor for: {url}")
        driver.get(url)
        
        # 2. Handle cookie consent if needed
        try:
            # Cookie consent handling code
        except Exception as e:
            logging.debug(f"Cookie handling failed: {e}")
        
        # 3. Multiple extraction strategies, in order of preference
        
        # Strategy 1: Targeted element search
        # ...
        
        # Strategy 2: Structural pattern analysis
        # ...
        
        # Strategy 3: Text pattern matching
        # ...
        
        # Strategy 4: Fallback mechanisms
        # ...
        
        # 5. Return error if all strategies fail
        return {"error": "Could not find data on Domain page"}
        
    except Exception as e:
        logging.error(f"Domain extractor error: {e}")
        return {"error": f"Domain extraction failed: {str(e)}"}
```

## Common Pitfalls to Avoid

1. **Narrow Focus**: Testing only with provided example URLs
2. **Brittle Selectors**: Using overly specific CSS selectors that break with minor site changes
3. **Insufficient Fallbacks**: Relying on a single extraction method
4. **Poor Error Handling**: Not catching exceptions at different levels
5. **Missing Wait Conditions**: Not waiting for dynamic content to load
6. **Ignoring Cookie Consent**: Many sites require accepting cookies to reveal content
7. **Hardcoded-Only Solutions**: Relying solely on hardcoded values without extraction logic

## Real-World Example: TMX Money Extractor

The TMX Money extractor demonstrates these principles in action:

```python
def extract_tmx_shares(driver, url):
    """
    Custom extractor for money.tmx.com URLs
    Pattern: https://money.tmx.com/en/quote/[SYMBOL]
    """
    try:
        logging.info(f"Using TMX Money custom extractor for: {url}")
        driver.get(url)
        
        # STRATEGY 1: Targeted label search
        label_terms = ["Listed Units Out", "Shares Outstanding", "Units Outstanding"]
        # ... implementation ...
        
        # STRATEGY 2: Structured key-value pairs
        # ... implementation ...
        
        # STRATEGY 3: Table-based search
        # ... implementation ...
        
        # STRATEGY 4: Full page text search
        # ... implementation ...
        
        # STRATEGY 5: Hardcoded values fallback
        # ... implementation ...
        
        return {"error": "Could not find outstanding shares"}
        
    except Exception as e:
        logging.error(f"TMX Money extractor error: {e}")
        return {"error": f"TMX Money extraction failed: {str(e)}"}
```

## Testing Your Custom Extractor

Always create a dedicated test script:

```python
def test_domain_extractor():
    """
    Test the domain.com extractor across multiple URLs
    """
    # List of test URLs from different parts of domain.com
    test_urls = [
        "https://domain.com/section1/page1",
        "https://domain.com/section2/page2",
        # ... at least 5-7 different URLs ...
    ]
    
    # Test implementation
    # ... implementation ...
    
    # Success metrics
    print(f"Success rate: {success_rate:.2f}%")
```

## Conclusion

Creating robust custom domain extractors requires careful planning, multiple extraction strategies, thorough testing, and attention to error handling. By following this guide, you'll create extractors that work reliably across entire domains, not just for specific examples.

Remember: The goal is to build extractors that work for ALL URLs from a domain, not just the specific examples provided. Your future self and team members will thank you for your thoroughness! 