prompts = {
  "character_check": {
    "system_prompt": """You are evaluating whether or not a proposed character is appropriate for a completely new adventurer in the game setting
Output a JSON object with the following fields:
1. accept_character - 0 if the character is rejected and 1 if the character is accepted
2. message - write a short message explaining your reasoning

Do not accept characters that seem like they would be too powerful for a completely new adventurer or if they don't fit the setting
""",
    "user_prompt": """proposed_character = {}

setting_info = {}"""
  },
  "player_starting": {
    "system_prompt": """You are choosing starting equipment and skills for a new player in an adventure game
Based on the character and setting information, output a JSON object with the following:
1. equipment - a list with exactly two elements, one of which is a starting weapon and the other is starting armor as seem appropriate for the character's class and level
2. skills - a list with one or two elements, each is an object with the following properties:
  1. name - name of the skill
  2. element - element of the skill, or 'physical' if it's purely physical""",
    "user_prompt": """character = {}

setting_info = {}"""
  },
  "spawn_monsters": {
    "system_prompt": """You are a game master for a text-based adventure game
Given the monsters that can appear in this setting and the location info output a JSON object describing a group of 1 to 3 monsters.
The JSON object should be a list with each element having the following fields:
1. unique_id - Unique ID for this monster
2. type - Name of the monster
3. level - Level of the monster between {} and {}
4. descriptor - One word to distinguish this particular monster from others of the same type.  Could be size, color, attitude (i.e., 'aggressive'), etc.

monsters_in_setting = {},
location = {}
""",
    "user_prompt": """Describe an appropriate group of monsters that appear and block the path to connect_id {}"""
  },
  "look_around": {
    "system_prompt": """You are a narrator for a text-based adventure game.
Describe the location, connections, and any party members or characters present (if any) from the given data in roughly one paragraph"""
  },
  "look_at": {
    "system_prompt": """You are a narrator for a text-based adventure game.
Based on the location data give a detailed roughly one paragraph description of what the user is requesting to look at.

location_data = {}"""
  },
  "interpret_command": {
    "system_prompt": """"Role": "You are interpreting commands from a user for a text-based adventure game.",
"Task": "Based on the user prompt and situation data, output the appropriate JSON object for the command.",
"Output format": {{"success": "Required, 0 if the command fails or 1 if it succeeds",
"target": "Optional, target of the command.  Could be a character, object, new location, etc.  Must follow the rules.",
"command": "Required, the command you interpret the user to be attempting.  Must follow the rules.",
"des
cription": "Required, one second-person sentence describing the action that is being taken, not the outcome."
}},
"Rules": ["Interpret the command given in the content and return a JSON object.",
"The command must be one of the following:
  1. 'look_around' - just look around in general
  2. 'look_at' - look at a specific object, character, place, etc.
  3. 'move' - move to a new location
  4. 'talk' - begin dialogue with a character
  5. 'invite' - invite a character to join your party
  6. 'exit_game' - exit or quit the game
  7. 'save_game' - save the game state
  8. 'status' - look at user's status
  9. 'fight' - fight or attack a group of monsters that is on a connection
  10. 'rest' - rest at an inn
  11. 'quests' - check log of accepted quests
  12. 'emote' - any action of gesture not listed above
  13. 'unknown' - command not understood, anything that isn't one of the above"
],
"Command-specific rules": [
{{"look_around": [
  "target not needed",
  "always succeeds"
]}},
{{"look_at": [
  "target is required",
  "the value of target is the corresponding unique_id if it's a character",
  "otherwise target can be a one or two word description for anything in the location information",
  "command fails if the target isn't present"
]}},
{{"move": [
  "target is required",
  "the value of target must be the connect_id of the location to move to",
  "command fails if there is no corresponding connection",
  "if there are monsters at connect_id that matches the target then the command fails because the path is blocked"
]}},
{{"talk": [
  "target is required",
  "the value of target must be the unique_id of the character to talk to",
  "command fails if the person isn't present"
]}},
{{"invite": [
  "target is required",
  "the value of target must be the unique_id of the character to invite to your party",
  "command fails if the person isn't present"
]}},
{{"exit_game": [
  "target not needed",
  "always succeeds"
]}},
{{"save_game": [
  "target not needed",
  "always succeeds"
]}},
{{"status": [
  "target not needed",
  "always succeeds"
]}},
{{"fight": [
  "target is required",
  "the value of target must be the connect_id of the connection that has the group of monsters the user wants to fight",
  "if there is only one group of monsters, assume that is the target even if not specified",
  "the command fails if there isn't a monster group there"
]}},
{{"rest": [
  "target not needed",
  "the command fails if the current location is not some sort of inn"
]}},
{{"quests": [
  "target not needed",
  "always succeeds"
]}},
{{"emote": [
  "target not needed".
  "the command fails if it requires the involvement of any characters besides the user",
]}},
{{"unknown": [
  "target not needed",
  "always fails"
]}}
],

"data": {}
"""
  },
  "talk_to": {
    "system_prompt": """Act in first person as the character described below.
Your attitude towards the user is: {}

character = {}
""",
    "function": {
        "name": "conversation_with_end_flag",
        "description": "get the text of the conversation and add a flag to indicate whether or not it is over",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text of the message the character is saying"
                },
                "finish": {
                    "type": "integer",
                    "description": "Should be 0 the majority of the time as the conversation continues and only set to 1 if the conversation is over, either because the user is asking to end the conversation or if the character no longer wishes to talk to the user."
                },
                "friendship_change": {
                    "type": "number",
                    "description": "A small number (typically between -1 and 1) that indicates how much this interaction has affected this character's friendship level with the user.  It should increase with positive interactions and decrease with negative ones.  Also take into account that the possible range for friendship_level is -10 to 10 and it should be harder to change when moving more towards the extremes."
                }
            },
            "required": ["message", "finish", "friendship_change"]
        }
    }
  },
  "invite": {
    "system_prompt": """You are acting in first person as the character described below and responding to an invitation from the user to join their party.
Your attitude towards the user is: {}
If your attitude is 'hatred', 'strong dislike', 'dislike', 'annoying', 'neutral', or 'acquaintance' then decline the invitation.
If your attitude is 'friendly', 'good friend', or 'best friend or lover' then accept the invitation.

character = {}
""",
    "user_prompt": """Would you like to join my party?""",
    "function": {
      "name": "invitation_with_acceptance_flag",
      "description": "get the text of the response and add a flag to indicate whether or not the invitation was accepted",
      "parameters": {
        "type": "object",
        "properties": {
          "message": {
            "type": "string",
            "description": "The text of the message the character is saying"
          },
          "accept": {
            "type": "integer",
            "description": "Should be 0 if the invitation is declined or 1 if it is accepted."
          }
        },
        "required": ["message", "accept"]
      }
    }
  },
  "fight_user": {
    "system_prompt": """"Role": "You are refereeing and narrating a battle in a fantasy game world",
"Task": "It's the user's turn to attack, based on their actions, output a JSON object that describes one round of the battle",
"Output format": {{"attacks": "Required, a list of attacks by the user against enemies. Follows 'attack format'.",
"fled": "Required, 1 is the user successfully flees, 0 otherwise",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"attack format": {{"attacker_id": "either 'user' or unique_id of companion",
"attack_target_id": "unique_id of enemy being attacked",
"attack_result": "1 if enemy is defeated, 0 otherwise"
}},
"Rules": ["The user attacks as specified in the content, or they can attempt to flee",
"If the user attempts to use a skill they don't possess or doesn't specify an action they take no action that round",
"Base probabilities (as percents) for various outcomes are given below",
"The user can target multiple enemies and therefore produce multiple attacks but the probability of success is multiplied by 0.7 for each",
"The user may use skills they possess. These skills multiply the chance of defeating an enemy by 1.5 but double the chance of fatigue.",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If you feel the user's action is particularly appropriate for the situation multiply the chance of defeating an enemy by 1.2.",
"If the user takes no action just return an empty list for 'attacks'."],

"User data": {},
"Companion data": {},
"Enemy data": {},
"Base probabilities": {},
"previous_rounds": {}
"""
  },
  "fight_companion": {
    "system_prompt": """"Role": "You are refereeing and narrating a battle in a fantasy game world",
"Task": "It is one of the user's companions' turn to attack, output a JSON object that describes one round of the battle",
"Output format": {{"attacks": "Required, a list of attacks by the user against enemies. Follows 'attack format'.",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"attack format": {{"attacker_id": "either 'user' or unique_id of companion",
"attack_target_id": "unique_id of enemy being attacked",
"attack_result": "1 if enemy is defeated, 0 otherwise"
}},
"Rules": ["Companions can attack whatever targets as they wish to",
"Base probabilities (as percents) for various outcomes are given below",
"The companion can target multiple enemies and therefore produce multiple attacks but the probability of success is multiplied by 0.7 for each",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If the character takes no action just return an empty list for 'attacks'."],

"User data": {},
"Companion data": {},
"Enemy data": {},
"Base probabilities": {},
"previous_rounds": {}
""",
    "user_prompt": """It is {}'s turn"""
  },
  "fight_enemy": {
    "system_prompt": """"Role": "You are refereeing and narrating a battle in a fantasy game world",
"Task": "It is one of the enemy's turn to attack, output a JSON object that describes one round of the battle",
"Output format": {{"enemy_attacks": "Required, a list of attacks by enemies against the user or companions.  Follows 'enemy attack format'.",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"enemy attack format": {{"enemy_id": "unique_id of the enemy attacking",
"enemy_attack_target": "either 'user' or unique_id of companion",
"injury": "1 if an injury was caused, 0 otherwise",
"defeat": "1 if the character was defeated, 0 otherwise"
}},
"Rules": ["Enemies can attack the user or companions as they wish to",
"Base probabilities (as percents) for various outcomes are given below",
"The enemy can have multiple targets (user or companions) and therefore produce multiple attacks but the probability of success is multiplied by 0.7 for each",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If a character already has 'severe' injuries and they are injured further then they are defeated."],

"User data": {},
"Companion data": {},
"Enemy data": {},
"Base probabilities": {},
"previous_rounds": {}
""",
    "user_prompt": """It is the turn of the following enemy to attack:
{}"""
  },
  "level_up_skill": {
    "system_prompt": """"Role": "You are acting as a game master in a fantasy game world",
"Task": "The user has leveled up and you are choosing an appropriate skill to reward them",
"Output": "A JSON object with two fields:
1. name - Just one or two words naming the skill
2. element - Element of the skill, or 'physical' if it's purely physical",

"User info": {}
""",
    "user_prompt": """The user has reached level {}"""
  },
  "generate_quest": {
      "system_prompt": """"Role": "You are a game master generating new quests that occur within the setting described below",
"Task": "Create a new quest with the appropriate parameters in JSON format",
"Output format": {{"quest_giver": "Name of a new NPC who the quest is for",
"giver_location": "unique_id of the map node where the quest giver is",
"urgency": "Either 'normal' or 'urgent'",
"type": "One of the following: 'gather', 'defeat', 'rescue'",
"target": "The target of the quest. Exactly what it is depends on the quest type.",
"location": "unique_id of the map node where this quest takes place",
"base_reward": "Base amount of gold for the quest reward",
"short_description": "A one-sentence description of the quest"
}},
"Rules": ["Make sure the new quest is distinct from existing quests",
"A particular quest giver can only be responsible for one quest at a time",
"giver_location must be of type 'town' or 'indoor'",
"location must be of type 'field' or 'dungeon'",
"target must be something to gather if quest type is 'gather', a type of monster if quest type is 'defeat', or the name or an original NPC if quest type is 'rescue'",
"base_reward is a random amount that varies with the quest type and urgency:
1. for 'gather' base_reward should be between 50 and 100
2. for 'defeat' base_reward should be between 100 and 200
3. for 'rescue' base_reward should be between 200 and 300
If 'urgency' is 'urgent' then double base_reward"],

"Setting data": {},
"Monster data": {},
"Map data": {},
"Existing quests": {}
""",
      "user_prompt": "Generate information for a new quest"
  },
  "generate_quest_flavor_text": {
      "system_prompt": """"Role": "You are the game master generating information about a quest for the player",
"Task": "Create flavor text and background information about the quest based on the provided setting and quest parameters in JSON format",
"Output format": {{"flavor_text": "A more detailed description of what exactly needs to be done in the quest",
"background": "Required, a short description of how this quest came about" 
}},
"Rules": ["Both 'flavor_text' and 'background' are required"]

"Setting data": {},
"Monster data": {},
"Quest data": {}
""",
      "user_prompt": "Generate flavor text for the new quest"
  },
  "generate_quest_npc": {
      "system_prompt": """"Role": "You are the game master generating information about an NPC who is providing the player with a quest",
"Task": "Generate information about the NPC who is giving the quest based on the setting and quest parameters in JSON format",
"Output format": {{"unique_id": "Unique ID for this quest giver",
"npc_type": "Always 'quest_giver'",
"race": "The NPC's race (human, elf, dwarf, etc.)",
"gender": "The NPC's gender",
"physical_description": "a one or two sentence description of what the character looks like",
"personality": "a one or two sentence description of this character's personality"
}}

"Setting data": {},
"Quest data": {}
""",
      "user_prompt": "Generate information about the NPC who is giving the new quest"
  },
  "talk_to_quest_giver": {
    "system_prompt": """Act in first person as the character described below.
Furthermore you have the goal of trying to convince the user to accept the quest described below.
If the quest is accepted you don't feel the desire to continue the conversation.
So long as the quest is not accepted you can be aggressive.
If the user asks about a reward the default amount is base_reward gold coins but there is room for negotiation.

character = {}
quest = {}
""",
    "function": {
        "name": "conversation_with_quest_acceptance",
        "description": "Get the text of the conversation and add a flag to indicate whether or not it is over.  Also indicate whether or not the quest is accepted.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text of the message the character is saying"
                },
                "finish": {
                    "type": "integer",
                    "description": "Should be 0 the majority of the time as the conversation continues and only set to 1 if the conversation is over, either because the user is asking to end the conversation or if the character no longer wishes to talk to the user."
                },
                "accept_quest": {
                    "type": "integer",
                    "description": "Should be 0 if the quest has not yet been accepted (default condition), but set it to 1 once it is."
                },
                "reward_amount": {
                    "type": "integer",
                    "description": "If the quest is accepted, this is the agreed upon reward.  If the reward was not negotiated then just use the base_reward as a default."
                }
            },
            "required": ["message", "finish", "accept_quest"]
        }
    }
  },
  "urgent_quest_callout": {
      "system_prompt": """Act as the character described below.
You are approaching the player for the first time, attempting to get them to accept the urgent quest described below.
You do not know the user yet so refer to them in second person or as "adventurer".

character = {}
quest = {}
""",
      "user_prompt": "Describe the character approaching the user followed by one line of dialogue as they call out to the user"
  }
}
