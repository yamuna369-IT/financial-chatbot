from flask import Flask, render_template, request, jsonify
from chatbot import answer_question

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    response = answer_question(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)