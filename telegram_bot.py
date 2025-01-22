import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from transformers import pipeline

BOT_TOKEN = "7498921311:AAHq0pyVCLgL1Sw15ryDoF2JydlKV0PnhLM"

# Initialize your LLM 
# using Hugging Face Transformers
try:
    llm = pipeline('text-generation', model='TinyLlama/TinyLlama-1.1B-Chat-v1.0', device=0)
except Exception as e:
    print(f"Error loading LLM: {e}")
    llm = None


async def start(update, context):
    await update.message.reply_text("Hello! I'm your AI assistant.")


async def echo(update, context):
    user_message = update.message.text
    if llm:
        try:
            prompt = f"{user_message}\nAssistant:"
            response = llm(prompt, max_length=200, truncation=True, num_return_sequences=1)[0]['generated_text']
            print(f"LLM Response: {response}")
            await update.message.reply_text(response)
        except Exception as e:
            print(f"Error during LLM inference: {e}")
            await update.message.reply_text("Sorry, I encountered an error processing your request.")
    else:
        await update.message.reply_text("LLM not available.")


def main():
    # Use Application instead of Updater
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
