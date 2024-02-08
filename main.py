import nextcord
import yaml
import cooldowns
import psutil
import requests
import datetime
from nextcord.ext import commands, tasks
from deep_translator import GoogleTranslator

with open("config.yaml", "r", encoding="utf-8", errors="ignore") as config_file:
	config = yaml.safe_load(config_file)

	TOKEN = config.get("BOTTOKEN")
	role = config.get("ROLEID")
	deepl_api_key = config.get("DEEPLAPI")
	target_channel_id = config.get("CHANNELID")
	channel_id = config.get("CHANNELID2")
	message_id = config.get("MESSAGEID")
	svrid = config.get("SVRID")

if TOKEN == None:
	print('\033[31m' + "ERROR: config.ymlに BOTTOKEN の値が存在しません" + '\033[0m')

bot = commands.Bot(help_command=None, intents=nextcord.Intents.all())

@bot.event
async def on_ready():
	print('----------------------------------------')
	print(f'ログインしました')
	print(f'Name  : {bot.user.name} | {bot.user.id}')
	print(f'Token : ' + '\033[32m' + f'{TOKEN}''\033[0m')
	print('----------------------------------------')
	update_status.start()

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
	channel = bot.get_channel(channel_id)

	if channel:
		message = await channel.fetch_message(message_id)
		await message.edit(embed=embed)
	await bot.change_presence(activity=nextcord.Game(name=player_count))

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def setupembed(interaction):
    embed = nextcord.Embed(description="このembedのメッセージidをconfig.yamlの`MESSAGEID: ""`に貼り付けてください。")
    await interaction.channel.send(embed=embed)

@bot.slash_command(description="募集をします。")
@cooldowns.cooldown(1, 3600, bucket=cooldowns.SlashBucket.guild)
async def 募集(interaction, title: str = nextcord.SlashOption(name="タイトル", description="embedのタイトル"), text: str = nextcord.SlashOption(name="内容", description="募集する時に使用する文章", required=True)):
	embed = nextcord.Embed(title=f"{title}", description=f"{text}")
	embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
	await interaction.response.send_message(f"<@&{role}>", embed=embed)

@bot.event
async def on_message(message):
	if message.channel.id != target_channel_id:
		return
	translated_message = GoogleTranslator(source='auto', target='ja').translate(message.content)
	embed = nextcord.Embed(description=f"{translated_message}", color=nextcord.Colour.green())
	await message.channel.send(embed=embed)

try:
	bot.run(TOKEN)
except nextcord.LoginFailure:
	print('\033[31m' + "ERROR: ログインできませんでした。tokenが正しいか確認してください。" + '\033[0m')
