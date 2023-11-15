# GPT Adventure
GPT-based text adventure game

## Overview
There are of course many examples of creating a text adventure style game with just a single prompt to ChatGPT.  That isn't what this is.
While that sort of approach is certianly interesting, there are still a lot of limitations.  For one, the entire game state is basically
just your chat history.  That imposes limitations if you want to alter game state outside of responses to the user, whether that's AI doing
something in the background or even potentially a multiplayer MUD-style game.

GPT Adventure is still a single player game, but it's built in a way that I think is more extensible.  It's based on the idea that a setting
is first created with a great deal of detail and then appropriate details are passed into prompts while playing to create a consistent experience.
There are multiple modes within the game for things like normal exploration, dialogue with NPCs, and combat.

## How to play

Install requirements (pip install -r requirements.txt).  They are pretty small since GPT Adventure mostly relies on the GPT API.

You will need an OpenAI API key.  Create an account at https://openai.com, log in, go to "API keys" at the side bar and create a key.  Then set the
value in the keys.ini file to your key.

It is highly recommended you add some money to your account.  Not because it costs a lot to play (the $5 of free credits you get when creating an
account is plenty), but because completley free accounts have limitations on how often they can query the API, and that will make running the game
extremely slow and difficult.

To generate a new world run worldgenerate.py.  Or just use the included Stormfell.json example.

To play the game run play_game.py.

## Features

### Hiearchical World generation

World generation uses GPT in a top-to-bottom way.  That is to say, it starts with prompts that just write a general setting information, then further
prompts use the results from the earlier prompts as input to add more and more detail all the way down to writing backstories for every NPC.  This not
only avoids issues with token limits, but I find it creates better results anyway.

### Setting informs details

An extensive amount of detail is created during world generation.  It is then available to pass into prompts as appropriate while the user explores
the world.  It's of course not necessary (and often not even desirable) to pass all of the setting information into every prompt.  For example,
when you look at an NPC the prompt is informed with details about their physical appearance, but information about their personality or backstory
isn't.  Yes that saves tokens but even more importantly that information shouldn't be available from just looking anyway.

### 'Character creation'

There is a very free-form character creation system.  The player simply answers a few questions however they want, however GPT is used to check that their
responses seem appropriate for a new adventurer in the setting.  So characters can be rejected if they're too outlandish.

### Multiple modes

The standard game mode is basically an interpreter for commands like looking at things, moving between locations, etc.  However there are additional
gameplay modes as well.  When you begin a conversation with an NPC it goes into a dialogue mode where GPT acts more as a standard chatbot simply
playing as that character.  There's also a mode for engaging in combat with monsters.

### Character relationships

You can increase your friendship level with NPCs just by talking to them.  As you do they change their attitude towards you and if the friendship level
is high enough you can recruit them to join your party.

### Hybrid roleplaying combat

There is combat in GPT Adventure, though it's not exactly stat-heavy traditional RPG combat.  It uses a probabalistic model that doesn't have detailed
tracking of things like hit points.  Base probabilities are calcualted in standard Python code, however GPT is used to determine and narrate the outcome.
The player can also get bonuses to their chances for particularly appropriate descriptions.

### Human-readable seting information

Running worldgenerate.py creates a new setting from scratch.  However the output is simply a JSON file.  That means that if the user wants to tweak any
aspects of the setting, they are free to do so.  It's even possible to write the whole setting from scratch and not use the world generator at all, so
long as the formatting is followed.

(Note that once you save a game the setting is included in the save file so you have to start a new game for any changes in the JSON to take effect)
