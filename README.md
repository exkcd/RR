# Winston

A personal discord bot (mainly used for testing and crying).

## Running

I don't think a lot of people would run an instance of my bot (because it is so bare bones), but if you happened to stumble upon this repository, and you actually *like* the things I build, I shall provide a guide to help install and run this bot. If it breaks, I'm sorry.

### Steps

1. **Make sure to install Python 3.8 or higher**

Any earlier version will make your life very sad.

2. **Set up a virtual environment**

`python3 -m venv venv` (`python3 -m venv tears` works, too)

3. **Clone this repository**

Self explanatory.

4. **Install dependencies**

Use `pip install -U -r requirements.txt`

**Make sure you are in the virtual environment when doing this:**

```
python3 -m venv path/to/env
source path/to/bin/activate
python3 -m pip install xyz
```

5. **Create a .env file in your bot's main folder**

In the `.env` file, paste your Discord bot token as `TOKEN={bot token here}` (do not put in quotes).

6. **Run your bot**

Run the bot using `python3 bot.py`


## Privacy Policy and Terms of Service

No personal data is stored or used.