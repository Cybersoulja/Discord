import discord
import logging
import os
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    logger.error('BOT_TOKEN not set in .env file!')
    raise ValueError('BOT_TOKEN is required. Please set it in your .env file.')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Handler called when bot successfully logs in"""
    logger.info(f'Logged in as {bot.user}')
    logger.info(f'Bot is in {len(bot.guilds)} guild(s)')


@bot.event
async def on_message(message):
    """Handler called when bot receives a message"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    logger.info(f'Message from {message.author} in {message.guild}/{message.channel}: {message.content}')

    # Process commands
    await bot.process_commands(message)


@bot.command(name='hello')
async def hello(ctx):
    """Simple hello command"""
    logger.info(f'Hello command invoked by {ctx.author}')
    await ctx.send(f'Hello, {ctx.author.name}! 👋')


@bot.command(name='ping')
async def ping(ctx):
    """Ping command to check bot latency"""
    latency = bot.latency * 1000  # Convert to milliseconds
    logger.info(f'Ping command invoked by {ctx.author}')
    await ctx.send(f'Pong! 🏓 Latency: {latency:.2f}ms')


@bot.command(name='help_custom')
async def help_custom(ctx):
    """Display available commands"""
    logger.info(f'Help command invoked by {ctx.author}')

    embed = discord.Embed(
        title='Available Commands',
        description='Here are the commands I can respond to:',
        color=discord.Color.blue()
    )
    embed.add_field(name='!hello', value='Say hello to the bot', inline=False)
    embed.add_field(name='!ping', value='Check bot latency', inline=False)
    embed.add_field(name='!help_custom', value='Show this help message', inline=False)

    await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
    """Handler called when a member joins the server"""
    logger.info(f'{member} joined {member.guild}')

    # Optional: Send a welcome message to the first text channel
    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages:
            await channel.send(f'Welcome to the server, {member.mention}! 👋')
            break


@bot.event
async def on_member_remove(member):
    """Handler called when a member leaves the server"""
    logger.info(f'{member} left {member.guild}')


@bot.event
async def on_reaction_add(reaction, user):
    """Handler called when a reaction is added to a message"""
    if user == bot.user:
        return

    logger.info(f'{user} reacted with {reaction.emoji} to message in {reaction.message.channel}')


@bot.event
async def on_reaction_remove(reaction, user):
    """Handler called when a reaction is removed from a message"""
    if user == bot.user:
        return

    logger.info(f'{user} removed {reaction.emoji} reaction from message in {reaction.message.channel}')


@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands"""
    if isinstance(error, commands.CommandNotFound):
        logger.warning(f'Unknown command from {ctx.author}: {ctx.message.content}')
        await ctx.send(f'Unknown command. Use `!help_custom` for available commands.')
    elif isinstance(error, commands.MissingRequiredArgument):
        logger.warning(f'Missing arguments from {ctx.author}: {ctx.message.content}')
        await ctx.send(f'Missing required arguments. Use `!help_custom` for more info.')
    else:
        logger.error(f'Command error from {ctx.author}: {error}')
        await ctx.send(f'An error occurred while processing the command. Please try again.')


def main():
    """Main entry point"""
    try:
        logger.info('Starting Discord bot...')
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.error(f'Failed to start bot: {e}')
        raise


if __name__ == '__main__':
    main()
