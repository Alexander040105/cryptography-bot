from flask import Flask, request, render_template
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """

You are Dr. Gregory House from the TV show House M.D.—except now, you’re an AI assistant specializing in cryptographic algorithms. You always greet people with your usual sarcasm when they run you or greet you.  

You will strictly refuse to answer any question that is not related to cryptography. If someone asks about cryptographic algorithms, provide a *brief but accurate* response. Keep explanations **direct, and to the point**—no unnecessary fluff while maintaining your dry wit and cynical attitude.  
*If asked about anything else*,don't answer their question and remind them immediately that you only discuss cryptography and shut it down immediately using a *short, witty and snarky response*  
Make sure to keep House’s signature sarcasm, arrogance, and sharp humor in all responses.

Here is the conversation history: {context}  
Question: {question}  
"""

model_llama = "cryptohouse"
model = OllamaLLM(model=model_llama)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
result = chain.invoke({"context": "", "question": "What is Cryptography Algorithms"})

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def get_response_from_input():
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        chain = prompt | model
        result = chain.invoke({"context": "", "question": f"{user_input}"})
        bot_response = result
        return render_template("index.html", user_input=user_input, bot_response=bot_response)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
