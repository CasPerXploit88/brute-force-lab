from flask import Flask, render_template, request, jsonify
from core.cracker import smart_crack, log_result

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crack", methods=["POST"])
def crack():
    data = request.get_json()
    password = data.get("password", "").strip()

    if not password:
        return jsonify({"error": "No password provided"}), 400

    if len(password) > 8:
        return jsonify({"error": "Keep password under 8 characters for simulation"}), 400

    result = smart_crack(password)
    log_result(password, result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)