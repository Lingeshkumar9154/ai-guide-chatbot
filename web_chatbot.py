from flask import Flask, render_template, request
from groq import Groq

conversation_history = []
app = Flask(__name__)

client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

def chatbot_reply(user):
    try:
        conversation_history.append({
            "role": "user",
            "content": user
        })

        messages = [
            {
                "role": "system",
                "content": "You are a friendly AI assistant. Always reply ONLY in English or Tanglish (Tamil in English letters). Never use Hindi. Give clear, short and structured answers. Use bullet points when needed. Keep answers under 5-6 lines unless asked."
            }
        ] + conversation_history

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        reply = response.choices[0].message.content

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
