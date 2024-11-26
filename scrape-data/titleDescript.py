import requests
import json

def fetch_data(query_params):
    # Base URL of the API
    base_url = "https://data.abudhabi/opendata/apis/search_main.php"
    
    # Make the API request with the provided query parameters
    response = requests.get(base_url, params=query_params)
    
    # If the request is successful, return the JSON data
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_data_to_file(data, filename="titleDescript.txt"):
    # Open the file in write mode
    with open(filename, "w", encoding="utf-8") as file:
        # Iterate through each item in the 'data' list from the response
        for item in data:
            # Extract the necessary fields
            title = item.get("title", "N/A")
            title_ar = item.get("titlear", "N/A")
            description = item.get("description", "N/A")
            
            # Write to the file in a readable format
            file.write(f"Title (English): {title}\n")
            # file.write(f"Title (Arabic): {title_ar}\n")
            file.write(f"Description: {description}\n\n")

def main():
    # Define the query parameters (example of sorting by modified date in descending order and filtering by CSV format)
    query_params = {
        'fulltext': '',
        'sort-order': 'desc',
        'sort': 'modified',
        'distribution__item__format': '',
        'publisher__name': '',
        'theme': 'Health'
    }
    
    # Fetch the data from the API
    data = fetch_data(query_params)
    
    # If data is available, save it to a file
    if data and 'data' in data:
        save_data_to_file(data['data'])
        print("Data saved to output.txt")
    else:
        print("No data found or failed to fetch data.")

if __name__ == "__main__":
    main()
