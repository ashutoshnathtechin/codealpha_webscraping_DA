import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_books(base_url, max_pages=1):
    books_data = []
    
    for page in range(1, max_pages + 1):
        # Handle pagination URL
        if page == 1:
            url = base_url + "index.html"
        else:
            url = base_url + f"catalogue/page-{page}.html"
            
        print(f"Scraping page {page}: {url}")
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all book articles
        articles = soup.find_all('article', class_='product_pod')
        if not articles:
            break
            
        for article in articles:
            # Extract title
            title = article.h3.a.get('title')
            
            # Extract price
            price_element = article.find('div', class_='product_price').find('p', class_='price_color')
            price = price_element.text if price_element else "N/A"
            
            # Extract rating (class contains 'star-rating' and the actual rating e.g., 'Three')
            rating_element = article.find('p', class_='star-rating')
            rating = rating_element['class'][1] if rating_element and len(rating_element['class']) > 1 else "None"
            
            # Extract link
            link = article.h3.a.get('href')
            if not link.startswith('catalogue/'):
                full_link = base_url + link
            else:
                full_link = base_url + link
                
            books_data.append({
                'Title': title,
                'Price': price,
                'Rating': rating,
                'URL': full_link
            })
            
        # Be polite and wait a bit between requests
        time.sleep(1)
        
    return books_data

def main():
    base_url = "https://books.toscrape.com/"
    
    # We will scrape the first 3 pages as an example
    max_pages = 3 
    
    print("Starting scraping process...")
    books = scrape_books(base_url, max_pages)
    
    if books:
        df = pd.DataFrame(books)
        csv_filename = "books_dataset.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"\nSuccess! Extracted {len(books)} books and saved to {csv_filename}")
        print("\nSample of scraped data:")
        print(df.head())
    else:
        print("No data was extracted.")

if __name__ == "__main__":
    main()
