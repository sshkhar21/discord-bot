import discord
from discord.ext import commands
import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Updated role names with correct tags
alliance_tags = {
    "🏰MOB": "[MOB]",
    "🏰MOS": "[MOS]",
    "🏰KAT": "[KAT]",
    "🏰TAN": "[TAN]",
    "🏰SHH": "[SHH]"
}

@bot.event
async def on_ready():
    logger.info(f"Bot is ready. Logged in as {bot.user}")
    
    # Log that we are starting to check for name changes
    logger.info("Checking for name changes due to role assignments...")

    for member in bot.guilds[0].members:  # Assuming the bot is in one guild
        # Get the member's current roles
        member_roles = [role.name for role in member.roles]
        
        # Check if the member has any role that matches alliance tags
        for role in member_roles:
            if role in alliance_tags:
                tag = alliance_tags[role]
                current_nick = member.nick if member.nick else member.name
                
                # If the nickname doesn't already start with the tag, update it
                if not current_nick.startswith(tag):
                    new_nick = f"{tag} {member.name}"
                    try:
                        await member.edit(nick=new_nick)
                        logger.info(f"Nickname updated to {new_nick} for {member.name}")
                    except discord.Forbidden:
                        logger.warning(f"Missing permission to change nickname for {member.name}.")
                    except Exception as e:
                        logger.error(f"Error updating nickname for {member.name}: {e}")

@bot.event
async def on_member_update(before, after):
    # Check if the roles have changed
    if before.roles != after.roles:
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]

        if added_roles:
            logger.info(f"Added roles: {[r.name for r in added_roles]}")
        if removed_roles:
            logger.info(f"Removed roles: {[r.name for r in removed_roles]}")

        # Handle added roles
        for role in added_roles:
            if role.name in alliance_tags:
                tag = alliance_tags[role.name]
                current_nick = after.nick if after.nick else after.name
                
                if not current_nick.startswith(tag):
                    new_nick = f"{tag} {after.name}"
                    try:
                        await after.edit(nick=new_nick)
                        logger.info(f"Nickname updated to {new_nick} for {after.name}")
                    except discord.Forbidden:
                        logger.warning(f"Missing permission to change nickname for {after.name}.")
                    except Exception as e:
                        logger.error(f"Error updating nickname for {after.name}: {e}")

        # Handle removed roles
        for role in removed_roles:
            if role.name in alliance_tags:
                tag = alliance_tags[role.name]
                current_nick = after.nick if after.nick else after.name
                
                if current_nick.startswith(tag):
                    new_nick = after.name  # Remove the tag if the role is removed
                    try:
                        await after.edit(nick=new_nick)
                        logger.info(f"Nickname updated to {new_nick} for {after.name}")
                    except discord.Forbidden:
                        logger.warning(f"Missing permission to change nickname for {after.name}.")
                    except Exception as e:
                        logger.error(f"Error updating nickname for {after.name}: {e}")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Trigger keywords
    trigger_keywords = ["snor", "snorlax", "snorlax2lazy"]
    message_content = message.content.lower()

    if any(keyword in message_content for keyword in trigger_keywords):
        embed = discord.Embed(
            title="He who must not be named has been called upon...",
            description="What do you want? :knife:",
            color=discord.Color.red()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/930870348545679370/1371854515611107379/snorlax-crawling.gif?ex=6824a694&is=68235514&hm=4713a1003ca2ae635e3d25ede88b4327bd6f6eeadb75d794044201be6489a1e6&=&width=623&height=468")
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))
