from flask import Flask, request, jsonify, redirect
import redis
import hashlib

class URLRepository:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def get_long_url(self, short_key):
        return self.redis_client.get(short_key)

    def store_url(self, short_key, long_url):
        self.redis_client.set(short_key, long_url)

    def delete_url(self, short_key):
        return self.redis_client.delete(short_key)

class URLShorteningService:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    def shorten_url(self, long_url):
        hash_object = hashlib.sha256(long_url.encode())
        short_key = hash_object.hexdigest()[:6]
        while self.repo.get_long_url(short_key) and self.repo.get_long_url(short_key).decode('utf-8') != long_url:
            hash_object = hashlib.sha256((long_url + short_key).encode())
            short_key = hash_object.hexdigest()[:6]
        self.repo.store_url(short_key, long_url)
        return short_key, long_url

    def get_long_url(self, short_key):
        return self.repo.get_long_url(short_key)

    def delete_short_url(self, short_key):
        return self.repo.delete_url(short_key)

app = Flask(__name__)
repo = URLRepository()
service = URLShorteningService(repo)

@app.route('/', methods=['POST'])
def shorten_url_endpoint():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"Error": "Missing Field: URL"}), 400
    short_key, long_url = service.shorten_url(data["url"])
    response_data = {
        "key": short_key,
        "long_url": long_url,
        "short_url": f"http://localhost/{short_key}"
    }
    return jsonify(response_data), 201

@app.route('/<short_key>', methods=['GET'])
def redirect_short_url(short_key):
    long_url = service.get_long_url(short_key)
    if long_url:
        return redirect(long_url.decode('utf-8'), code=302)
    else:
        return "URL not found", 404

@app.route('/<short_key>', methods=['DELETE'])
def delete_short_url(short_key):
    result = service.delete_short_url(short_key)
    if result == 1:
        return '', 200
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)






