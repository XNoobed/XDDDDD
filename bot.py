import os, asyncio
from zippy import zdl
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


bot = Client(
    "Zippy",
    api_hash="578d2817642f3aa3a283efaf49f4ef4e",
    api_id=int(12845924),
    bot_token="2026467093:AAGCKQBm-6MqqyXokaQh-qsY-ZHku2KbrHA"
)

async def progress(current, total, client, info, file):
        percent = f"Subiendo: {file.name}\nTamaño: {file.size_fmt}\n\n{current * 100 / total:.2f}%"
        await asyncio.sleep(.5)
        await info.edit(percent)

Conversation_state = {}

@bot.on_message(filters.private)
async def msg_handler(client, message: Message):
    who = message.from_user.id
    state = Conversation_state.get(who)
    # users = [957370219, 728171240, 1642684372, 1051187422, 2123007198]
    users = open("users.txt", "r").read()
    name = message.from_user.first_name
    username = f"https://t.me/{message.from_user.username}"
    
    ADDUSER = 0
    BANUSER = 1
    if message.from_user.username in users:
        if message.text == '/start':
            await message.reply(f"Hola [{name}]({username})")
        elif message.text == '/help':
            await message.reply("solo envia el link y ya xd")
        elif message.text.endswith("/file.html"):
            try:
                i = await message.reply("Descargando OwO")
                file = await zdl(message.text)
                await i.edit(f"Descargado:\n\nNombre: {file.name}\nTamaño: {file.size_fmt}\n [Link Directo]({file.download_url})\nFecha de Subida: {file.date_uploaded_fmt}", disable_web_page_preview=True)
                info = await message.reply(f"Subiendo: {file.name}\nTamaño: {file.size_fmt}")
                await message.reply_document(file.name, progress=progress, progress_args=(client, info, file))
                os.remove(file.name)
                await info.delete()
            except Exception as e:
                await i.edit("Error en el link :3")
                print(e)
        elif message.photo:
            await message.reply("Imagenes no admitidas")
        elif message.video:
            await message.reply("Videos no admitidos")
        elif message.sticker:
            await message.reply("Stickers no admitidos")
        elif message.document:
            await message.reply("Archivos no admitidas")
        if state is None and message.text == '/add':
            await message.reply("Envie el username del usuario que desea admitir sin el @")
            Conversation_state[who] = ADDUSER

            return
        if state == ADDUSER and message.text:
            del Conversation_state[who]

            open("users.txt", "a").write("\n"+message.text)
            await message.reply("Usuario admitido")

        if state is None and message.text == '/ban':
            await message.reply("Envie el username del usuario que desea banear sin el @")
            Conversation_state[who] = BANUSER

            return
        if state == BANUSER and message.text:
            del Conversation_state[who]

            with open(r"users.txt", "r") as us:
                lines = us.readlines()
            content = message.text
            with open(r"users.txt", "w") as us:
                for line in lines:
                    if line.strip("\n") != content:
                        us.write(line)
            await message.reply("Usuario baneado")
        if message.text == '/get':
            f = open("users.txt", "r").read()
            await message.reply_text(f)
    else:
        await message.reply("WTF que haces??? no estas permitido")
if __name__ == '__main__':
    print("Iniciado")
    bot.run()