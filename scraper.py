import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_ebay():
    url = "https://www.ebay.com/sch/i.html"
    query = 'Fossil Gengar'
    query_words = query.lower().split()

    params = {
        '_nkw': query,
        '_sacat': '0',
        '_from': 'R40',
        '_ipg': '240',
        'rt': 'nc'
    }

    page_number = 0
    items_list = []

    while page_number < 20:
        page_number += 1
        print(f"Scraping page: {page_number}")
        params['_pgn'] = page_number
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.find_all('div', class_='s-item__wrapper clearfix')
        if not items:
            print("No listings found on this page.")
            break

        for item in items[2:]:
            try:
                title_elem = item.find('div', class_='s-item__title')
                if not title_elem: continue
                title = title_elem.text.strip().lower()

                # Strict filter: title must include all query words
                if not all(word in title for word in query_words):
                    continue

                price = item.find('span', class_='s-item__price').text
                link = item.find('a', class_='s-item__link')['href'].split('?')[0]
                image_url = item.find('div', class_='s-item__image-wrapper image-treatment').find('img').get('src', 'No image URL')

                items_list.append({
                    'Title': title.title(),
                    'Price': price,
                    'Link': link,
                    'Image Link': image_url
                })
            except Exception:
                continue

    df = pd.DataFrame(items_list)
    print(f"\nScraped {len(df)} new listings.\n")
    return df

def filter_items(df):
    forbidden_terms = [
        'proxy', 'custom', 'signed', 'autograph', 'error', 'fake', 'damaged', 'bgs',
        'cgc', '9', '8', '7', '6', '5', '4', '3', '2', '1'
    ]
    mask = ~df['Title'].str.lower().str.contains(r'\b(?:' + '|'.join(forbidden_terms) + r')\b', regex=True)
    return df[mask].reset_index(drop=True)

def save_to_csv(filtered_df, filename="gengar_scrapes.csv"):
    filtered_df['Scraped Date'] = datetime.today().strftime('%Y-%m-%d')
    try:
        existing_df = pd.read_csv(filename)
        before = len(existing_df)
        combined = pd.concat([existing_df, filtered_df])
        combined.drop_duplicates(subset=['Link'], inplace=True)
        after = len(combined)
        combined.to_csv(filename, index=False)
        added = after - before
    except FileNotFoundError:
        filtered_df.to_csv(filename, index=False)
        added = len(filtered_df)
    return added

def main():
    scraped_df = scrape_ebay()
    filtered_df = filter_items(scraped_df)
    added = save_to_csv(filtered_df)
    print(f"Scraped {len(scraped_df)} new listings. {added} added to the CSV.")

if __name__ == "__main__":
    main()
