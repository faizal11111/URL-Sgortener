# main.py

from flask import Flask, jsonify, request, redirect
from .models import URLMapping
from .utils import generate_short_code, is_valid_url
from datetime import datetime
app = Flask(__name__)
url_mapping = URLMapping()
# Health Check Endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"}), 200
    
# Shorten a URL
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL in request"}), 40
    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate a unique short code
    short_code = generate_short_code()
    while url_mapping.get_original_url(short_code) is not None:
        short_code = generate_short_code()
    url_mapping.add_url(short_code, original_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

# Redirect to original URL
@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    original_url = url_mapping.get_original_url(short_code)
    if original_url:
        url_mapping.increment_click_count(short_code)
        return redirect(original_url, code=302)
    return jsonify({"error": "URL not found"}), 404

# Get analytics for a short code
@app.route('/api/stats/<short_code>', methods=['GET'])
def get_click_count(short_code):
    original_url = url_mapping.get_original_url(short_code)
    if original_url:
        count = url_mapping.get_click_count(short_code)
        created_at = url_mapping.get_creation_time(short_code)
        return jsonify({
            "url": original_url,
            "clicks": count,
            "created_at": created_at.isoformat() if created_at else None
        }), 200
    return jsonify({"error": "URL not found"}), 404

# Entry point for running directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
