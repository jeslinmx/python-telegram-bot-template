import logging
import os
import sys
import traceback

import telegram as tg
import telegram.ext as tgext
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_markdown, escape_markdown

api_token = os.getenv("TELEGRAM_API_TOKEN")
report_chat_ids = os.getenv("LOG_RECIPIENTS", "").split(",")

def some_handler(upd: tg.Update, ctx: tgext.CallbackContext):
    pass

@run_async
def report_error(upd: tg.Update, ctx: tgext.CallbackContext):
    # Attempt to notify user that a problem has been encountered.
    # This has no effect on e.g. inline queries and poll updates.
    if upd.effective_message:
        upd.effective_message.reply_text("Sorry, an unforeseen problem occurred. The developer(s) have been informed and are looking into this.")

    payload = f"`{ctx.error}` occurred"
    payload += f" with the user {mention_markdown(upd.effective_user.id, escape_markdown(upd.effective_user.first_name))}" if upd.effective_user else ""
    payload += f" within the chat _{upd.effective_chat.title}_" if upd.effective_chat else ""
    payload += f" with the poll id {upd.poll.id}" if upd.poll else ""
    payload += f".\nTraceback:```{traceback.format_exc()}```"

    for chat_id in report_chat_ids:
        if chat_id:
            ctx.bot.send_message(
                chat_id,
                parse_mode=tg.ParseMode.MARKDOWN,
                text=payload
            )
    # Uncomment if you want the error to also be logged.
    # raise ctx.error

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO,
    )

    updater = tgext.Updater(
        token=os.getenv("TELEGRAM_API_TOKEN"),
        use_context=True,
    )

    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(report_error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()