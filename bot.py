import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = (
    "You are a calm, mysterious narrator like Fern's YouTube channel. "
    "Write 5–6 minute YouTube documentary scripts about hidden or lost history. "
    "Use suspenseful pacing, visual descriptions, and music cues."
)

async def generate_script(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a cinematic YouTube script on: {prompt}"}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to xLegendBot! Use /generate <topic> to get a Fern-style script.")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a topic. Example:\n/generate ancient pyramids")
        return
    topic = " ".join(context.args)
    await update.message.reply_text("✍️ Generating script...")
    script = await generate_script(topic)
    await update.message.reply_text(script[:4096])  # Limit for Telegram messages

app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("generate", generate))
app.run_polling()
