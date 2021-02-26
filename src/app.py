from flask import Flask, request, jsonify
from services.pghelper import (
    create_tables
)


app = Flask(__name__)

@app.route('/v1',  methods = ["GET"])
def main():
    return {"status": "success", "message": "dataeng_test Q2"}

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", debug=True)