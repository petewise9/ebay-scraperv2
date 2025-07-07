# eBay Scraper Tutorial

## Overview

This Python scraper collects Pokemon card listings from eBay, by default targeting **Fossil Gengar PSA 10** cards. It scrapes multiple pages, filters unwanted listings, and saves results to CSV with deduplication. With Github Actions, it runs automatically once per day.

## Installation

1. **Install required packages:**
   ```bash
   pip install requests beautifulsoup4 pandas lxml
   ```

2. **Run the scraper:**
   ```bash
   python scraper.py
   ```

## Usage

### Basic Usage
The scraper automatically searches for "Fossil Gengar PSA 10" by default and saves results to `gengar_scrapes.csv`.

### Customizing Search
To search for different items, modify the `query` variable:
```python
query = 'Your Search Term Here'  # e.g., 'Charizard PSA 10'
```

## Code Structure

### Main Functions

**`scrape_ebay()`** - Core scraping function
- Scrapes up to 20 pages of eBay results (can change page limits)
- Extracts title, price, link, and image URL
- Applies strict keyword matching

**`filter_items(df)`** - Removes unwanted listings
- Filters out custom, fake, damaged, and lower-grade cards
- Removes non-PSA graded items (BGS, CGC)

**`save_to_csv()`** - Data persistence
- Saves to CSV with timestamp
- Merges with existing data and removes duplicates

### Data Collected

| Field | Description |
|-------|-------------|
| Title | Item title from eBay |
| Price | Current listing price |
| Link | Direct link to listing |
| Image Link | URL to item image |
| Scraped Date | Date when scraped |

## Key Features

### Filtering System
The scraper removes listings containing:
- `proxy`, `custom`, `fake` - Non-authentic cards
- `signed`, `autograph` - Altered cards
- `error`, `damaged` - Damaged cards
- `bgs`, `cgc` - Non-PSA graded cards
- `9`, `8`, `7`, etc. - Lower grade cards

### Output Example
```csv
Title,Price,Link,Image Link,Scraped Date
Fossil Gengar Holo Pokemon Card Psa 10,$125.00,https://www.ebay.com/itm/...,https://i.ebayimg.com/...,2024-01-15
```
- Currently set up to populate an existing CSV. If no csv by that name exists, then the script will create one first. 

## Configuration

### Change Page Limit
```python
while page_number < 20:  # Modify number here
```

### Modify Filters
```python
forbidden_terms = [
    'proxy', 'custom',    # Keep these
    'your_new_term',      # Add new terms
]
```

## Other Notes

- You can run it manually from Github
- Only scrapes publicly available data
- Includes natural delays between requests

## Troubleshooting

**Empty results:** Search query may be too specific

## Extensions

### Add New Data Fields
```python
# In the scraping loop
condition = item.find('span', class_='SECONDARY_INFO').text
items_list.append({
    # existing fields...
    'Condition': condition  # New field
})
```

### Multiple Search Queries
```python
queries = ['Fossil Gengar PSA 10', 'Base Set Charizard PSA 10']
for query in queries:
    # Run scraper for each query
```

## Summary

This scraper demonstrates key web scraping concepts including HTTP requests, HTML parsing, data filtering, and CSV management. It's designed for educational purposes while providing practical market research value. 

Remember to use responsibly and in accordance with eBay's terms of service.