# src/data_collector/collector.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
# Allow all domains to access this service
CORS(app)

@app.route('/fetch-images', methods=['GET'])
def fetch_images():
    file_ref = request.args.get('fileRef')
    print(f"Fetching images for File Reference: {file_ref}")  # Debugging: log file reference

    url = f"https://gish.amo.gov.hk/internet/linktoimages/GetImageList?FILE_REF={file_ref}"
    print(f"Constructed URL: {url}")  # Debugging: log the constructed URL

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: HTTP {response.status_code}")  # Error logging
        return jsonify({'error': 'Failed to fetch data', 'status_code': response.status_code}), 500

    print("Data fetched successfully, parsing HTML...")  # Debugging: successful fetch

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')  # Modify this according to actual structure
    image_urls = [img['src'] for img in images]
    print(f"Extracted {len(image_urls)} images")  # Debugging: number of images extracted

    return jsonify(image_urls)

if __name__ == '__main__':
    app.run(port=5002, debug=True)

