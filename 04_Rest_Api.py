import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BookFetcher:
    def __init__(self, query, limit=10):
        self.api_url = "http://openlibrary.org/search.json"
        self.query = query
        self.limit = limit
        self.books = []
        self.session = requests.Session()

    def fetch_data(self):
        """Fetching data from the Open Library API."""
        params = {
            'q': self.query,
            'limit': self.limit
        }
        try:
            response = self.session.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            self.books = data['docs']
            logging.info(f"Fetched {len(self.books)} books from the API.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from the API: {e}")
            self.books = []

    def process_data(self):
        """Process the fetched data into a DataFrame."""
        processed_books = []
        for book in self.books:
            book_info = {
                'title': book.get('title', 'N/A'),
                'author_name': ', '.join(book.get('author_name', ['N/A'])),
                'first_publish_year': book.get('first_publish_year', 'N/A'),
                'isbn': ', '.join(book.get('isbn', ['N/A']))
            }
            processed_books.append(book_info)
        
        df = pd.DataFrame(processed_books)
        return df

    def save_to_csv(self, df, csv_file='books.csv'):
        """Save the DataFrame to a CSV file."""
        try:
            df.to_csv(csv_file, index=False)
            logging.info(f"Data saved to {csv_file}")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {e}")

    def close_session(self):
        """Close the requests session."""
        self.session.close()

if __name__ == "__main__":
    # Creating an instance of BookFetcher
    book_fetcher = BookFetcher(query='python programming', limit=10)
    
    # Fetching the data
    book_fetcher.fetch_data()
    
    # Processing the data into a DataFrame
    df = book_fetcher.process_data()
    
    # Saveving the DataFrame to a CSV file
    book_fetcher.save_to_csv(df)
    
    # Closing the session
    book_fetcher.close_session()
