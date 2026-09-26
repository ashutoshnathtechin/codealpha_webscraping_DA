import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_worldbank_news(url):
    print(f"Scraping {url}...")
    
    # Step 3: Fetch the Web Page (Adding headers just in case!)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print(f"Connection error: {e}")
        return []
        
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return []
    
    # Step 4: Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    news_data = []
    
    # Step 5: Extract the Data
    # We will target the "News & Stories" section which contains a list of articles.
    # The articles are stored in <li> tags with the class "item"
    article_elements = soup.find_all('li', class_='item')
    
    for element in article_elements:
        # Extract the Title
        title_tag = element.find('h4', class_='item-title')
        title = title_tag.text.strip() if title_tag else "No Title"
        
        # Extract the Author
        author_tag = element.find('span', class_='author')
        # Authors sometimes have a trailing comma in the text we need to clean up
        author = author_tag.text.strip().rstrip(',') if author_tag else "Unknown"
        
        # Extract the Date
        date_tag = element.find('span', class_='date')
        date = date_tag.text.strip() if date_tag else "No Date"
        
        # Extract the Link
        link_tag = element.find('a')
        href = link_tag.get('href') if link_tag else ""
        
        # Ensure the link is a full URL
        if href and not href.startswith('http'):
            href = "https://data.worldbank.org" + href
            
        news_data.append({
            'Article Title': title,
            'Author': author,
            'Date Published': date,
            'URL': href
        })
            
    return news_data

def main():
    url = "https://data.worldbank.org/?utm_source=chatgpt.com"
    data = scrape_worldbank_news(url)
    
    if data:
        # Step 7: Export to CSV
        df = pd.DataFrame(data)
        
        csv_filename = "worldbank_news_dataset.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"\nSuccess! Extracted {len(df)} news articles and saved to '{csv_filename}'.")
        print("\nPreview of the dataset:")
        print(df.head())
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
