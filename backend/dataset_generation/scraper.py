import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

class DocScraper:
    def __init__(self, base_url, output_dir="raw_data", max_pages=50):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.output_dir = output_dir
        self.max_pages = max_pages
        self.visited = set()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain and url.startswith(self.base_url)

    def clean_text(self, text):
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def scrape_page(self, url):
        if url in self.visited or len(self.visited) >= self.max_pages:
            return
        
        print(f"Scraping: {url}")
        self.visited.add(url)
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to retrieve {url}")
                return

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content - heuristic for common doc sites (Docusaurus, Sphinx, MkDocs)
            # Try to find common content articles, fallback to body
            content_div = soup.find('article') or soup.find('main') or soup.find('div', class_='content') or soup.find('body')
            
            if content_div:
                # Remove navigation, headers, footers if inside content
                for tag in content_div.find_all(['nav', 'header', 'footer', 'script', 'style']):
                    tag.decompose()
                
                text = content_div.get_text(separator=' \n ')
                cleaned_text = self.clean_text(text)
                
                # Save to file
                filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + ".txt"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Source: {url}\n\n")
                    f.write(cleaned_text)
                    
            # Find links
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                # Remove fragment
                full_url = full_url.split('#')[0]
                
                if self.is_valid_url(full_url) and full_url not in self.visited:
                    self.scrape_page(full_url)
                    
            time.sleep(0.5) # Be polite using rate limiting
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    # Default to Polars docs as an example
    TARGET_URL = "https://docs.pola.rs/"
    scraper = DocScraper(TARGET_URL, output_dir="raw_data", max_pages=20)
    scraper.scrape_page(TARGET_URL)
    print(f"Finished scraping. Files saved to {scraper.output_dir}")
