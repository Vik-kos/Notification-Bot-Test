from discord.ext import commands, tasks
from discord.commands import slash_command
import discord
import os
import logging
from datetime import datetime

from cogs.helperfunctions.img_handler import prepare_deal_imgs

class Notification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reset = None
        self.last_notification = None
        self.channel = None

    
    #@commands.Cog.listener()
    @slash_command()
    async def start_deals(self, ctx):
        #print(ctx)
        self.channel = await self.bot.fetch_channel(ctx.channel_id)
        self.showdeal.start()

    #@slash_command()
    @tasks.loop(minutes=1)
    async def showdeal(self):
        #print(f"self.reset : {self.reset}")
        if self.reset is not None and self.reset > datetime.now():
            return

        if self.last_notification is not None:
            message = await self.channel.fetch_message(self.last_notification.id)
            await message.delete()
            self.last_notification = None

        self.reset = await prepare_deal_imgs()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        embed = discord.Embed(
            title="Deal Information"
        )
        deal_end_time = discord.utils.format_dt(self.reset, "R")

        file = discord.File(os.path.join(current_directory, "helperfunctions/images/deals.png"))
        embed.set_image(url="attachment://deals.png")
        embed.add_field(name="Deal ends: ", value=deal_end_time)

        self.last_notification = await self.channel.send(file=file, embed=embed)
        

def setup(bot):
    bot.add_cog(Notification(bot))