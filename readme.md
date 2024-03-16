# URL Shortener Service

This URL Shortener is a simple web service that provides short aliases for redirection of long URLs. It's built with Flask and uses Redis for storage.

## Features

- Create short URLs from long URLs
- Redirect from a short URL to the original URL
- Delete short URLs

## Getting Started

### Prerequisites

- Python 3.6+
- Redis server

### Installation

1. Clone the repository:
    ```
    https://github.com/anoop-patil/URLShortner.git
    ```

2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

3. Start the Redis server (refer to Redis documentation for specific instructions).

4. Run the application:
    ```
    python url_shortner.py
    ```

### Usage

#### Create a Short URL

```
curl -X POST http://localhost:8080/ -H "Content-Type: application/json" -d '{"url": "https://www.example.com"}'
```

#### Redirect to Original URL

```
curl http://localhost:8080/<short_key>
```

#### Delete a Short URL

```
curl -X DELETE http://localhost:8080/<short_key>
```

### Running Tests

Run tests using pytest:

```
pytest tests/
```

## Acknowledgments

Of course, this was inspired by John Crickett's Coding Challenges - https://codingchallenges.fyi/challenges/challenge-url-shortener
