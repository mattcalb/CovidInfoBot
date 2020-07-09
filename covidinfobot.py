import discord
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

client = discord.Client() # create our client

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready") # when the bot is ready to work
    game = discord.Game("!info help")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command()
async def info(ctx, *, countryname):

    countryname = countryname.lower()

    if countryname == "help":
        embed=discord.Embed(title="Help", description="type !info name of the country", color=0xff0000)
        await ctx.send(embed=embed)

    if countryname != "help":
        
        countryname = countryname.replace(" ","-")

        if countryname == "usa" or countryname == "united-states" or countryname == "united-states-of-america" or countryname == "america":
            countryname = "us" # there's a lot of ways to say USA xD

        if countryname == "united-kingdom":
            countryname = "uk" # there's another way to say uk
            
        result = requests.get("https://www.worldometers.info/coronavirus/country/" + countryname) # put the countryname into the link

        if result.status_code != 200:
            embed=discord.Embed(title="Something went wrong!", description="try again!", color=0xff0000)
            await ctx.send(embed=embed)

        src = result.content # storing the page's content

        soup = BeautifulSoup(src, "lxml") # parse and process the source

        # if the name of the country is invalid
        invalid = soup.find(text="Not Found")
        if invalid == "Not Found" and countryname != "help":
            embed=discord.Embed(title="Invalid Country!", description="type a correct country's name!", color=0xff0000)
            await ctx.send(embed=embed)

        else:

            # finding the numbers
            numbers = soup.find_all("div", class_="maincounter-number")

            cases = numbers[0].get_text()
            deaths = numbers[1].get_text()
            recovered = numbers[2].get_text()

            cases = cases.replace("\n","")
            deaths = deaths.replace("\n","")
            recovered = recovered.replace("\n","")

            embed=discord.Embed(title=f"{countryname}", color=0xff0000)
            embed.add_field(name="Cases", value=f"{cases}", inline=False)
            embed.add_field(name="Deaths", value=f"{deaths}", inline=False)
            embed.add_field(name="Recovered", value=f"{recovered}", inline=True)
            embed.set_footer(text="all data is extracted from https://www.worldometers.info/coronavirus/")
            await ctx.send(embed=embed)
   

client.run("INSERT BOT TOKEN HERE") # run the bot