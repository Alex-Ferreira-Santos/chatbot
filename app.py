from time import sleep
from flask import Flask,render_template, request, Response
from flask_cors import CORS, cross_origin
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))
modelo = "llama3-8b-8192"

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = 'Content-Type'
app.secret_key = 'alura'

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce. 
            Você não deve responder perguntas que não sejam dados do e-commerce informado!
            """
            response = cliente.chat.completions.create(
                messages=[
                        {
                            "role": "system",
                            "content": prompt_do_sistema
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model = modelo)
            return response
        except Exception as erro:
                repeticao += 1
                if repeticao >= maximo_tentativas:
                        return "Erro no GPT: %s" % erro
                print('Erro de comunicação com OpenAI:', erro)
                sleep(1)


@app.route("/chat", methods=["POST"])
@cross_origin()
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
