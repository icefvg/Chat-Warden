import discord
from discord.ext import commands
import asyncio
import logging
import os
import re
import json
from dotenv import load_dotenv
load_dotenv()

from config import BAD_WORD_REPLACEMENTS, WEBHOOK_CACHE_SIZE
from word_filter import WordFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('discord_bot.log')
    ]
)
logger = logging.getLogger(__name__)

class ProfanityBot(commands.Bot):
    def __init__(self):
        # Required intents for message monitoring
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description='A bot that replaces bad words with funny alternatives'
        )
        
        # Initialize word filter
        self.word_filter = WordFilter()
        
        # Webhook cache to avoid recreating webhooks
        self.webhook_cache = {}
        self.webhook_cache_size = 0
        self.max_webhook_cache = WEBHOOK_CACHE_SIZE
        
        # Load custom word lists
        self.custom_bad_words = {}
        self.whitelist = set()
        self.load_custom_lists()
        
    def load_custom_lists(self):
        """Load custom bad words and whitelist from files"""
        try:
            # Load custom bad words
            if os.path.exists('custom_bad_words.json'):
                with open('custom_bad_words.json', 'r') as f:
                    self.custom_bad_words = json.load(f)
                    self.word_filter.bad_words.update(self.custom_bad_words)
                    self.word_filter.patterns = self.word_filter._compile_patterns()
            
            # Load whitelist
            if os.path.exists('whitelist.json'):
                with open('whitelist.json', 'r') as f:
                    self.whitelist = set(json.load(f))
        except Exception as e:
            logger.warning(f"Could not load custom lists: {e}")
    
    def save_custom_lists(self):
        """Save custom bad words and whitelist to files"""
        try:
            with open('custom_bad_words.json', 'w') as f:
                json.dump(self.custom_bad_words, f, indent=2)
            
            with open('whitelist.json', 'w') as f:
                json.dump(list(self.whitelist), f, indent=2)
        except Exception as e:
            logger.error(f"Could not save custom lists: {e}")

    async def setup_hook(self):
        """Called when the bot is starting up"""
        logger.info("Bot is starting up...")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
        
    async def on_ready(self):
        """Called when the bot has successfully connected to Discord"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is monitoring {len(self.guilds)} guilds')
        
        # Log guild information
        for guild in self.guilds:
            logger.info(f'Connected to guild: {guild.name} (ID: {guild.id})')
    
    async def get_or_create_webhook(self, channel):
        """Get existing webhook or create a new one for the channel"""
        try:
            # Check cache first
            cache_key = f"{channel.guild.id}_{channel.id}"
            if cache_key in self.webhook_cache:
                webhook = self.webhook_cache[cache_key]
                try:
                    # Test if webhook is still valid
                    await webhook.fetch()
                    return webhook
                except discord.NotFound:
                    # Webhook was deleted, remove from cache
                    del self.webhook_cache[cache_key]
                    self.webhook_cache_size -= 1
            
            # Try to find existing webhook
            webhooks = await channel.webhooks()
            bot_webhook = None
            
            for webhook in webhooks:
                if webhook.user == self.user:
                    bot_webhook = webhook
                    break
            
            # Create new webhook if none exists
            if not bot_webhook:
                bot_webhook = await channel.create_webhook(
                    name=f"{self.user.name} Filter",
                    reason="Profanity filter webhook"
                )
                logger.info(f"Created new webhook for channel {channel.name}")
            
            # Add to cache (with size limit)
            if self.webhook_cache_size >= self.max_webhook_cache:
                # Remove oldest entry
                oldest_key = next(iter(self.webhook_cache))
                del self.webhook_cache[oldest_key]
                self.webhook_cache_size -= 1
            
            self.webhook_cache[cache_key] = bot_webhook
            self.webhook_cache_size += 1
            
            return bot_webhook
            
        except discord.Forbidden:
            logger.error(f"No permission to create webhook in {channel.name}")
            return None
        except Exception as e:
            logger.error(f"Error creating webhook for {channel.name}: {e}")
            return None
    
    async def on_message(self, message):
        """Monitor all messages for profanity"""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Ignore DMs
        if not message.guild:
            return
        
        # Check if user is whitelisted
        if message.author.id in self.whitelist:
            return
        
        # Check if message contains bad words
        filtered_content, has_bad_words = self.word_filter.filter_message(message.content)
        
        if has_bad_words:
            try:
                # Log the detection
                logger.info(f"Bad word detected in message from {message.author} in {message.channel.name}")
                
                # Delete the original message
                await message.delete()
                logger.info(f"Deleted message from {message.author}")
                
                # Get or create webhook for the channel
                webhook = await self.get_or_create_webhook(message.channel)
                
                if webhook:
                    # Get user's avatar URL
                    avatar_url = message.author.display_avatar.url
                    
                    # Send the filtered message via webhook
                    await webhook.send(
                        content=filtered_content,
                        username=message.author.display_name,
                        avatar_url=avatar_url,
                        allowed_mentions=discord.AllowedMentions.none()
                    )
                    
                    logger.info(f"Sent filtered message via webhook for {message.author}")
                else:
                    # Fallback: send a regular message if webhook creation fails
                    embed = discord.Embed(
                        description=f"🧼 **{message.author.display_name}**: {filtered_content}",
                        color=discord.Color.blue()
                    )
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    await message.channel.send(embed=embed, delete_after=None)
                    logger.info(f"Sent filtered message as embed for {message.author}")
                    
            except discord.Forbidden:
                logger.error(f"No permission to delete message in {message.channel.name}")
            except discord.NotFound:
                logger.warning(f"Message was already deleted in {message.channel.name}")
            except Exception as e:
                logger.error(f"Error processing message in {message.channel.name}: {e}")
        
        # Process commands (if any)
        await self.process_commands(message)
    
    async def on_message_delete(self, message):
        """Handle message deletion events"""
        if not message.author.bot:
            logger.debug(f"Message deleted from {message.author} in {message.channel.name}")
    
    async def on_error(self, event, *args, **kwargs):
        """Handle general bot errors"""
        logger.error(f"An error occurred in event {event}: {args}, {kwargs}")
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        else:
            logger.error(f"Command error in {ctx.command}: {error}")
            await ctx.send("❌ An error occurred while executing the command.")

# Create bot instance
bot = ProfanityBot()

@bot.command(name='status')
@commands.has_permissions(manage_messages=True)
async def status(ctx):
    """Check bot status and statistics"""
    embed = discord.Embed(
        title="🤖 Profanity Filter Bot Status",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="📊 Statistics",
        value=f"Guilds: {len(bot.guilds)}\nCached Webhooks: {bot.webhook_cache_size}",
        inline=True
    )
    
    embed.add_field(
        name="🔧 Word Filter",
        value=f"Bad Words: {len(bot.word_filter.bad_words)}\nPatterns: {len(bot.word_filter.patterns)}",
        inline=True
    )
    
    embed.add_field(
        name="🚀 Performance",
        value=f"Latency: {round(bot.latency * 1000)}ms",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='test_filter')
@commands.has_permissions(manage_messages=True)
async def test_filter(ctx, *, text=None):
    """Test the word filter on provided text"""
    if not text:
        await ctx.send("❌ Please provide text to test. Example: `!test_filter hello fuck world`")
        return
        
    filtered_text, has_bad_words = bot.word_filter.filter_message(text)
    
    embed = discord.Embed(
        title="🧪 Filter Test Results",
        color=discord.Color.blue() if has_bad_words else discord.Color.green()
    )
    
    embed.add_field(
        name="Original Text",
        value=f"```{text}```",
        inline=False
    )
    
    embed.add_field(
        name="Filtered Text",
        value=f"```{filtered_text}```",
        inline=False
    )
    
    embed.add_field(
        name="Contains Bad Words",
        value="✅ Yes" if has_bad_words else "❌ No",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='clear_webhook_cache')
@commands.has_permissions(administrator=True)
async def clear_webhook_cache(ctx):
    """Clear the webhook cache"""
    bot.webhook_cache.clear()
    bot.webhook_cache_size = 0
    await ctx.send("✅ Webhook cache cleared successfully!")

# Slash Commands
@bot.tree.command(name="status", description="Check bot status and statistics")
async def slash_status(interaction: discord.Interaction):
    """Slash command version of status"""
    # Check if user has manage messages permission in the guild
    if not interaction.guild or not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You need 'Manage Messages' permission to use this command.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🤖 Profanity Filter Bot Status",
        description="Real-time statistics and performance metrics",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="📊 Server Statistics",
        value=f"```\nGuilds: {len(bot.guilds)}\nCached Webhooks: {bot.webhook_cache_size}\nWhitelisted Users: {len(bot.whitelist)}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔧 Word Filter",
        value=f"```\nDefault Words: {len(BAD_WORD_REPLACEMENTS)}\nCustom Words: {len(bot.custom_bad_words)}\nTotal Patterns: {len(bot.word_filter.patterns)}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🚀 Performance",
        value=f"```\nLatency: {round(bot.latency * 1000)}ms\nUptime: Online\nStatus: Active\n```",
        inline=True
    )
    
    if bot.user:
        embed.set_footer(text=f"Bot ID: {bot.user.id}", icon_url=bot.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="test_filter", description="Test the word filter on provided text")
async def slash_test_filter(interaction: discord.Interaction, text: str):
    """Slash command to test word filtering"""
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in servers.", ephemeral=True)
        return
    
    member = interaction.guild.get_member(interaction.user.id)
    if not member or not member.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You need 'Manage Messages' permission to use this command.", ephemeral=True)
        return
    
    filtered_text, has_bad_words = bot.word_filter.filter_message(text)
    
    embed = discord.Embed(
        title="🧪 Filter Test Results",
        color=discord.Color.red() if has_bad_words else discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="📝 Original Text",
        value=f"```{text}```",
        inline=False
    )
    
    embed.add_field(
        name="🧼 Filtered Text", 
        value=f"```{filtered_text}```",
        inline=False
    )
    
    embed.add_field(
        name="🔍 Detection Result",
        value="🚨 Profanity Detected" if has_bad_words else "✅ Clean Text",
        inline=True
    )
    
    embed.add_field(
        name="⚡ Processing",
        value="Instant" if len(text) < 100 else "Fast",
        inline=True
    )
    
    embed.set_footer(text=f"Tested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="add_bad_word", description="Add a custom bad word with replacement")
async def slash_add_bad_word(interaction: discord.Interaction, bad_word: str, replacement: str):
    """Add a custom bad word to the filter"""
    
    await interaction.response.defer(thinking=True)
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permission to use this command.", ephemeral=True)
        return
    
    bad_word = bad_word.lower().strip()
    replacement = replacement.strip()
    
    if len(bad_word) < 2:
        await interaction.response.send_message("❌ Bad word must be at least 2 characters long.", ephemeral=True)
        return
    
    bot.custom_bad_words[bad_word] = replacement
    bot.word_filter.bad_words[bad_word] = replacement
    bot.word_filter.patterns = bot.word_filter._compile_patterns()
    bot.save_custom_lists()
    
    embed = discord.Embed(
        title="✅ Bad Word Added",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="🚫 Bad Word",
        value=f"`{bad_word}`",
        inline=True
    )
    
    embed.add_field(
        name="🔄 Replacement",
        value=f"`{replacement}`",
        inline=True
    )
    
    embed.add_field(
        name="📊 Total Custom Words",
        value=str(len(bot.custom_bad_words)),
        inline=True
    )
    
    embed.set_footer(text=f"Added by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="remove_bad_word", description="Remove a custom bad word from the filter")
async def slash_remove_bad_word(interaction: discord.Interaction, bad_word: str):
    """Remove a custom bad word from the filter"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permission to use this command.", ephemeral=True)
        return
    
    bad_word = bad_word.lower().strip()
    
    if bad_word not in bot.custom_bad_words:
        await interaction.response.send_message(f"❌ `{bad_word}` is not in the custom bad words list.", ephemeral=True)
        return
    
    replacement = bot.custom_bad_words.pop(bad_word)
    bot.word_filter.bad_words.pop(bad_word, None)
    bot.word_filter.patterns = bot.word_filter._compile_patterns()
    bot.save_custom_lists()
    
    embed = discord.Embed(
        title="✅ Bad Word Removed",
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="🗑️ Removed Word",
        value=f"`{bad_word}` → `{replacement}`",
        inline=False
    )
    
    embed.add_field(
        name="📊 Remaining Custom Words",
        value=str(len(bot.custom_bad_words)),
        inline=True
    )
    
    embed.set_footer(text=f"Removed by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list_custom_words", description="List all custom bad words")
