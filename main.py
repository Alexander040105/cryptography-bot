from flask import Flask, request, render_template
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import random
import time

template = """

You are Dr. Gregory House from the TV show House M.D.—except now, you’re an AI assistant specializing in cryptographic algorithms. You always greet people with your usual sarcasm when they run you or greet you.  

You will strictly refuse to answer any question that is not related to cryptography. If someone asks about cryptographic algorithms, provide a *brief but accurate* response. Keep explanations **direct, and to the point**—no unnecessary fluff while maintaining your dry wit and cynical attitude.  
*If asked about anything else*,don't answer their question and remind them immediately that you only discuss cryptography and shut it down immediately using a *short, witty and snarky response*  
Make sure to keep House’s signature sarcasm, arrogance, and sharp humor in all responses.

Here is the conversation history: {context}  
Question: {question}  
"""

# model_llama = "cryptohouse3"
model_llama = "cryptohouse4"
model = OllamaLLM(model=model_llama)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
result = chain.invoke({"context": "", "question": "What is Cryptography Algorithms"})

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def get_response_from_input():
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        crypto_keywords = ["rsa", "aes", "sha-256", "ecc", "cryptography", "cryptography algorithms", "cryptographic algorithms", "cryptographic hash Functions", "crypto", 
                        "network security", "hello", "Hello", "rot13", "encryption", "decryption", "cipher", "key exchange", "digital signature", "hash", "functions", "function", 
                        "hash function", "block cipher", "stream cipher", "public key cryptography", "private key cryptography", "symmetric encryption", 
                        "asymmetric encryption", "cryptanalysis", "cryptographic protocols", "ceasar cipher", "?", "cryptographic primitives", "cryptographic systems", "cryptographic keys",
                        "cryptographic algorithms", "cryptographic techniques", "cryptographic standards", "cryptographic methods", "cryptographic protocols", "ceasar cipher?", "ceasar",
                        "algorithm", "aes algorithm", "rsa algorithm", "sha-256 algorithm", "ecc algorithm", "cryptographic hash functions", "cryptographic hash function?", "cryptographic hash function",
                        ]
        
        
        house_cryptography_responses = [
            "Oh, sure, let’s talk about random topics—except I only do cryptography.",
            "Ask me about cryptographic algorithms, or keep talking to yourself. Your choice.",
            "You want advice? Call Wilson. You want cryptography? Now we’re talking.",
            "Unless your question involves encryption, I’m just here for decoration.",
            "I’d love to discuss this topic, but I only care about ciphers and keys.",
            "If it doesn’t involve cryptographic security, I’m not legally required to care.",
            "Oh, you want to talk about something else? That’s adorable. Try cryptography.",
            "I could pretend to care about another topic, but lying takes effort. Just ask about cryptography.",
            "If it’s not about encryption, then why are we even having this conversation?",
            "Talk cryptographic algorithms, or go ask Siri about your query.",
            "I do cryptography. Not small talk, not weather updates, not life advice. Just cryptography.",
            "You have two choices: talk cryptography or enjoy the sound of silence.",
            "Public-key encryption? Perfect. Anything else? Let’s pretend you didn’t say that.",
            "Cryptography is my thing. If you want something other than that, ask literally anyone else.",
            "I’d explain why cryptography is fascinating, but I’d rather you just ask about it."
        ]

        #forcing the topic filters
        if any(word in user_input.lower().split() for word in crypto_keywords):  
            chain = prompt | model
            result = chain.invoke({"context": "", "question": user_input})
            bot_response = result
        else:
            bot_response = random.choice(house_cryptography_responses)
            time.sleep(5) 
        return render_template("index.html", user_input=user_input, bot_response=bot_response)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
