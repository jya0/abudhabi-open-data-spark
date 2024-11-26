import requests
import os

# Define API endpoints
SEARCH_MAIN_URL = "https://data.abudhabi/opendata/apis/search_main.php"
SEARCH_INNER_URL = "https://data.abudhabi/opendata/apis/search_inner.php"

# Directory to save CSV files
SAVE_DIR = "downloaded_csvs"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_dataset_identifiers():
    """Fetch the list of dataset identifiers from the main API."""
    params = {
        'fulltext': '',
        'sort-order': 'desc',
        'sort': 'modified',
        'distribution__item__format': '',
        'publisher__name': '',
        'theme': 'Health'
    }
    try:
        response = requests.get(SEARCH_MAIN_URL, params=params)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        if data["status"] == 200:
            return [item["identifier"] for item in data.get("data", [])]
        else:
            print("Error fetching dataset identifiers")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dataset identifiers: {e}")
        return []

def fetch_dataset_details(identifier):
    """Fetch dataset details from the inner API using the identifier."""
    try:
        response = requests.get(SEARCH_INNER_URL, params={"identifier": identifier})
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        if data["status"] == 200:
            return data["data"]
        else:
            print(f"Error fetching details for identifier {identifier}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dataset details for {identifier}: {e}")
        return None

def download_csv(url, title):
    """Download the CSV file from the given URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        filename = f"{title.replace(' ', '_')}.csv"
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {title}: {e}. Skipping this dataset.")

def main():
    """Main function to orchestrate the process."""
    identifiers = fetch_dataset_identifiers()
    print(f"Found {len(identifiers)} datasets to process.")
    
    for identifier in identifiers:
        details = fetch_dataset_details(identifier)
        if details and "distribution" in details:
            for distribution in details["distribution"]:
                if distribution["format"].lower() == "csv":
                    csv_url = distribution["url"]
                    title = distribution.get("title", f"dataset_{identifier}")
                    download_csv(csv_url, title)
                else:
                    print(f"No CSV format found for identifier {identifier}")

if __name__ == "__main__":
    main()
