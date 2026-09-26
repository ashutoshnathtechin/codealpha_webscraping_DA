import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nasa_homepage(url):
    """
    Scrapes the NASA Open Data Portal homepage to extract 
    all the listed data archives and important links.
    """
    print(f"Scraping {url}...")
    
    # Step 3: Fetch the Web Page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
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
    links_data = []
    
    # Step 5: Extract the Data
    # On the NASA homepage, datasets aren't listed in a table; 
    # instead, the page contains links to various data archives and portals.
    # We will find all 'a' (anchor) tags.
    for a_tag in soup.find_all('a'):
        text = a_tag.get_text(strip=True)
        href = a_tag.get('href')
        
        # Filter: We only want valid external or absolute links that have descriptive text
        if text and href and href.startswith('http'):
            links_data.append({
                'Link Title': text,
                'URL': href
            })
            
    return links_data

def main():
    # The URL provided
    url = "https://data.nasa.gov/?utm_source=chatgpt.com"
    
    # Scrape the page
    data = scrape_nasa_homepage(url)
    
    if data:
        # Step 7: Export to CSV
        # Convert to Pandas DataFrame
        df = pd.DataFrame(data)
        
        # Remove duplicate links to clean the dataset
        df = df.drop_duplicates()
        
        # Save to CSV
        csv_filename = "nasa_portal_links.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        print(f"\nSuccess! Extracted {len(df)} unique links and saved to '{csv_filename}'.")
        print("\nPreview of the dataset:")
        print(df.head(10))
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
