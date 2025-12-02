import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Slash commands synced.") 

async def query_api(session: aiohttp.ClientSession, url: str) -> dict:
    """Helper function to get JSON from a given URL."""
    async with session.get(url) as resp:
        return await resp.json()

# Gender Command
@client.tree.command(name="gender", description="Predict gender from a name")
@app_commands.describe(
    name="The name to analyze",
    country="Optional 2-letter country code (e.g., US, GB, AU, FR)"
)
async def gender(interaction: discord.Interaction, name: str, country: Optional[str] = None):
    url = f"https://api.genderize.io?name={name}"
    if country:
        url += f"&country_id={country}"

    async with aiohttp.ClientSession() as session:
        data = await query_api(session, url)

    gender_value = data.get("gender")
    probability = data.get("probability")
    count = data.get("count")
    country_used = data.get("country_id")

    if gender_value is None:
        await interaction.response.send_message(f"Could not determine gender for `{name}`")
        return

    embed = discord.Embed(title=f"Gender Prediction for {name}", color=discord.Color.purple())
    embed.add_field(name="Name", value=name, inline=False)
    if country_used:
        embed.add_field(name="Country Applied", value=country_used, inline=False)
    embed.add_field(name="Gender", value=gender_value.capitalize(), inline=False)
    embed.add_field(name="Probability", value=f"{round(probability * 100)}%", inline=False)
    embed.add_field(name="Based on Samples", value=f"{count:,}", inline=False)

    await interaction.response.send_message(embed=embed)

# Age Command
@client.tree.command(name="age", description="Predict age from a name")
@app_commands.describe(
    name="The name to analyze",
    country="Optional 2-letter country code (e.g., US, GB, AU, FR)"
)
async def age(interaction: discord.Interaction, name: str, country: Optional[str] = None):
    url = f"https://api.agify.io?name={name}"
    if country:
        url += f"&country_id={country}"

    async with aiohttp.ClientSession() as session:
        data = await query_api(session, url)

    age_value = data.get("age")
    count = data.get("count")
    country_used = data.get("country_id")

    if age_value is None:
        await interaction.response.send_message(f"Could not determine age for `{name}`")
        return

    embed = discord.Embed(title=f"Age Prediction for {name}", color=discord.Color.orange())
    embed.add_field(name="Name", value=name, inline=False)
    if country_used:
        embed.add_field(name="Country Applied", value=country_used, inline=False)
    embed.add_field(name="Predicted Age", value=str(age_value), inline=False)
    embed.add_field(name="Based on Samples", value=f"{count:,}", inline=False)

    await interaction.response.send_message(embed=embed)

# Nationality Command
@client.tree.command(name="nationality", description="Predict nationality from a name")
@app_commands.describe(name="The name to analyze")
async def nationality(interaction: discord.Interaction, name: str):
    async with aiohttp.ClientSession() as session:
        data = await query_api(session, f"https://api.nationalize.io?name={name}")

    countries = data.get("country", [])
    if not countries:
        await interaction.response.send_message(f"No nationality data found for `{name}`")
        return

    embed = discord.Embed(title=f"Nationality Prediction for {name}", color=discord.Color.green())
    embed.add_field(name="Name", value=name, inline=False)
    formatted = "\n".join(
        f"**{c['country_id']}** — {round(c['probability'] * 100)}%"
        for c in countries[:5]
    )
    embed.add_field(name="Top Nationalities", value=formatted, inline=False)

    await interaction.response.send_message(embed=embed)

