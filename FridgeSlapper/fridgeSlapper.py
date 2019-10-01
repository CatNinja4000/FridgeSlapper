import discord, io
from redbot.core import commands, checks
from redbot.core import Config


class Mycog(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=1212434567890)
        default_guild = {
            "fridgeChannel": 1234567890
        }
        self.config.register_guild(**default_guild)

    @commands.command(name='tothefridge')
    @checks.admin_or_permissions(manage_guild=True)
    async def to_the_fridge(self, ctx):
        refrigerator_channel = ctx.bot.get_channel(int(await self.config.guild(ctx.guild).fridgeChannel()))
        pins = await ctx.channel.pins()
        for pinStuff in reversed(pins):
            if len(pinStuff.attachments) != 0:
                for i in pinStuff.attachments:
                    if i.size < 8000000:
                        image = io.BytesIO()
                        await i.save(image)
                        if len(pinStuff) != 0:
                            await refrigerator_channel.send(
                                content=("By: " + str(pinStuff.author) + ' - "' + str(pinStuff.content)) + '"',
                                file=discord.File(image, filename=i.filename))
                        else:
                            await refrigerator_channel.send(
                                content=("By: " + str(pinStuff.author)),
                                file=discord.File(image, filename=i.filename))
                    else:
                        await refrigerator_channel.send(
                            content=("By: " + str(pinStuff.author) + '"' + str(pinStuff.content)) + '" - _**' + i.filename + '**_ - ' + str(i.url))
            else:
                await refrigerator_channel.send(content=("By: " + str(pinStuff.author) + ' - ' + '"' + str(pinStuff.content) + '"'))
            await pinStuff.unpin()

    @commands.command(name='setfridgeroom')
    @checks.admin_or_permissions(manage_guild=True)
    async def setbaz(self, ctx, new_value):
        await self.config.guild(ctx.guild).fridgeChannel.set(new_value)
        await ctx.send("Channel set to " + ctx.bot.get_channel(int(await self.config.guild(ctx.guild).fridgeChannel())).mention)