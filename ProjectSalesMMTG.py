from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pandas as pd
from datetime import datetime

TOKEN = "7030080230:AAGL4Z2X_92vjurQyMjGZPnlmC-kwJkRFr8"
EXCEL_PATH = r"C:\Users\Modern 14\Desktop\ProjectTelegrammForMM.xlsx"


async def handle_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    try:
        df = pd.read_excel(EXCEL_PATH)


        df['Регион_clean'] = df['Регион'].astype(str).str.strip().str.lower()
        region_name = update.message.text.strip().title()
        region_df = df[df['Регион_clean'] == user_input]

        if region_df.empty:
            await update.message.reply_text(f"❌ Данных по региону '{update.message.text}' не найдено.")
        else:
            message = f"📊 *Продажи по {region_name} на Сегодня  :*\n\n"

            for _, row in region_df.iterrows():

                if isinstance(row['Дата'], datetime):
                    date_str = row['Дата'].strftime('%Y-%m-%d')
                else:
                    try:
                        parsed_date = pd.to_datetime(row['Дата'])
                        date_str = parsed_date.strftime('%Y-%m-%d')
                    except:
                        date_str = "—"

                message += (
                    f"📅 Дата: {date_str}\n\n"
                    f"👤 Менеджер: {row['Маркет-менеджер']}\n"
                    f"💰 Продажи: ${row['Продажи']:,}\n"
                    f"📈 Percentage of sales from yesterday to today: {round(row['Процент продаж'] * 100, 1)}%\n"
                    f"✅ Статус: {row['Статус']}\n"
                )
            await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка при чтении или обработке файла.")
        print("Ошибка:", e)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_region_request))

print("✅ Бот запущен.")
app.run_polling()
