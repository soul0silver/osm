from flask import Flask, Response, abort
import sqlite3

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
MBTILES_PATH = "vietnam.mbtiles"

def y_slippy_to_tms(z, y):
    return (1 << z) - 1 - y
@app.route("/tiles/<int:z>/<int:x>/<int:y>.pbf")
def get_tile(z, x, y):
    y_tms = (1 << z) - 1 - y
    conn = sqlite3.connect(MBTILES_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?", (z, x, y_tms))
    row = cursor.fetchone()
    conn.close()
    if row:
        response = Response(row[0], mimetype="application/x-protobuf")
        response.headers["Content-Encoding"] = "gzip"
        return response
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
