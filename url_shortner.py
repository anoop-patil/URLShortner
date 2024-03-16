from flask import Flask, request, jsonify, redirect, abort
import redis
import hashlib

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"Error": "Missing Field: URL"}), 400

    long_url = data["url"]

    hash_object = hashlib.sha256(long_url.encode())
    short_key = hash_object.hexdigest()[:6]

    # Check for collisions and adjust as necessary (basic example, can be expanded)
    while redis_client.get(short_key) and redis_client.get(short_key).decode('utf-8') != long_url:
        # This is a simplistic approach; in a real scenario, you'd want to add a counter or random data
        hash_object = hashlib.sha256((long_url + short_key).encode())
        short_key = hash_object.hexdigest()[:6]

    redis_client.set(short_key, long_url)

    response_data = {
        "key": short_key,
        "long_url": long_url,
        "short:url": f"http://localhost/{short_key}"
    }

    return jsonify(response_data), 201


@app.route('/<short_key>', methods=['GET'])
def redirect_short_url(short_key):
    long_url = redis_client.get(short_key)
    if long_url:
        return redirect(long_url.decode('utf-8'), code=302)
    else:
        return "URL not found", 404


@app.route('/<short_key>', methods=['DELETE'])
def delete_short_url(short_key):
    result = redis_client.delete(short_key)
    if result == 1:
        return '', 200
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)
