import nextcord
import asyncio
from nextcord.ext import commands, tasks
import requests
import psutil
import datetime

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all(), help_command=None)

svrid = "70192"

@tasks.loop(seconds=15)
async def update_status():
    api_url = f"https://api.scplist.kr/api/servers/{svrid}"
    try:
        response = requests.get(api_url)
        data = response.json()

        player_count = data['players']
        memory_usage = str(psutil.virtual_memory().percent)
        cpu_percent = str(psutil.cpu_percent(interval=1))
        timestamp = datetime.datetime.now()

    except Exception as e:
        print(f'Error retrieving data from API: {e}')
        return

    embed = nextcord.Embed(color=nextcord.Color.blue(), timestamp=timestamp)
    embed.add_field(name="-----------", value="", inline=False)
    embed.add_field(name="プレイヤー数", value=player_count, inline=False)
    embed.add_field(name="-----------", value="", inline=False)
    embed.add_field(name="CPU使用率", value=f"{cpu_percent}%", inline=False)
    embed.add_field(name="-----------", value="", inline=False)
    embed.add_field(name="メモリ使用率", value=f"{memory_usage}%", inline=False)
    embed.add_field(name="-----------", value="", inline=False)
    embed.set_author(name="もよもよサーバー / moyomoyo Server", icon_url="https://media.discordapp.net/attachments/1132240475282231357/1196669796981420042/moyomoyo.png?ex=65b87898&is=65a60398&hm=9376470251bd9a10a059bf66ffd220eebc6c57e6e0f95a6cdbbb007d1f327068&=&format=webp&quality=lossless")
    
    channel_id = 1182316610619449394
    message_id = 1196676298764988457
    channel = bot.get_channel(channel_id)

    if channel:
        message = await channel.fetch_message(message_id)
        await message.edit(embed=embed)

@bot.event
async def on_ready():
    print("ok")
    update_status.start()

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def setupembed(interaction):
    embed = nextcord.Embed(description="このembedのメッセージidをコード内の`message_id`に貼り付けてください。")
    await interaction.channel.send(embed=embed)

bot.run('MTE5MDQ5NDcxMDM3NzIyMjIyNA.GupHJO.TyNvKoZIhW9eVBK5ouUvDkOfTvkWxixZnZao6c')