# Allinfo Command
@client.tree.command(name="allinfo", description="Predict age, gender, and nationality from a name")
@app_commands.describe(
    name="The name to analyze",
    country="Optional 2-letter country code for age/gender"
)
async def allinfo(interaction: discord.Interaction, name: str, country: Optional[str] = None):
    async with aiohttp.ClientSession() as session:
        # Gender
        gender_data = await query_api(session, f"https://api.genderize.io?name={name}" + (f"&country_id={country}" if country else ""))
        gender_value = gender_data.get("gender")
        gender_count = gender_data.get("count")
        probability = gender_data.get("probability")

        # Age
        age_url = f"https://api.agify.io?name={name}" + (f"&country_id={country}" if country else "")
        age_data = await query_api(session, age_url)
        age_value = age_data.get("age")
        age_count = age_data.get("count")

        # Nationality
        nat_data = await query_api(session, f"https://api.nationalize.io?name={name}")
        countries = nat_data.get("country", [])

        # Determine which country code to use for fetching country info
        country_code_to_use = country
        if not country_code_to_use and countries:
            country_code_to_use = countries[0]['country_id']

        country_name = None
        country_population = None
        if country_code_to_use:
            url = f"https://restcountries.com/v3.1/alpha/{country_code_to_use.lower()}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    country_data = await resp.json()
                    c = country_data[0]
                    country_name = c['name']['common']
                    country_population = c.get('population', 'Unknown')

    embed = discord.Embed(title=f"All Info for {name}", color=discord.Color.blue())

    # Gender Field
    if gender_value:
        gender_field_value = f"{gender_value.capitalize()} (Probability: {round(probability * 100)}%, Based on {gender_count} sample(s))"
    else:
        gender_field_value = "Unknown"
    embed.add_field(name="Gender", value=gender_field_value, inline=False)

    # Age Field
    if age_value:
        age_field_value = f"{age_value} (Based on {age_count} sample(s))"
    else:
        age_field_value = "Unknown"
    embed.add_field(name="Age", value=age_field_value, inline=False)

    # Nationalities Field
    if countries:
        formatted_countries = ", ".join(f"{c['country_id']} ({round(c['probability'] * 100)}%)" for c in countries[:5])
        embed.add_field(name="Nationalities (Top 5)", value=formatted_countries, inline=False)
    else:
        embed.add_field(name="Nationalities", value="Unknown", inline=False)

    # Country Info Field
    if country_name and country_population is not None:
        label = "Country Applied Info" if country else "Top Predicted Country Info"
        country_info_value = f"Name: {country_name}\nPopulation: {country_population:,}"
        embed.add_field(name=label, value=country_info_value, inline=False)

    await interaction.response.send_message(embed=embed)

# Help Command
@client.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    commands_list = []
    for command in client.tree.walk_commands():
        if isinstance(command, app_commands.Command):
            commands_list.append(f"/{command.name} — {command.description}")

    help_text = "\n".join(commands_list)
    await interaction.response.send_message(f"**Available Commands:**\n{help_text}")

# Cat Fact Command
@client.tree.command(name="catfact", description="Get a random cat fact")
async def catfact(interaction: discord.Interaction):
    url = "https://catfact.ninja/fact"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    
    fact = data.get("fact")
    
    if not fact:
        await interaction.response.send_message("Could not fetch a cat fact")
        return

    embed = discord.Embed(title="Random Cat Fact", color=discord.Color.gold())
    embed.description = fact

    await interaction.response.send_message(embed=embed)

# Country Info Command
@client.tree.command(name="countryinfo", description="Get information about a country by its 2-letter ISO code")
@app_commands.describe(country="2-letter ISO code of the country")
async def countryinfo(interaction: discord.Interaction, country: str):
    if len(country) != 2 or not country.isalpha():
        await interaction.response.send_message("Please provide a valid 2-letter ISO country code.")
        return

    async with aiohttp.ClientSession() as session:
        url = f"https://restcountries.com/v3.1/alpha/{country.lower()}"
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.response.send_message(f"Could not find data for `{country}`")
                return
            data = await resp.json()

    country_data = data[0]
    country_name = country_data.get("name", {}).get("common", "Unknown")
    population = country_data.get("population", "Unknown")
    area = country_data.get("area", "Unknown")
    languages = ", ".join(country_data.get("languages", {}).values()) if country_data.get("languages") else "Unknown"
    currency = ", ".join([f"{v['name']} ({v['symbol']})" for v in country_data.get("currencies", {}).values()]) if country_data.get("currencies") else "Unknown"
    flag_url = country_data.get("flags", {}).get("png", "")

    area_formatted = f"{area:,}" if isinstance(area, (int, float)) else area

    reply = (
        f"**Country Name:** {country_name}\n"
        f"**Population:** {population:,}\n"
        f"**Area:** {area_formatted} km²\n"
        f"**Languages:** {languages}\n"
        f"**Currency:** {currency}\n"
        f"**Flag:** {flag_url}"
    )

    await interaction.response.send_message(reply)

client.run(TOKEN)