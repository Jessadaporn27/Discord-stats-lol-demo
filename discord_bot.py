import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


TOKEN = "MTMwMjIzNjA3NjUyMTQyNzAxNA.GbAuVs.2K31eS0gsXSTSFQk-LiMZpycS8rlea_cogUsy8"

# สร้าง Intents และเปิดใช้งานค่าเริ่มต้น
intents = discord.Intents.default()
intents.message_content = True  # เปิดใช้งานการเข้าถึงเนื้อหาข้อความ

# สร้างบอทและระบุ prefix พร้อมทั้ง intents
bot = commands.Bot(command_prefix="!", intents=intents)

# ฟังก์ชันเพื่อดึงข้อมูลสถิติของผู้เล่น
@bot.command()
async def stats(ctx, summoner_name: str):
    await ctx.send("กำลังดึงข้อมูล กรุณารอสักครู่...")
    stats = get_player_stats(summoner_name)
    await ctx.send(stats)

# ฟังก์ชันสำหรับการดึงข้อมูลสถิติ
def get_player_stats(summoner_name):
    url = f"https://www.op.gg/summoners/th/{summoner_name}"
    try:
        response = requests.get(url)

        if response.status_code == 404:
            return f"Summoner '{summoner_name}' not found."

        if response.status_code != 200:
            return f"Failed to retrieve data from the server. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Debug: Print the initial part of the HTML content
        print(soup.prettify()[:10000])  # Print the first 1000 characters of the HTML

        # Get Stat box
        statbox = soup.find("div", class_="stats-box stats-box--TOTAL css-1egz98l eci27mx0")
        if not statbox:
            return "Stat box not found. Please check the console for HTML structure."

        # Get Win-Lose data
        win_lose_element = statbox.find("div", class_="win-lose")
        win_lose = win_lose_element.text.strip() if win_lose_element else "Win-Lose data not found"

        # Get KDA data
        kda = statbox.find("div", class_="ratio").text if statbox.find("div", class_="ratio") else "KDA data not found"

        return (
            f"Summoner: {summoner_name}\n"
            f"Rank Win-Lose: {win_lose}\n"
            f"KDA: {kda}"
        )

    except requests.RequestException as e:
        return f"An error occurred: {e}"





# รันบอท
bot.run(TOKEN)
