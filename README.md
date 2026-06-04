# Discord Bot with Extensions (Cogs)

This is a modular Discord bot built with `discord.py`. It uses "Cogs" to organize commands into different extensions.

## Features

- Modular architecture using Cogs.
- Simple setup with environment variables.
- Example commands: `!ping`, `!getout`.

## Prerequisites

- Python 3.8 or higher.
- A Discord Bot Token (from the [Discord Developer Portal](https://discord.com/developers/applications)).

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_bot_token_here` with your actual Discord bot token.

## Running the Bot

Start the bot by running:
```bash
python main.py
```

## Project Structure

- `main.py`: The entry point of the bot. Loads extensions and starts the bot.
- `cogs/`: Directory containing all bot extensions (Cogs).
  - `fun.py`: Contains fun commands like `!ping` and `!getout`.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment variables (not tracked by Git).

## Commands

- `!ping`: Responds with "Pong!".
- `!getout`: Sends a GIF that says "GET OUT!!!".
