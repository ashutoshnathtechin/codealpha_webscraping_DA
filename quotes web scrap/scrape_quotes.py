import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_quotes(base_url, max_pages=5):
    """
    Scrapes quotes, authors, and tags from quotes.toscrape.com.
    Handles pagination automatically up to max_pages.
    """
    quotes_data = []
    
    for page in range(1, max_pages + 1):
        # The pagination structure is /page/1/, /page/2/, etc.
        url = f"{base_url}page/{page}/"
        print(f"Scraping page {page}: {url}")
        
        # Step 3: Fetch the Web Page
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            break
            
        # Step 4: Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Step 5: Extract the Data
        # Each quote is inside a <div class="quote">
        quote_elements = soup.find_all('div', class_='quote')
        
        # If no quotes are found, we've likely hit a page that doesn't exist
        if not quote_elements:
            print("No more quotes found. Ending pagination.")
            break
            
        for element in quote_elements:
            # Extract Quote Text (inside <span class="text">)
            text = element.find('span', class_='text').text
            
            # Extract Author (inside <small class="author">)
            author = element.find('small', class_='author').text
            
            # Extract Tags (inside <a class="tag"> inside <div class="tags">)
            tags_elements = element.find('div', class_='tags').find_all('a', class_='tag')
            tags = [tag.text for tag in tags_elements]
            # Convert list of tags into a single comma-separated string
            tags_string = ", ".join(tags)
            
            # Append to our list of dictionaries
            quotes_data.append({
                'Quote': text,
                'Author': author,
                'Tags': tags_string
            })
            
        # Be polite to the server by waiting a second between page requests
        time.sleep(1)
        
    return quotes_data

def main():
    base_url = "http://quotes.toscrape.com/"
    print("Starting Quotes scraping project...")
    
    # Scrape the first 5 pages to get a good dataset (50 quotes)
    quotes = scrape_quotes(base_url, max_pages=5)
    
    if quotes:
        # Step 7: Export to CSV
        df = pd.DataFrame(quotes)
        
        # Using utf-8-sig to ensure quotes/special characters display correctly in Excel
        csv_filename = "quotes_dataset.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"\nSuccess! Extracted {len(quotes)} quotes and saved to '{csv_filename}'.")
        print("\nPreview of the dataset:")
        print(df.head())
    else:
        print("No quotes were extracted.")

if __name__ == "__main__":
    main()
