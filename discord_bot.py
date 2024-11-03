import aiohttp
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


TOKEN = "token here"

# สร้าง Intents และเปิดใช้งานค่าเริ่มต้น
intents = discord.Intents.default()
intents.message_content = True  # เปิดใช้งานการเข้าถึงเนื้อหาข้อความ

# สร้างบอทและระบุ prefix พร้อมทั้ง intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def tier(ctx, role, region = "kr"):
    await ctx.send("waiting for data...")
    try:
        champions = get_top_data(role,region)
        if champions:
            response = "\n".join([f"{idx + 1}. {champion}" for idx, champion in enumerate(champions)])
        else:
            response = "not found"
    except Exception as e:
        response = f"Error: {e}"

    await ctx.send(response)

@bot.command()
async def counter(ctx, champion, role):
    await ctx.send("waiting for data...")
    try:
        champions = get_counter_data(champion, role)
        if champions:
            response = "\n".join([f"{idx + 1}. {champion}" for idx, champion in enumerate(champions)])
        else:
            response = "not found."
    except Exception as e:
        response = f"Error: {e}"

    await ctx.send(response)

@bot.command()
async def rank(ctx, summoner_name: str):
    url = f"https://u.gg/lol/profile/th2/{summoner_name}/overview"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()

            # Corrected selector
            selector = "#content > div > div.content-side-padding.w-full.max-w-\[1016px\].mx-auto.md\:box-content > div > div > div.summoner-profile_overview.w-\[1016px\].mt-\[24px\] > div.summoner-profile_overview__side > div.rank-block > div > div:nth-child(1) > div > div.rank-sub-content > div.text-container > div.rank-text > span.rank-title"
            lp = "#content > div > div.content-side-padding.w-full.max-w-\[1016px\].mx-auto.md\:box-content > div > div > div.summoner-profile_overview.w-\[1016px\].mt-\[24px\] > div.summoner-profile_overview__side > div.rank-block > div > div:nth-child(1) > div > div.rank-sub-content > div.text-container > div.rank-text > span:nth-child(2)"
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            rank_title_elem = soup.select_one(selector)
            lp_elem = soup.select_one(lp)

            # Check if element exists
            if rank_title_elem:
                rank_title = rank_title_elem.text
                lp_title = lp_elem.text
                await ctx.send(f"{summoner_name}'s rank is: {rank_title} {lp_title}")
            else:
                await ctx.send(f"Could not find rank information for {summoner_name}")

def get_counter_data(champion, role):
    url = f"https://u.gg/lol/champions/{champion}/counter?role={role}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    for i in range(1, 11):  # วนลูปจากแถวที่ 1 ถึงแถวที่ 10
        selector = f'#content > div > div > div > div > div > div.champion-profile-page > div > div:nth-child(1) > div.counters-list.best-win-rate > a:nth-child({i}) > div.col-2 > div.champion-name'
        data_div = soup.select_one(selector)

        # ตรวจสอบว่าพบข้อมูลหรือไม่
        if data_div:
            data_list.append(data_div.text.strip())
        else:
            data_list.append("ไม่พบข้อมูล")

    return data_list

def get_top_data(role, region, rank_limit=10):
    url = f"https://www.op.gg/champions?position={role}&region={region}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # ค้นหาแถวที่อยู่ใน `tbody`
    rows = soup.select('table tbody tr')

    # เก็บข้อมูลจากแต่ละแถวที่ต้องการ
    data_list = []

    for i, row in enumerate(rows):
        if i >= rank_limit:  # หยุดเมื่อได้ข้อมูลครบตามจำนวนที่ต้องการ
            break

        data = row.select_one('td.css-1hw6gn9.ez7snl12 a strong')

        if data:
            data_list.append(data.text.strip())

    return data_list


# รันบอท
bot.run(TOKEN)
