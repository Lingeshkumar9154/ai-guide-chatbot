from flask import Flask, render_template, request
import requests

conversation_history = []
app = Flask(__name__)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
   "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

def chatbot_reply(user):
    try:
        conversation_history.append({
            "role": "user",
            "content": user
        })

        data = {
            "model": "google/gemma-3-4b-it:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a friendly AI assistant. Always reply ONLY in English or Tanglish (Tamil in English letters). Never use Hindi or other languages. Always give clear, short and structured answers. Use bullet points or steps when needed. Keep answers simple like a friend explaining. Avoid long paragraphs. Always keep answers under 5-6 lines unless asked. When giving code, always format it properly using code blocks like ```c or ```python and ensure it is complete and correct. Always provide recent or approximate latest data when asked."
                }
            ] + conversation_history
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        print("API Response:", result)

        if 'choices' not in result:
            return f"API Error: {result.get('error', {}).get('message', 'Unknown error')}"

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
        print("User message:", user)
        reply = chatbot_reply(user)
        return reply

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
