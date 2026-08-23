import os
import io
import httpx
from pypdf import PdfReader
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from google import genai

app = FastAPI()

# Variáveis de Ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
PDF_URL = os.getenv("PDF_URL")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# Clientes
gemini_client = genai.Client(api_key=GEMINI_KEY)
pdf_content_cache = ""

def load_pdf_from_github() -> str:
    global pdf_content_cache
    if not pdf_content_cache:
        response = httpx.get(PDF_URL)
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        pdf_content_cache = "\n".join([page.extract_text() or "" for page in reader.pages])
    return pdf_content_cache

def ask_gemini(question: str) -> str:
    context = load_pdf_from_github()
    prompt = f"Baseie-se estritamente no seguinte documento para responder à pergunta:\n\n{context}\n\nPergunta: {question}"
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Interface Web
@app.get("/", response_class=HTMLResponse)
async def serve_chat():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Chatbot PDF</title>
      <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        #chat { border: 1px solid #ccc; height: 350px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; border-radius: 8px; }
        .user { color: #0056b3; margin-bottom: 8px; }
        .bot { color: #28a745; margin-bottom: 8px; }
        input { width: 75%; padding: 8px; }
        button { padding: 8px 15px; }
      </style>
    </head>
    <body>
      <h2>Chatbot - Consulta de Documento</h2>
      <div id="chat"></div>
      <input type="text" id="msg" placeholder="Digite sua pergunta..." />
      <button onclick="send()">Enviar</button>
      <script>
        async function send() {
          const input = document.getElementById('msg');
          const chat = document.getElementById('chat');
          if(!input.value) return;
          chat.innerHTML += `<div class='user'><b>Você:</b> ${input.value}</div>`;
          const text = input.value;
          input.value = '';
          const res = await fetch(`/api/ask?q=${encodeURIComponent(text)}`);
          const data = await res.json();
          chat.innerHTML += `<div class='bot'><b>Bot:</b> ${data.answer}</div>`;
          chat.scrollTop = chat.scrollHeight;
        }
      </script>
    </body>
    </html>
    """

# Endpoint de consulta pública
@app.get("/api/ask")
async def api_ask(q: str):
    return {"answer": ask_gemini(q)}

# Configuração do Telegram Webhook
tg_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def start_cmd(update: Update, context):
    await update.message.reply_text("Olá! Envie uma pergunta sobre o documento.")

async def handle_tg_message(update: Update, context):
    await update.message.chat.send_action("typing")
    answer = ask_gemini(update.message.text)
    await update.message.reply_text(answer)

tg_app.add_handler(CommandHandler("start", start_cmd))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tg_message))

@app.on_event("startup")
async def on_startup():
    await tg_app.initialize()
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/telegram-webhook"
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.set_webhook(url=webhook_url)

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"status": "ok"}