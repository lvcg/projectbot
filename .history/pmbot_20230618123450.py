import discord
from discord.ext import commands
from github import Github
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv

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

bot.run('YOUR_BOT_TOKEN')
