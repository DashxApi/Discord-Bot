import os
import discord
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await client.change_presence(activity=discord.Game(name="Powered by Dashx Enterprise"))

@client.event
async def on_message(message):
    if message.author == client.user:
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

    # Get webhook URLs for each channel and send to the command status category
    webhook_list_channel = await command_status_category.create_text_channel("𝙸𝚗𝚏𝚘")
    message_content = "Webhook List - Dashx Tools\n"
    for channel in webhook_apis_category.channels:
        for webhook in await channel.webhooks():
            message_content += f"**{channel.name}**\n{webhook.url}\n{webhook.name}\n\n"

    await webhook_list_channel.send(message_content)

client.run(os.getenv('BOT_TOKEN'))
