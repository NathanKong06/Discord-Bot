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

    reply = f"**Name:** {name}\n"
    if country_used:
        reply += f"**Country Applied:** {country_used}\n"
    reply += (
        f"**Gender:** {gender_value.capitalize()}\n"
        f"**Probability:** {round(probability * 100)}%\n"
        f"**Based on:** {count} sample(s)"
    )
    await interaction.response.send_message(reply)

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

    reply = f"**Name:** {name}\n"
    if country_used:
        reply += f"**Country Applied:** {country_used}\n"
    reply += f"**Predicted Age:** {age_value}\n**Based on:** {count} sample(s)"
    await interaction.response.send_message(reply)

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

    formatted = "\n".join(
        f"**{c['country_id']}** — {round(c['probability'] * 100)}%"
        for c in countries[:5]
    )

    await interaction.response.send_message(
        f"**Name:** {name}\n{formatted}"
    )

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

    reply = f"**Name:** {name}\n**Country Applied:** {country if country else 'Global'}\n"

    # Gender
    if gender_value:
        reply += f"**Gender:** {gender_value.capitalize()} " \
                 f"(Probability: {round(probability * 100)}%, " \
                 f"Based on {gender_count} sample(s))\n"
    else:
        reply += "**Gender:** Unknown\n"

    # Age
    if age_value:
        reply += f"**Predicted Age:** {age_value} (Based on {age_count} sample(s))\n"
    else:
        reply += "**Predicted Age:** Unknown\n"

    # Nationality
    if countries:
        formatted_countries = ", ".join(f"{c['country_id']} ({round(c['probability'] * 100)}%)" for c in countries[:5])
        reply += f"**Predicted Nationalities (Top 5):** {formatted_countries}"
    else:
        reply += "**Predicted Nationalities:** Unknown"

    await interaction.response.send_message(reply)

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
    
    await interaction.response.send_message(f"Cat Fact: {fact}")

client.run(TOKEN)