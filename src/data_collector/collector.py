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
    url = f"https://gish.amo.gov.hk/internet/linktoimages/GetImageList?FILE_REF={file_ref}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')  # Modify this according to actual structure
    image_urls = [img['src'] for img in images]
    return jsonify(image_urls)

if __name__ == '__main__':
    app.run(port=5002)

