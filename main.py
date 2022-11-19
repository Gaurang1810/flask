from flask import Flask, jsonify,render_template,url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))