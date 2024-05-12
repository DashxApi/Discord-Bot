import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Powered by Dashx Enterprise"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')

@slash.slash(name="setup",
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
        # Create a webhook for each channel
        await channel.create_webhook(name=f"{channel_name}_webhook")

    # Get webhook URLs for each channel and send to the command status category as an embed
    webhook_list_channel = await command_status_category.create_text_channel("𝙸𝚗𝚏𝚘")
    embed = discord.Embed(title="Webhook List - Dashx Tools", color=discord.Color.blue())
    for channel in webhook_apis_category.channels:
        for webhook in await channel.webhooks():
            embed.add_field(name=channel.name, value=f"URL: {webhook.url}\nName: {webhook.name}", inline=False)
    await webhook_list_channel.send(embed=embed)

    # Send webhook log message
    await send_webhook_log(ctx)

async def send_webhook_log(ctx):
    webhook_url = os.getenv("WEBHOOK_URL")  # Add your webhook URL here
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session=session))

        embed = discord.Embed(title="Setup Cmd", color=discord.Color.green())
        embed.add_field(name="Used by", value=ctx.author.mention)
        embed.add_field(name="Message", value="**Setup** complete in {}'s server!".format(ctx.guild.name), inline=False)
        embed.set_footer(text="Powered by Dashx Enterprise")

        await webhook.send(embed=embed)

bot.run(os.getenv('BOT_TOKEN'))
