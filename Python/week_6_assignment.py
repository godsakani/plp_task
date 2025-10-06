# Example Output
# Terminal Output Text
# Welcome to the Ubuntu Image Fetcher
# A tool for mindfully collecting images from the web
# https://example.com/ubuntu-wallpaper.jpg
# Please enter the image URL: 
# ✓ Successfully fetched: ubuntu-wallpaper.jpg
# ✓ Image saved to Fetched_Images/ubuntu-wallpaper.jpg
import requests
import os
from urllib.parse import urlparse
from requests.exceptions import MissingSchema, RequestException, ConnectionError, HTTPError

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URL from user
    url = input("Please enter the image url1, url2, url3.... ")
    clean_urls = []
    pic_count = 1
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
        
        # Fetch the image
        raw_urls = url.split(',')
        for urls in raw_urls:
            clean_urls.append(urls.strip())
            
        for urls in clean_urls:
            response = requests.get(urls, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
        
            # Extract filename from URL or generate one
            parsed_url = urlparse(urls)
            filename = os.path.basename(parsed_url.path)
                
            if not filename:
                filename = f"downloaded_image_{pic_count}.jpg"
                print(filename)
            else:
                filename = f"{pic_count}_{filename}.jpg"
            # Save the image
            filepath = os.path.join("Fetched_Images", filename)
                
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")
            print("\nConnection strengthened. Community enriched.")
    except MissingSchema:
        print(f"✗ Invalid URL (No scheme supplied. Please include 'http://' or 'https://')")
    except HTTPError as e:
        print(f"✗ HTTP Error {e}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        

if __name__ == "__main__":
    main()
# Challenge Questions

# Modify the program to handle multiple URLs at once.

# Implement precautions that you should  take when downloading files from unknown sources.

# Implement a feature that prevents downloading duplicate images.

# Implement what HTTP headers might be important to check before saving the response content.

# Evaluation Criteria

# Proper use of the requests library for fetching content

# Effective error handling for network issues

# Appropriate file management and directory creation

# Clean, readable code with clear comments

# Faithfulness to Ubuntu principles of community and respect
 
# Remember:
# "A person is a person through other persons." - Ubuntu philosophy. Your program connects you to the work of others across the web.
# Test case:
# # https://picsum.photos/id/237/200/300, https://picsum.photos/id/1/400/300,https://picsum.photos/id/1050/400/500