import discord
from discord.ext import commands
from github import Github
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv
from transformers import AlbertTokenizer, AlbertForSequenceClassification

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

# GitHub Configuration
github_token = 'YOUR_GITHUB_TOKEN'
github_organization = 'YOUR_GITHUB_ORGANIZATION'
github_repo = 'YOUR_GITHUB_REPO'
github = Github(github_token)

# Azure DevOps Configuration
azure_organization = 'YOUR_AZURE_ORGANIZATION'
azure_project = 'YOUR_AZURE_PROJECT'
azure_token = 'YOUR_AZURE_PERSONAL_ACCESS_TOKEN'
credentials = BasicAuthentication('', azure_token)
azure_connection = Connection(base_url='https://dev.azure.com/' + azure_organization, creds=credentials)

# ALBERT Configuration
albert_model_name = 'albert-base-v2'
albert_tokenizer = AlbertTokenizer.from_pretrained(albert_model_name)
albert_model = AlbertForSequenceClassification.from_pretrained(albert_model_name)

# ... Define more GitHub and Azure project management commands ...
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="User Information", color=member.color)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="User ID", value=member.id)
    embed.add_field(name="Join Date", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="Server Name", value=server.name)
    embed.add_field(name="Region", value=server.region)
    embed.add_field(name="Owner", value=server.owner.name)
    embed.add_field(name="Member Count", value=server.member_count)
    await ctx.send(embed=embed)



@bot.command()
async def create_github_issue(ctx, title, body):
    repo = github.get_repo(f'{github_organization}/{github_repo}')
    issue = repo.create_issue(title=title, body=body)
    await ctx.send(f'GitHub Issue created successfully.\nTitle: {issue.title}\nURL: {issue.html_url}')

@bot.command()
async def create_azure_work_item(ctx, title, description):
    core_client = azure_connection.clients.get_core_client()
    new_work_item = {
        'op': 'add',
        'path': '/fields/System.Title',
        'value': title
    }
    work_item = core_client.create_work_item(document=[new_work_item], project=azure_project, type='Task')
    await ctx.send(f'Azure Work Item created successfully.\nID: {work_item.id}\nURL: {work_item._links.web.href}')
    


# ... Define more GitHub and Azure project management commands ...

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Connected to Discord!')
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hello there!")

    await bot.process_commands(message)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please check the command and try again.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Please provide all necessary arguments.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")


bot.run('YOUR_BOT_TOKEN')
