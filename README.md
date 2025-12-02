# Discord Bot

A Discord bot that predicts gender, age, and nationality based on a given name using external APIs, and provides additional information such as country details and random cat facts.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NathanKong06/Discord-Bot.git
   cd Discord-Bot
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Discord bot token:

   ```bash
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

## Usage

Run the bot with:

```bash
python bot.py
```

Make sure your bot is invited to your Discord server with the appropriate permissions.

## Commands

Use `/` in your Discord chat to see available commands.

### `/gender`

Predict gender from a name.

- **Parameters:**
  - `name`: The name to analyze (string)
  - `country` (optional): 2-letter country code (e.g., US, GB)

### `/age`

Predict age from a name.

- **Parameters:**
  - `name`: The name to analyze (string)
  - `country` (optional): 2-letter country code (e.g., US, GB)

### `/nationality`

Predict nationality from a name.

- **Parameters:**
  - `name`: The name to analyze (string)

### `/allinfo`

Predict age, gender, and nationality from a name.

- **Parameters:**
  - `name`: The name to analyze (string)
  - `country` (optional): 2-letter country code for age/gender predictions

### `/countryinfo`

Get detailed information about a country.

- **Parameters:**
  - `country_code`: **Only accepts 2-letter ISO country codes** (e.g., US, GB, FR)

### `/catfact`

Get a random cat fact.

### `/help`

Show all available commands.

- **Notes:**
  - Displays a list of commands and brief descriptions in an embed.

## Notes

- The bot uses external APIs:
  - [Genderize.io](https://genderize.io/)
  - [Agify.io](https://agify.io/)
  - [Nationalize.io](https://nationalize.io/)
  - [Catfact.ninja](https://catfact.ninja/)
  - [Rest Countries](https://restcountries.com/)
  - [api.nationalize.io](https://nationalize.io/)
  
- Accuracy depends on the data available in these APIs.

- Country codes should be provided as two-letter ISO codes (e.g., US, GB).

- Make sure your bot has the `applications.commands` scope enabled in the Discord Developer Portal to use slash commands.

- All command responses are now displayed in Discord embeds for enhanced readability and user experience.
