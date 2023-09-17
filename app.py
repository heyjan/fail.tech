from flask import Flask, request, jsonify, abort, send_from_directory
import asyncio
from collections import deque
import threading
import sqlite3

# Flask and SQLite Setup
app = Flask(__name__, static_folder='static')


def query_db(query, args=(), one=False):
    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/search', methods=['GET'])
def search():
    queryAddress = request.args.get('address')
    queryTwitter = request.args.get('twitter')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    if queryAddress and queryTwitter:
        results = query_db("SELECT * FROM data WHERE address LIKE ? AND twitterUsername LIKE ? LIMIT ? OFFSET ?",
                           ('%' + queryAddress + '%', '%' + queryTwitter + '%', per_page, offset))
    elif queryAddress:
        results = query_db("SELECT * FROM data WHERE address LIKE ? LIMIT ? OFFSET ?",
                           ('%' + queryAddress + '%', per_page, offset))
    elif queryTwitter:
        results = query_db("SELECT * FROM data WHERE twitterUsername LIKE ? LIMIT ? OFFSET ?",
                           ('%' + queryTwitter + '%', per_page, offset))
    else:
        return jsonify([])  # Return empty list if no queries are provided

    keys = ['id', 'address', 'twitterUsername', 'twitterName', 'twitterPfpUrl', 'twitterUserId', 'lastOnline']
    results_dict = [dict(zip(keys, result)) for result in results]

    return jsonify(results_dict)

# Create a queue to hold messages that we want to send to Discord
message_queue = deque()

@app.route('/', methods=['POST'])
def webhook_listener(client):
    content_type = request.headers.get('Content-Type')
    if not content_type or 'application/json' not in content_type:
        abort(415)  # Unsupported Media Type
    webhook_token = request.headers.get('Arkham-Webhook-Token')

    valid_tokens = {'Kep9w4rCgMx09o', 'Token2', 'Token3'}  # Add your valid tokens to this set
    if webhook_token not in valid_tokens:
        abort(403)  # Forbidden, incorrect token

    data = request.json
    print(data)

    # Append data to our queue
    message_queue.append(data)
    print(f"Current Queue: {message_queue}")  # Debug print

    return jsonify({"message": "Received and forwarded"}), 200

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0')
