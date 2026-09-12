import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Configuration
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app_telegram = Application.builder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("🚀 Bienvenue sur VPN IA DRCONGO ! Posez vos questions ou demandez des configurations.")

async def admin(update: Update, context):
    await update.message.reply_text("👤 Admin : Salomon (+243 961 923 572)")

async def handle_ai(update: Update, context):
    user_text = update.message.text
    system_prompt = "Tu es l'IA de VPN IA DRCONGO, expert en VPN (nPv Tunnel, HTTP Injector) et réseaux en RDC. Réponds de façon claire et courtoise."
    response = model.generate_content(f"{system_prompt}\n\nUtilisateur: {user_text}")
    await update.message.reply_text(response.text)

app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("admin", admin))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update_data = json.loads(post_data.decode('utf-8'))

        asyncio.run(self.process_update(update_data))

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

    async def process_update(self, update_data):
        await app_telegram.initialize()
        update = Update.de_json(update_data, app_telegram.bot)
        await app_telegram.process_update(update)
      
