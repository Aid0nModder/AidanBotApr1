import discord
from discord import Embed, Color

import datetime, math, asyncio

# EMBED STUFF #
def getEmbed(title, desc, col, fields, timestamp=True, inline=False):
	emb = Embed(title=title, description=desc, color=col)
	if timestamp:
		emb.timestamp = datetime.datetime.utcnow()
	for f in fields:
		inline = inline
		emb.add_field(name=f[0], value=f[1], inline=inline)
	return emb

def getComEmbed(ctx=None, client=None, command="N/A", title=Embed.Empty, desc=Embed.Empty, col=Color.from_rgb(52, 235, 202), fields=[], inline=False):
	emb = getEmbed(title=title, desc=desc, col=col, fields=fields, inline=inline)
	if ctx:
		if isinstance(ctx.channel, discord.channel.DMChannel):
			emb.set_footer(text=f"Requested by {ctx.author} in a private DM")
		else:
			emb.set_footer(text=f"Requested by {ctx.author} in #{ctx.channel}")
	emb.set_author(name=f"{client.name} > {command}", icon_url=client.pfp)
	return emb
def getComEmbedSimple(title=Embed.Empty, desc=Embed.Empty, color=Color.from_rgb(52, 235, 202)):
	emb = getEmbed(title=title, desc=desc, col=color, fields=[], timestamp=False)
	return emb

async def ClientError(ctx, client, error): # not used for now
    await ctx.send(embed=getComEmbed(ctx, client, "Client Error", f"Looks like something's wrong with {client.name}'s client. Please try again. If you're having trouble figuring out what it is, see error.", f"```{error}```", Color.from_rgb(220, 29, 37)))
async def ComError(ctx, client, error):
    await ctx.send(embed=getComEmbed(ctx, client, "Error", f"{client.name} has ran into an error. Please try your command again. See error for more info. Contact the bot owner if this error can't be fixed in any way whatsoever that you tried.", f"```{error}```", Color.from_rgb(220, 29, 37)))
async def ExistError(ctx, client):
    await ctx.send(embed=getComEmbed(ctx, client, "Error", "This command doesn't seem to exist, make sure you typed it right.", "", Color.from_rgb(220, 29, 37)))
async def ParamError(ctx, client, error):
    await ctx.send(embed=getComEmbed(ctx, client, "Parameter Error", f"{client.name} has encountered an error and your command was cancelled. See error for more info. This error occurred because either a missing parameter or argument was detected: ", f"Missing required argument for {client.getprefix(client, ctx.message)}{ctx.command}: **{error.param}**\n```{client.getprefix(client, ctx.message)}{ctx.command} {ctx.command.signature}```", Color.from_rgb(145, 29, 37)))
async def CooldownError(ctx, client, error):
	await ctx.send(embed=getComEmbed(ctx, client, "Cooldown Error", "Command on cooldown!! ```Try again in {:.2f} seconds.```".format(error.retry_after), "", Color.from_rgb(145, 29, 37)))

async def SendDM(client, title, description):
	aidan = await client.fetch_user(384439774972215296)
	emb = getComEmbed(None, client, "System Message", title, description, Color.from_rgb(70, 29, 37))
	await aidan.send(embed=emb)

# INTERACTIONS #

async def areyousure(client, ctx, txt):
	MSG = await ctx.send(txt, view=discord.ui.View(
		discord.ui.Button(label="Yes", style=discord.ButtonStyle.green, custom_id="accept"), discord.ui.Button(label="No", style=discord.ButtonStyle.red, custom_id="deny")
	))
	def check(interaction):
		return (interaction.user.id == client.owner_id and interaction.message.id == MSG.id and (interaction.data["custom_id"] == "accept" or interaction.data["custom_id"] == "deny"))
	try:
		interaction = await client.wait_for("interaction", timeout=10, check=check)
		await MSG.delete()
		if interaction.data["custom_id"] == "deny":
			return False
		else:
			return True
	except asyncio.TimeoutError:
		await MSG.delete()
		return False

async def userPostedRecently(channel, user, limit):
	async for msg in channel.history(limit=limit):
		if msg.author == user:
			return True
	return False

# OTHER #

def getIntFromText(txt):
	theNEWlist = "1234567890abcdefghijklmnopqrstuvwxyz .,:;/-+ `"
	sed = ""
	for letter in txt:
		if letter == "$" or letter == "%":
			sed += "46"
		else:
			ind = theNEWlist.find(letter)
			if ind:
				sed += str(ind+1)
			else:
				sed += "47"
	return int(sed)

# generats a bar using emotes
def getBar(value, maxvalue, size, hashalf=False):
	valueperseg = maxvalue / size
	segsfilled = math.ceil(value / valueperseg)
	ishalf = False
	if hashalf and math.ceil((value - (valueperseg/2)) / valueperseg) < segsfilled:
		ishalf = True

	barmotes = {
		"left": {"full":"<:left_full:862331445526921287>", "half":"<:left_half:862331445700067328>", "fulls":"<:left_fullsingle:862331445750005770>", "empty":"<:left_empty:862331445720121365>"},
		"mid": {"full":"<:middle_full:862331445300428821>", "half":"<:middle_half:862331445845688340>", "fulls":"<:middle_fullsingle:862331445703737364>", "empty":"<:middle_empty:862331445813313606>"},
		"right": {"full":"<:right_full:862331445657468939>", "half":"<:right_half:862331445702819880>", "fulls":"<:right_full:862331445657468939>", "empty":"<:right_empty:862331445313273857>"}
	}
	
	bar = ""
	for i in range(1, size+1):
		place = "right"
		if i == 1:
			place = "left"
		elif i < size:
			place = "mid"

		if i < segsfilled:
			bar += barmotes[place]["full"]
		elif i == segsfilled:
			if ishalf:
				bar += barmotes[place]["half"]
			else:
				bar += barmotes[place]["fulls"]
		else:
			bar += barmotes[place]["empty"]
	return bar

# Example: ["s40", "m5", "h20", "d1"] returns time + (1 day, 20 hours, 5 minutes, 40 seconds)
def argsToTime(args):
	timelist = { "s":0, "m":0, "h":0, "d":0 }
	timetxt = []
	for arg in args:
		time = 0
		try:
			time = int(arg[1:len(arg)])
		except:
			print(f"COULD NOT CONVERT '{arg}' TO INT.")
			return

		if arg[0] in timelist:
			timelist[arg[0]] = time
		
	def timestep(let, single, multiple):
		if timelist[let]:
			append = f"1 {single}" if timelist[let] == 1 else f"{timelist[let]} {multiple}"
			timetxt.append(append)

	timestep("d", "day", "days")
	timestep("h", "hour", "hours")
	timestep("m", "minute", "minutes")
	timestep("s", "second", "seconds")

	timetxt = ",".join(timetxt)
	return timelist, timetxt

def dateToStr(day, month):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	m, d = months[month-1], day
	if day == 1 or day == 21 or day == 31:
		d = f"{d}st"
	elif day == 2 or day == 22:
		d = f"{d}nd"
	elif day == 3 or day == 23:
		d = f"{d}rd"
	else:
		d = f"{d}th"
	return d + " of " + m