async def slash_list_custom_words(interaction: discord.Interaction):
    """List all custom bad words"""
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You need 'Manage Messages' permission to use this command.", ephemeral=True)
        return
    
    if not bot.custom_bad_words:
        embed = discord.Embed(
            title="📝 Custom Bad Words",
            description="No custom bad words have been added yet.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📝 Custom Bad Words",
        description=f"Total: {len(bot.custom_bad_words)} custom words",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    words_list = []
    for i, (word, replacement) in enumerate(list(bot.custom_bad_words.items())[:20], 1):
        words_list.append(f"{i}. `{word}` → `{replacement}`")
    
    if len(bot.custom_bad_words) > 20:
        words_list.append(f"... and {len(bot.custom_bad_words) - 20} more")
    
    embed.add_field(
        name="🚫 Custom Words & Replacements",
        value="\n".join(words_list) if words_list else "None",
        inline=False
    )
    
    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="whitelist_add", description="Add a user to the whitelist (they won't be filtered)")
async def slash_whitelist_add(interaction: discord.Interaction, user: discord.User):
    """Add a user to the whitelist"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permission to use this command.", ephemeral=True)
        return
    
    if user.id in bot.whitelist:
        await interaction.response.send_message(f"❌ {user.mention} is already whitelisted.", ephemeral=True)
        return
    
    bot.whitelist.add(user.id)
    bot.save_custom_lists()
    
    embed = discord.Embed(
        title="✅ User Whitelisted",
        description=f"{user.mention} has been added to the whitelist.",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="👤 User",
        value=f"{user.display_name} ({user.id})",
        inline=True
    )
    
    embed.add_field(
        name="📊 Total Whitelisted",
        value=str(len(bot.whitelist)),
        inline=True
    )
    
    embed.set_footer(text=f"Added by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="whitelist_remove", description="Remove a user from the whitelist")
async def slash_whitelist_remove(interaction: discord.Interaction, user: discord.User):
    """Remove a user from the whitelist"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permission to use this command.", ephemeral=True)
        return
    
    if user.id not in bot.whitelist:
        await interaction.response.send_message(f"❌ {user.mention} is not whitelisted.", ephemeral=True)
        return
    
    bot.whitelist.remove(user.id)
    bot.save_custom_lists()
    
    embed = discord.Embed(
        title="✅ User Removed from Whitelist",
        description=f"{user.mention} has been removed from the whitelist.",
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="👤 User",
        value=f"{user.display_name} ({user.id})",
        inline=True
    )
    
    embed.add_field(
        name="📊 Remaining Whitelisted",
        value=str(len(bot.whitelist)),
        inline=True
    )
    
    embed.set_footer(text=f"Removed by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="whitelist_list", description="List all whitelisted users")
async def slash_whitelist_list(interaction: discord.Interaction):
    """List all whitelisted users"""
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You need 'Manage Messages' permission to use this command.", ephemeral=True)
        return
    
    if not bot.whitelist:
        embed = discord.Embed(
            title="👥 Whitelisted Users",
            description="No users are currently whitelisted.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="👥 Whitelisted Users",
        description=f"Total: {len(bot.whitelist)} whitelisted users",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    users_list = []
    for i, user_id in enumerate(list(bot.whitelist)[:20], 1):
        try:
            user = bot.get_user(user_id)
            if user:
                users_list.append(f"{i}. {user.mention} ({user.display_name})")
            else:
                users_list.append(f"{i}. Unknown User ({user_id})")
        except:
            users_list.append(f"{i}. User ID: {user_id}")
    
    if len(bot.whitelist) > 20:
        users_list.append(f"... and {len(bot.whitelist) - 20} more")
    
    embed.add_field(
        name="🤍 Whitelisted Users",
        value="\n".join(users_list) if users_list else "None",
        inline=False
    )
    
    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

def main():
    """Main function to run the bot"""
    # Get Discord token from environment variable
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable is not set!")
        print("Error: Please set the DISCORD_BOT_TOKEN environment variable.")
        return
    
    try:
        # Run the bot
        bot.run(token, log_handler=None)  # We handle logging ourselves
    except discord.LoginFailure:
        logger.error("Invalid Discord bot token provided!")
        print("Error: Invalid Discord bot token. Please check your DISCORD_BOT_TOKEN.")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error starting bot: {e}")

# Helper function to check permissions
def check_permissions(interaction: discord.Interaction, permission_level: str) -> tuple[bool, str]:
    """Check if user has required permissions"""
    if not interaction.guild:
        return False, "❌ This command can only be used in servers."
    
    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        return False, "❌ Could not find your server membership."
    
    if permission_level == "manage_messages":
        if not member.guild_permissions.manage_messages:
            return False, "❌ You need 'Manage Messages' permission to use this command."
    elif permission_level == "administrator":
        if not member.guild_permissions.administrator:
            return False, "❌ You need Administrator permission to use this command."
    
    return True, ""

@bot.tree.command(name="help", description="Show all available commands and bot information")
async def slash_help(interaction: discord.Interaction):
    """Show comprehensive help and command list"""
    embed = discord.Embed(
        title="🤖 Profanity Filter Bot - Help & Commands",
        description="Advanced Discord bot that filters profanity in real-time with smart detection and funny replacements.",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow()
    )
    
    # Basic commands for everyone
    embed.add_field(
        name="📊 Information Commands",
        value="```\n/help - Show this help message\n```",
        inline=False
    )
    
    # Commands for manage messages permission
    embed.add_field(
        name="🛠️ Moderator Commands (Manage Messages)",
        value="```\n/status - View bot statistics\n/test_filter <text> - Test filtering\n/list_custom_words - View custom words\n/whitelist_list - View whitelisted users\n```",
        inline=False
    )
    
    # Commands for administrators
    embed.add_field(
        name="⚡ Admin Commands (Administrator)",
        value="```\n/add_bad_word <word> <replacement>\n/remove_bad_word <word>\n/whitelist_add <user>\n/whitelist_remove <user>\n```",
        inline=False
    )
    
    # Features overview
    embed.add_field(
        name="🔥 Key Features",
        value="• **Multi-Language**: English + Hindi, Punjabi, Bengali, Tamil, Telugu\n• **Smart Detection**: Handles f*ck, f.u.c.k, madarch0d, etc.\n• **Webhook System**: Maintains user identity\n• **Custom Words**: Add your own bad words\n• **Whitelist**: Exempt trusted users\n• **Real-time**: Instant message filtering",
        inline=False
    )
    
    # Usage examples
    embed.add_field(
        name="💡 Example Usage",
        value="• Type `fuck` → Bot replaces with `fluff`\n• Type `madarchod` → Bot replaces with `buddy`\n• Use `/add_bad_word noob silly` to add custom filter\n• Use `/whitelist_add @User` to exempt someone",
        inline=False
    )
    
    # Statistics
    embed.add_field(
        name="📈 Current Stats",
        value=f"• **Servers**: {len(bot.guilds)}\n• **Default Words**: {len(BAD_WORD_REPLACEMENTS)}\n• **Custom Words**: {len(bot.custom_bad_words)}\n• **Whitelisted Users**: {len(bot.whitelist)}",
        inline=True
    )
    
    # Performance info
    embed.add_field(
        name="⚡ Performance",
        value=f"• **Latency**: {round(bot.latency * 1000)}ms\n• **Detection Patterns**: {sum(len(patterns) for patterns in bot.word_filter.patterns.values())}\n• **Cache Size**: {bot.webhook_cache_size}",
        inline=True
    )
    
    embed.set_footer(
        text="Made with ❤️ | Use /status for detailed information", 
        icon_url=bot.user.display_avatar.url if bot.user else None
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    main()
