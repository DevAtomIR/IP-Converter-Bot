import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = 13415480
api_hash = "7a6c59032649b4e9177af0e4f675da03"
bot_token = "5784869466:AAE3itNp1VvSoPe71M80b3Zp7TyLmaqeLyA"

app = Client("bot", api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Please enter an IPv4 or IPv6 address :")

@app.on_message()
async def message(_, message):
    ip = message.text

    if ":" in ip:  # IPv6
        url = f"https://www.whatsmydns.net/ipv6-to-ipv4?q={ip}"
    else:  # IPv4
        url = f"https://www.whatsmydns.net/ipv4-to-ipv6?q={ip}"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    result_div = soup.find("div", class_="mb-8 p-4 border-t border-gray-100 shadow-lg rounded")

    if result_div:
        result_p = result_div.find_all("p")
        if len(result_p) >= 2:
            result_code = result_p[1].find("code")
            result = result_code.get_text()

            if ":" in ip:  # IPv6
                await message.reply_text(f"IPv4 ⇾ `{result}`")
            else:  # IPv4
                modified_ipv6 = '::ffff:' + result.split(':', 1)[-1]
                modified_ipv6 = modified_ipv6[:-2]
                await message.reply_text(f"IPv6 ⇾ `{modified_ipv6}`")

        else:
            await message.reply_text("Error : Invalid IPv4 Address")

app.run()
