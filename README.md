# Discord Bot

A Discord bot that predicts gender, age, and nationality based on a given name using external APIs.

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

The bot uses slash commands. Use `/` in your Discord chat to see available commands.

### `/gender`

Predict gender from a name.

- **Parameters:**
  - `name`: The name to analyze (string)

- **Example:**

  ```text
  /gender name:Alice country:US
  ```

- **Response:**

  ```text
  Name: Alice
  Gender: Female
  Probability: 100%
  Based on: 69089 sample(s)
  ```

### `/age`

Predict age from a name.

- **Parameters:**
  - `name`: The name to analyze (string)
  - `country` (optional): 2-letter country code (e.g., US, GB, AU, FR)

- **Example:**

  ```text
  /age name:Alice country:US
  ```

- **Response:**

  ```text
  Name: Alice
  Country Applied: US
  Predicted Age: 66
  Based on: 3434 sample(s)
  ```

### `/nationality`

Predict nationality from a name.

- **Parameters:**
  - `name`: The name to analyze (string)

- **Example:**

  ```text
  /nationality name:Alice
  ```

- **Response:**

  ```text
  Name: Alice
  CN — 16%
  IT — 5%
  CM — 3%
  RO — 3%
  HK — 3%
  ```

### `/allinfo`

Predict age, gender, and nationality from a name.

- **Parameters:**
  - `name`: The name to analyze (string)
  - `country` (optional): 2-letter country code for age/gender

- **Example:**

  ```text
  /allinfo name:Alice country:US
  ```

- **Response:**

  ```text
  Name: Alice
  Gender: Female (Probability: 100%, Based on 69089 sample(s))
  Predicted Age: 66 (Based on 3434 sample(s))
  Predicted Nationalities (Top 5): CN (16%), IT (5%), CM (3%), RO (3%), HK (3%)
  ```

### `/help`

Show all available commands.

- **Example:**

  ```text
  /help
  ```

- **Response:**

  ```text
  Available Commands:
  /gender — Predict gender from a name
  /age — Predict age from a name
  /nationality — Predict nationality from a name
  /allinfo — Predict age, gender, and nationality from a name
  /help — Show all available commands
  ```

## Notes

- The bot uses external APIs:
  - [Genderize.io](https://genderize.io/)
  - [Agify.io](https://agify.io/)
  - [Nationalize.io](https://nationalize.io/)

- Accuracy depends on the data available in these APIs.

- Country codes should be provided as two-letter ISO codes (e.g., US, GB).

- Make sure your bot has the `applications.commands` scope enabled in the Discord Developer Portal to use slash commands.
