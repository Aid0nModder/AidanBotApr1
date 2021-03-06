import discord
from discord.ext import commands
from discord.utils import find

from functions import getComEmbed

class AllCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def intro(self, ctx):
        emb = getComEmbed(None, self.client, "The New Face Of AidanBot!", f"Hello world!.. AidanBot is no more.", f"I'm {self.client.name}, after being taken down i decided trying to make another bot was too hard, so i hacked AidanBot and am using him instead, so welcome to the Aidan's Bot's family! run -help for help\n\n- Aidan and AliTheKing")
        await ctx.send(embed=emb)
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, message):
        await ctx.send(message)
        await ctx.message.delete()

    @commands.command()
    async def help(self, ctx):
        emb = getComEmbed(ctx, self.client, "help", "Aidan's Bots Help Menu", "A list of all Aidan's Bots Commands", fields=[
            ["๐ Fun Commands ๐", "Coming Soon!"],
            ["๐จ Moderation Commands๐จ", "Coming Soon!"],
            ["๐ฐ Economy Commands ๐ฐ", "Coming Soon!"],
            ["๐ผ๏ธ Image Manipulation Commands ๐ผ๏ธ", "Coming Soon!"]
        ])
        await ctx.send(embed=emb)

def setup(client):
	client.add_cog(AllCog(client))