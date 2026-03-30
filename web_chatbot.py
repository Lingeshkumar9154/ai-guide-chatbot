from flask import Flask, render_template, request
import requests

conversation_history = []

app = Flask(__name__)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": "Bearer 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",  # 🔥 un API key inga podu
    "Content-Type": "application/json"
}

def chatbot_reply(user):
    try:
        conversation_history.append({
            "role": "user",
            "content": user
        })

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a friendly AI assistant. Reply in English or Tanglish. Keep answers short and simple."
                }
            ] + conversation_history
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        reply = result['choices'][0]['message']['content']

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:
        return "Error da macha 😅: " + str(e)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form["message"]
        reply = chatbot_reply(user)
        return reply

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
