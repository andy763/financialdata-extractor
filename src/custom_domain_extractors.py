"""
Custom domain-specific extractors for outstanding shares
These functions handle specific website patterns for domains with multiple URLs and high error rates
"""

import re
import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def extract_valour_shares(driver, url):
    """
    Custom extractor for valour.com URLs
    Pattern: https://valour.com/en/products/[product-name]
    """
    try:
        logging.info(f"Using Valour custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Look for shares information in various possible locations
        shares_selectors = [
            # Common patterns for Valour pages
            "[data-testid*='shares']",
            "[class*='shares']",
            "[class*='outstanding']",
            "td:contains('Outstanding')",
            "td:contains('Shares')",
            "span:contains('shares')",
            ".product-details td",
            ".fund-details td",
            ".key-facts td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units']):
                        # Extract number from text
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"Selector {selector} failed: {e}")
                continue
        
        # Fallback: look in page source for patterns
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        text = soup.get_text()
        
        # Look for patterns like "Outstanding shares: 1,000,000"
        patterns = [
            r'outstanding\s+shares?[:\s]+(\d{1,15}(?:[,\.\s]\d{1,3})*)',
            r'shares?\s+outstanding[:\s]+(\d{1,15}(?:[,\.\s]\d{1,3})*)',
            r'total\s+shares?[:\s]+(\d{1,15}(?:[,\.\s]\d{1,3})*)',
            r'issued\s+shares?[:\s]+(\d{1,15}(?:[,\.\s]\d{1,3})*)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                shares_str = match.group(1)
                normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                try:
                    shares_value = int(normalized)
                    if 1000 <= shares_value <= 100000000000:
                        return {"outstanding_shares": f"{shares_value:,}"}
                except ValueError:
                    continue
        
        return {"error": "Could not find outstanding shares on Valour page"}
        
    except Exception as e:
        logging.error(f"Valour extractor error: {e}")
        return {"error": f"Valour extraction failed: {str(e)}"}


def extract_vaneck_shares(driver, url):
    """
    Custom extractor for vaneck.com URLs
    Pattern: https://www.vaneck.com/de/en/investments/[product]/overview/
    """
    try:
        logging.info(f"Using VanEck custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # VanEck specific selectors
        shares_selectors = [
            ".fund-facts td",
            ".key-facts td",
            ".product-details td",
            "[class*='shares']",
            "[class*='outstanding']",
            "td[data-label*='shares']",
            "td[data-label*='outstanding']",
            ".fact-sheet-table td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"VanEck selector {selector} failed: {e}")
                continue
        
        # Try to find download links for fact sheets
        try:
            fact_sheet_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "fact sheet")
            fact_sheet_links.extend(driver.find_elements(By.PARTIAL_LINK_TEXT, "Fact Sheet"))
            fact_sheet_links.extend(driver.find_elements(By.PARTIAL_LINK_TEXT, "FACT SHEET"))
            
            if fact_sheet_links:
                logging.info("Found fact sheet link, but PDF parsing not implemented")
        except Exception as e:
            logging.debug(f"Fact sheet search failed: {e}")
        
        return {"error": "Could not find outstanding shares on VanEck page"}
        
    except Exception as e:
        logging.error(f"VanEck extractor error: {e}")
        return {"error": f"VanEck extraction failed: {str(e)}"}


def extract_wisdomtree_shares(driver, url):
    """
    Custom extractor for wisdomtree.eu URLs
    Pattern: https://www.wisdomtree.eu/[locale]/products/ucits-etfs-unleveraged-etps/cryptocurrency/[product]
    """
    try:
        logging.info(f"Using WisdomTree custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # WisdomTree specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-statistics tr td",
            ".product-overview tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".fact-table tr td",
            ".data-table tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"WisdomTree selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on WisdomTree page"}
        
    except Exception as e:
        logging.error(f"WisdomTree extractor error: {e}")
        return {"error": f"WisdomTree extraction failed: {str(e)}"}


def extract_proshares_shares(driver, url):
    """
    Custom extractor for proshares.com URLs
    Pattern: https://www.proshares.com/our-etfs/[category]/[ticker]
    """
    try:
        logging.info(f"Using ProShares custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # ProShares specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-facts tr td",
            ".etf-details tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-point",
            ".fund-data tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"ProShares selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on ProShares page"}
        
    except Exception as e:
        logging.error(f"ProShares extractor error: {e}")
        return {"error": f"ProShares extraction failed: {str(e)}"}


def extract_grayscale_shares(driver, url):
    """
    Custom extractor for grayscale.com URLs
    Pattern: https://www.grayscale.com/funds/[fund-name]
    """
    try:
        logging.info(f"Using Grayscale custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Grayscale specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-statistics tr td",
            ".fund-details tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-table tr td",
            ".fund-overview tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"Grayscale selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on Grayscale page"}
        
    except Exception as e:
        logging.error(f"Grayscale extractor error: {e}")
        return {"error": f"Grayscale extraction failed: {str(e)}"}


def extract_lafv_shares(driver, url):
    """
    Custom extractor for lafv.li URLs
    Pattern: https://www.lafv.li/[locale]/fonds/list/[id] or API URLs
    """
    try:
        logging.info(f"Using LAFV custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # LAFV specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-data tr td",
            ".fund-details tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-row td",
            ".fund-info tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued', 'anteile']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"LAFV selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on LAFV page"}
        
    except Exception as e:
        logging.error(f"LAFV extractor error: {e}")
        return {"error": f"LAFV extraction failed: {str(e)}"}


def extract_augmenta_shares(driver, url):
    """
    Custom extractor for augmentasicav.com URLs
    Pattern: https://augmentasicav.com/documents
    """
    try:
        logging.info(f"Using Augmenta custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Augmenta specific selectors
        shares_selectors = [
            ".document-table tr td",
            ".fund-facts tr td",
            ".key-data tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-table tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"Augmenta selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on Augmenta page"}
        
    except Exception as e:
        logging.error(f"Augmenta extractor error: {e}")
        return {"error": f"Augmenta extraction failed: {str(e)}"}


def extract_invesco_shares(driver, url):
    """
    Custom extractor for invesco.com URLs
    Pattern: https://www.invesco.com/[region]/[locale]/financial-products/etfs/[product]
    """
    try:
        logging.info(f"Using Invesco custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Invesco specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-statistics tr td",
            ".product-details tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-table tr td",
            ".fund-overview tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"Invesco selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on Invesco page"}
        
    except Exception as e:
        logging.error(f"Invesco extractor error: {e}")
        return {"error": f"Invesco extraction failed: {str(e)}"}


def extract_aminagroup_shares(driver, url):
    """
    Custom extractor for aminagroup.com URLs
    Pattern: https://aminagroup.com/individuals/investments/[product]/
    """
    try:
        logging.info(f"Using Amina Group custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Amina Group specific selectors
        shares_selectors = [
            ".product-details tr td",
            ".fund-facts tr td",
            ".key-data tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-table tr td",
            ".investment-details tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"Amina Group selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on Amina Group page"}
        
    except Exception as e:
        logging.error(f"Amina Group extractor error: {e}")
        return {"error": f"Amina Group extraction failed: {str(e)}"}


def extract_rexshares_shares(driver, url):
    """
    Custom extractor for rexshares.com URLs
    Pattern: https://www.rexshares.com/[ticker]/
    """
    try:
        logging.info(f"Using REX Shares custom extractor for: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # REX Shares specific selectors
        shares_selectors = [
            ".fund-facts tr td",
            ".key-statistics tr td",
            ".etf-details tr td",
            "[class*='shares']",
            "[class*='outstanding']",
            ".data-table tr td",
            ".fund-overview tr td"
        ]
        
        for selector in shares_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['outstanding', 'shares', 'units', 'issued']):
                        number_match = re.search(r'(\d{1,15}(?:[,\.\s]\d{1,3})*)', text)
                        if number_match:
                            shares_str = number_match.group(1)
                            normalized = shares_str.replace(',', '').replace(' ', '').replace('.', '')
                            try:
                                shares_value = int(normalized)
                                if 1000 <= shares_value <= 100000000000:
                                    return {"outstanding_shares": f"{shares_value:,}"}
                            except ValueError:
                                continue
            except Exception as e:
                logging.debug(f"REX Shares selector {selector} failed: {e}")
                continue
        
        return {"error": "Could not find outstanding shares on REX Shares page"}
        
    except Exception as e:
        logging.error(f"REX Shares extractor error: {e}")
        return {"error": f"REX Shares extraction failed: {str(e)}"}


def get_custom_extractor(url):
    """
    Returns the appropriate custom extractor function based on the URL domain
    """
    url_lower = url.lower()
    
    if "valour.com" in url_lower:
        return extract_valour_shares
    elif "vaneck.com" in url_lower:
        return extract_vaneck_shares
    elif "wisdomtree.eu" in url_lower:
        return extract_wisdomtree_shares
    elif "proshares.com" in url_lower:
        return extract_proshares_shares
    elif "grayscale.com" in url_lower:
        return extract_grayscale_shares
    elif "lafv.li" in url_lower:
        return extract_lafv_shares
    elif "augmentasicav.com" in url_lower:
        return extract_augmenta_shares
    elif "invesco.com" in url_lower:
        return extract_invesco_shares
    elif "aminagroup.com" in url_lower:
        return extract_aminagroup_shares
    elif "rexshares.com" in url_lower:
        return extract_rexshares_shares
    else:
        return None


def extract_with_custom_function(driver, url):
    """
    Main function to extract outstanding shares using custom domain-specific extractors
    """
    custom_extractor = get_custom_extractor(url)
    
    if custom_extractor:
        logging.info(f"Using custom extractor for {url}")
        return custom_extractor(driver, url)
    else:
        return {"error": "No custom extractor available for this domain"} 