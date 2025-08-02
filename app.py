from flask import Flask, request, jsonify
app = Flask(__name__)

class URLShortener:
    def __init__(self):
        self.url_map = {}
        self.counter = 0

    def shorten_url(self, original_url):
        self.counter += 1
        short_url = f"http://short.url/{self.counter}"
        self.url_map[short_url] = original_url
        return short_url
    
    def get_original_url(self, short_url):
        return self.url_map.get(short_url, "URL not found")
    
    def get_all_urls(self):
        return self.url_map
    
    def expiry_of_url(self, short_url):
        if short_url in self.url_map:
            return f"Short URL {short_url} expires in 30 minutes."
        return "Short URL not found."
    
    def delete_url(self, short_url):
        if short_url in self.url_map:
            del self.url_map[short_url]
            return "Short URL deleted successfully."
        return "Short URL not found."
    
url_shortener = URLShortener()

@app.route('/')
def home():
    return "Welcome to the URL Shortener API!"

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    original_url = data.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    short_url = url_shortener.shorten_url(original_url)
    return jsonify({"short_url": short_url}), 201

@app.route('/expand', methods=['GET'])
def expand():
    short_url = request.args.get('url')
    if not short_url:
        return jsonify({"error": "Short URL is required"}), 400
    original_url = url_shortener.get_original_url(short_url)
    return jsonify({"original_url": original_url}), 200

@app.route('/urls', methods=['GET'])
def list_urls():
    urls = url_shortener.get_all_urls()
    return jsonify(urls), 200

@app.route('/expiry', methods=['GET'])
def expiry():
    short_url = request.args.get('url')
    if not short_url:
        return jsonify({"error": "Short URL is required"}), 400
    expiry_message = url_shortener.expiry_of_url(short_url)
    return jsonify({"expiry_message": expiry_message}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    short_url = request.args.get('url')
    if not short_url:
        return jsonify({"error": "Short URL is required"}), 400
    result = url_shortener.delete_url(short_url)
    return jsonify({"message": result}), 200

# ✅ Corrected this line
if __name__ == '__main__':
    app.run(debug=True)
