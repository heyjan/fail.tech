from flask import Flask, jsonify, request, send_from_directory
import sqlite3

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
