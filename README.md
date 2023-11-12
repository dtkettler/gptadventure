# GPT Adventure
GPT-based text adventure game

## Overview
There are of course many examples of creating a text adventure style game with just a single prompt to ChatGPT.  That isn't what this is.
While that sort of approach is certianly interesting, there are still a lot of limitations.  For one, the entire game state is basically
just your chat history.  That imposes limitations if you want to alter game state outside of responses to the user, whether that's AI doing
something in the background or even potentially a multiplayer MUD-style game.

GPT Adventure is still a single player game, but it's built in a way that I think is more extensible.  It's based on the idea that a setting
is first created with a great deal of detail and then appropriate details are passed into prompts while playing to create a consistent experience.

## Features

### Hiearchical World generation

World generation uses GPT in a top-to-bottom way.  That is to say, it starts with prompts that just write a general setting, then further prompts
use the results from the earlier prompts as input to add more and more detail all the way down to writing backstories for every NPC.  This not
only avoids issues with token limits, but I find it creates better output anyway.

### Setting informs details

An extensive amount of detail is created during world generation.  It is then available to pass into prompts as appropriate while the user explores
the world.  It's of course not necessary (and often not even desirable) to pass all of the setting information into every prompt.  For example,
when you look at an NPC the prompt is informed with details about their physical appearance, but information about their personality or backstory
isn't.  Yes that saves tokens but even more importantly that information shouldn't be available from just looking anyway.

### Multiple modes

The standard game mode is basically an interpreter for commands like looking at things, moving between locations, etc.  However there are additional
gameplay modes as well.  When you begin a conversation with an NPC it goes into a dialogue mode where GPT acts more as a standard chatbot simply
playing as that character.  There's also a mode for engaging in combat with monsters.

### Character relationships

### Hybrid combat
