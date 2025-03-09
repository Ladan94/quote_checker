import re
import requests
from bs4 import BeautifulSoup

def extract_quotes(text):
    """Finds and returns all quoted text from an article."""
    return re.findall(r'"(.*?)"|“(.*?)”', text)

def search_quote_online(quote):
    """Searches the quote on Google and checks if it appears in reliable sources."""
    query = f'"{quote}" site:wikipedia.org OR site:scholar.google.com'
    search_url = f"https://www.google.com/search?q={query}"
    
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents blocking by Google
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return False, "Error: Unable to fetch search results"
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")

    if results:
        return True, results[0].text  # First search result
    else:
        return False, "No matching sources found"

def analyze_text(text):
    """Checks all quotes in the text and verifies their accuracy."""
    quotes = extract_quotes(text)
    quotes = [q[0] or q[1] for q in quotes]  # Remove empty matches
    report = []

    for quote in quotes:
        is_valid, source = search_quote_online(quote)
        if is_valid:
            report.append(f"✅ Verified: \"{quote}\" (Found source: {source})")
        else:
            report.append(f"⚠️ Unverified: \"{quote}\" (No valid source found)")

    return "\n".join(report)

# Example usage
if __name__ == "__main__":
    text = '''
    Albert Einstein once said, "Imagination is more important than knowledge."
    However, some believe that "Knowledge is everything" – but this quote is often misattributed.
    '''
    
    result = analyze_text(text)
    print(result)
