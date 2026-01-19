import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

#Fetch webpage content
def fetch_page(url):
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    
#Parse HTML and extract book data
def parse_page(html):
    
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    book_list = []

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        price = price.replace("Â", "").replace("A", "")
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.p["class"][1]   # Example: One, Two, Three

        book_list.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })

    return book_list

#Save data into CSV file
def save_to_csv(data, filename):
    
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["Title", "Price", "Availability", "Rating"]
            )
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"Error saving CSV: {e}")

#Main function to scrape multiple pages
def scrape_books(pages=5):
    
    all_books = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        url = BASE_URL.format(page)
        html = fetch_page(url)

        if html:
            books = parse_page(html)
            all_books.extend(books)

    return all_books

if __name__ == "__main__":
    books_data = scrape_books(pages=5)
    save_to_csv(books_data, "books.csv")
    print("Scraping completed. Data saved to books.csv")
