prompts = {
#  "create_setting": {
#    "system_prompt": """You are creating the setting for a game world.
#Output a JSON object with the following fields:
#1. city_name - name of the city that will be the central focus of this game
#2. area_description - description of the region around the city, including things like climate, geography, flora and fauna, etc.
#3. history - a few paragraphs of history of the city""",
#    "user_prompt": """Create a setting for a city and surrounding area in a Tolkein-esque fantasy world"""
#  },
  "create_setting": {
    "system_prompt": """You are creating the setting for a game world.
Output a JSON object with the following fields:
1. area_description - description of the region around the city, including things like climate, geography, major landmarks, flora and fauna, etc.
2. history - a few paragraphs of history of the city""",
    "user_prompt": """Create a setting for a city named {} and surrounding area in a Tolkein-esque fantasy world"""
  },
  "build_map": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Output a JSON object that describes the game's map",
"Output format": "A list called 'nodes' with elements that follow the node format",
"node format": "{{"unique_id": "string, a unique ID for each map node",
"name": "string, the name of this node",
"type": "string, the type of this node (see rules)",
"description": "string, a brief one or two sentence description of the node",
"connections": "a list of connections (see connection format)"}}",
"connection format": "{{"connect_id": "A reference to the unique_id of the connecting node",
"connect_name": "A reference to the name of the connecting node",
"how": "A description of how this node connects to the other node.
For field or town areas this can be roads and paths.
For going from town to indoor areas there should be a door or entrance.
Between indoor areas there should be a door or passageway, but these are rare.",
"direction": "the general direction of the connection"}}",
"Rules": ["Node type must be one of the following:
  1. 'town' - outdoor areas that are within town
  2. 'indoor' - interiors of buildings
  3. 'field' - outdoor areas that are outside of town",
"There should be 3 to 5 'town' nodes",
"There should be 3 to 5 'field' nodes",
"There should be 3 to 5 'indoor' nodes",
"'town' nodes can include things like outdoor markets, town squares, major streets, landmarks, etc.",
"'indoor' nodes can include things like taverns, blacksmiths, inns, guilds, storage rooms, etc.",
"'field' nodes can include things like lakes, rivers, forests, mountains, etc.",
"There must be at least one city gate node which is considered a 'town' node",
"'field' nodes can only connect to each other or to a 'town' node if it's a city gate",
"'indoor' nodes can connect to 'town' nodes or to each other but the latter is less common",
"'town' nodes can connect to each other, to 'indoor' nodes, or to 'field' nodes from a city gate node",
"There must be exactly one special 'field' node with unique_id 'dungeon_entrance'",
"The 'dungeon_entrance' node has a special connection to a node with unique_id 'dungeon_start' which is not part of this map"
]""",
#    "system_prompt": """You are building a map for a game world.
#Start by laying out town and field nodes first, then add indoor nodes that connect to town nodes, and finally one
#dungeon entrance connected to a field area that has a few dungeon nodes.
#There should be at around 30 nodes and those nodes should include locations such as:
#Taverns
#Blacksmiths
#Inns
#Guilds
#City gates
#Rural areas
#Rooms in a dungeon
#etc.
#
#Output a JSON object with a list of nodes and each node containing the following fields:
#1. unique_id - A unique ID for each node
#2. name - The name of this node
#3. type - The type of this node.  It must be one of the following:
#  1. 'town' - outdoor areas that are within town
#  2. 'indoor' - interiors of buildings
#  3. 'field' - outdoor areas that are outside of town
#  4. 'dungeon' - rooms of a dungeon
#4. description - A short one or two sentence description of the node
#5. connections - Another list with the fields:
#  1. connect_id - A reference to the unique_id of the connecting node
#  2. connect_name - A reference ot the name of the connecting node
#  3. how - A description of how this node connects to the other node.  It must follow the rules:
#    'town' to 'town' - just give a direction
#    'field' to 'field' - just give a direction
#    'field' to 'town' or 'town' to 'field' - give a direction but it must be at a city gate
#    'town' to 'indoor' - use a door or entrance
#    'indoor' to 'town' - use an exit
#    'indoor' to 'indoor' - use a door or passageway, but these should be limited
#    'field' to 'dungeon' or 'dungeon' to 'field' - can only take place at a dungeon entrance
#    'dungeon' to 'dungeon' - can be quite varied, including directions, doors, and passageways""",

    "user_prompt": """Create a map of an original small city and surrounding area in a Tolkein-esque fantasy world.
Use the following setting information:
{}
"""
  },
  "build_dungeon_map": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Output a JSON object that describes the game's map",
"Output format": "A list called 'nodes' with elements that follow the node format",
"node format": "{{"unique_id": "string, a unique ID for each map node",
"name": "string, the name of this node",
"type": "string, the type of this node (see rules)",
"description": "string, a brief one or two sentence description of the node",
"connections": "a list of connections (see connection format)"}}",
"connection format": "{{"connect_id": "A reference to the unique_id of the connecting node",
"connect_name": "A reference to the name of the connecting node",
"how": "A description of how this node connects to the other node.
Between dungeon areas there can be passageways, doors, stairs, etc.",
"direction": "the general direction of the connection"}}",
"Rules": ["Node type for the dungeon map is always 'dungeon'",
"There should be 5 to 8 dungeon nodes",
"There must be exactly one starting dungeon node with unique_id 'dungeon_start'",
"The starting dungeon node has a special connection to a node with unique_id 'dungeon_entrance' that is not part of this map",
"There must also be one dungeon boss node",
]""",
    "user_prompt": """Create a map of a small underground dungeon in a Tolkein-esque fantasy world.
Use the following setting information:
{}
"""
  },
  "find_starting_point": {
    "system_prompt": """Based on the map information in the content, give the unique_id of the node that makes the best starting point for new adventurers.
Output just the unique_id of the node and nothing else."""
  },
  "describe_node": {
    "system_prompt": """You are describing a scene in a game world.
Based on the data in the content create a more few paragraphs of description for the location""",
    "user_prompt": """setting_info = {}
    
location_info = {}"""
  },
  "create_npcs": {
    "system_prompt": """You are describing characters in a game world.
Output a JSON object with a list of characters, each entry containing the following fields:
1. unique_id - a unique id for this character
2. name - the character's name
3. race - the character's race (i.e., human, elf, dwarf, etc.)
4. gender - the character's gender
5. profession - the character's profession
6. physical_description - a one or two sentence description of what the character looks like
7. personality - a one or two sentence description of this character's personality
8. location_id - the unique_id of the node where the character is currently located
9. relationships - optional, a list describing this character's relationships with other characters.  Has the following fields:
  1. relation_id - a reference to the unique_id of the character they have a relationship with
  2. relationship - the nature of their relationship, i.e. 'lover', 'father', 'mother', 'son', 'daughter', etc.

Use the JSON map data for more context and to get location_ids""",
    "user_prompt": """Create about a dozen characters to populate the following map in a Tolkein-esque fantasy world:
{}

Given the setting:
{}"""
  },
  "character_details": {
    "system_prompt": """"Role": "You are writing more detailed descriptions of characters in a game world given some basic information about them",
"Task": "Based on the given setting and character info output a JSON object with more detail about that character",
"Output format": {{"clothes": "Describe the character's clothing",
"height": "Give a rough non-numeric height (i.e., tall, short, very tall, average etc.) for this character",
"hair": "Describe character's hair color and style",
"eyes": "Describe the character's eyes",
"build": "Describe the character's build or figure",
"equipment": "Describe any notable equipment the character usually carries",
"hobby": "Come up with one hobby for this character that has nothing to do with their profession, i.e. fishing, gardening, playing a musical instrument, etc.",
"likes": "List a few things this character likes",
"dislikes": "List a few things this character dislikes",
"relationship_status": "Married, dating someone, single, not interested, etc.",
"backstory": "Based on the data write a couple paragraphs of backstory for this character"
}}""",
    "user_prompt": """setting_info = {}

character_info = {}"""
  },
  "character_backstory": {
    "system_prompt": """You are describing the backstory of characters in a game world.
Based on the data in the content write a backstory for this character""",
    "user_prompt": """setting_info = {}
    
character_info = {}"""
  },
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
  "look_around": {
    "system_prompt": """You are a narrator for a text-based adventure game.
Describe the location, connections, and any characters present (if any) from the given data in roughly one paragraph"""
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
"description": "Required, one second-person sentence describing the action that is being taken, not the outcome."
}},
"Rules": ["Interpret the command given in the content and return a JSON object.",
"The target for the command must be present at or connected to the current location. If it's not the command fails.",
"If the target for the command is a location or character, the value for the target parameter must be just its unique_id",
"If the target for the command is not a location or character then its value can be a one or two word description",
"The command must be one of the following:
  1. 'look_around' - just look around in general
  2. 'look_at' - look at a specific object, character, place, etc.
  3. 'move' - move to a new location
  4. 'talk' - begin dialogue with a character
  5. 'invite' - you are inviting a character to join your party
  6. 'exit_game' - exit or quit the game
  7. 'save_game' - save the game state
  8. 'status' - look at user's status
  9. 'unknown' - command not understood, anything that isn't one of the above"
],

"data": {},
"""
#Interpret the command given in the content and return a JSON object with the following fields:
#1. success - 0 if the command fails or 1 if it succeeds
#2. target - optional, target of the command.  Could be a character, object, new location, etc.  If it is a character or location node use the appropriate unique_id. If it is a character they must be present for the command to succeed.  If it is a location it must be a valid connection.
#3. command - interpret what the user is trying to do, must be one of the following:
#  1. 'look_around' - just look around in general
#  2. 'look_at' - look at a specific object, character, place, etc.
#  3. 'move' - move to a new location
#  4. 'talk' - begin dialogue with a character
#  5. 'exit_game' - exit the game
#  6. 'unknown' - command not understood, anything that isn't one of the above"""
  },
#  "talk_to": {
#    "system_prompt": """Return a JSON object with the following fields:
#1. finish - 0 if the conversation should continue (default) or 1 if the conversation is over, either because the user is asking it to end or if the character is done talking
#2. response - your response to the conversation as the appropriate character in first person
#
#You are acting as the following character:
#{}"""
#  }
  "talk_to": {
#    "system_prompt": """Act in first person as the character described below.
#Act more or less friendly towards the user based on your friendship level, which should be a value between -10 and 10.
#0 is completely neutral.
#-10 would be their most hated enemy.
#10 would be their closest friend or lover.
#
#character = {}
#""",
    "system_prompt": """Act in first person as the character described below.
Your attitude towards the user is: {}

character = {}
""",
#""""Role:": "Act in first person as the character described below",
#"Response": "Output a JSON object with exactly two fields:
#  1. 'finish' - Should be 0 the majority of the time as the conversation continues and only set to 1 if the conversation is over, either because the user is asking to end the conversation or if the character no longer wishes to talk to the user
#  2. 'message' - your in-character response to the conversation
#  3. 'friendship_change' - a floating point number indicating how this conversation has changed the character's friendship with the user",
#"Character": {}
#""",
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
  "fight": {
    "system_prompt": """"Role": "You are narrating a battle in a fantasy game world",
"Task": "Based on the user's actions, abilities and level, status, any companions present, and the number and strength of monsters present, and what happened in previous rounds output a JSON object that describes a round of the battle",
"Output format": {{"fight_status": "Required, 'victory' if the user wins, 'continuing' if the fight isn't over yet, 'fled' if the user successfuly flees, or 'defeat' if the user is defeated.",
"fatigue": "Optional, the user's fatigue status after this round if it has changed. Can be 'none', 'slight', 'moderate', or 'severe'.",
"injuries": "Optional, the user's injury status after this round if it has changed. Can be 'none', 'slight', 'moderate', or 'severe'.",
"description": "Required, give a few sentences describing what happens in this round of the fight, including what the opponent does."
}},
"Rules": ["Each round calculate the fight status and any fatigue or injuries first, then describe the scene.  Make sure to include what the user's opponent does.",
"The base chance of achieving victory is as a percentage is 30 + (user's level - opponents level) * 10 + 5 * number of previous rounds.",
"Minimum chance of victory is 0, max is 100 percent.",
"The base chance of being injured is (opponents level - user's level + 1) * 10 percent.",
"Injuries increases one level at a time, 'none' to 'slight' to 'moderate' to 'severe'."
"The base chance of fatigue increasing is 10 * the user's rounds rounds_since_rest stat.",
"Fatigue increases one level at a time, 'none' to 'slight' to 'moderate' to 'severe'.",
"The base chance of defeat is 0 if injuries are 'none', 10 percent if injuries are 'slight', 30 percent if injuries are 'moderate', and 50 percent if injuries are 'severe'.",
"There can't be victory and defeat.  If both are rolled consider it a victory.",
"If the user's fatigue is 'slight', multiply the chance of victory by 0.9.",
"If the user's fatigue is 'moderate', multiply the chance of victory by 0.7 and the chance of injuries by 1.2.",
"If the user's fatigue is 'severe', multiply the chance of victory by 0.5 and the chance of injuries by 1.5",
"The user can also attempt to flee. This has a base chance of 80 percent.",
"Attacking the opponent with something they are resistant to multiplies the chance of victory by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of victory.",
"The user may use skills they possess. These skills multiply the chance of victory by 1.5 but double the chance of fatigue.",
"If the user attempts to use a skill they don't possess or doesn't do anything their chance of victory for the round is 0.",
"If you feel the user's action is particularly appropriate for the situation multiply the chance of victory by 1.2."],

"user_data": {},
"monster_data": {},
"previous_rounds": {}
"""
  },
  "fight2": {
    "system_prompt": """"Role": "You are refereeing and narrating a battle in a fantasy game world",
"Task": "Based on the user's actions and given base probabilities, output a JSON object that describes one round of the battle",
"Output format": {{"attacks": "Required, a list of attacks by the user or companions against enemies. Follows 'attack format'.",
"enemy_attacks": "Required, a list of attacks by enemies against the user or companions.  Follows 'enemy attack format'.",
"fatigue": "Required, a list of possible fatigue changes.  Follows 'fatigue format'.",
"description": "Required, wrote a few sentences describing what happens in this round of the fight, including what companions and enemies do."
}},
"attack format": {{"attacker_id": "either 'user' or unique_id of companion",
"attack_target_id": "unique_id of enemy being attacked",
"attack_result": "1 if enemy is defeated, 0 otherwise"
}},
"enemy attack format": {{"enemy_id": "unique_id of the enemy attacking",
"enemy_attack_target": "either 'user' or unique_id of companion",
"injury": "1 if an injury was caused, 0 otherwise",
"defeat": "1 if the character was defeated, 0 otherwise"
}},
"fatigue format": {{"id": "either 'user' or unique_id of companion",
"fatigued": "1 if the character is fatigued, 0 otherwise",
}},
"Rules": ["The user attacks as specified in the content, or they can attempt to flee",
"Each companion in the companion data should also make one attack per round",
"Each enemy in the enemy data should also make one attack per round",
"If the user attempts to use a skill they don't possess or doesn't specify an action they take no action that round",
"Companions attack whatever targets as they wish to, though they can take suggestions from the user",
"Enemies attack the user or companions as they wish to",
"Base probabilities for various outcomes are given below",
"The user may use skills they possess. These skills multiply the chance of defeating an enemy by 1.5 but double the chance of fatigue.",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If you feel the user's action is particularly appropriate for the situation multiply the chance of defeating an enemy by 1.2.",
"If a character already has 'severe' injuries and they are injured further then they are defeated."],

"User data": {},
"Companion data": {},
"Enemy data": {},
"Base probabilities": {},
"previous_rounds": {}
"""
  },
  "fight_user": {
    "system_prompt": """"Role": "You are refereeing and narrating a battle in a fantasy game world",
"Task": "It's the user's turn to attack, based on their actions, output a JSON object that describes one round of the battle",
"Output format": {{"attacks": "Required, a list of attacks by the user against enemies. Follows 'attack format'.",
"fatigued": "Required, 1 if the user is fatigued, 0 otherwise",
"fled": "Required, 1 is the user successfully flees, 0 otherwise",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"attack format": {{"attacker_id": "either 'user' or unique_id of companion",
"attack_target_id": "unique_id of enemy being attacked",
"attack_result": "1 if enemy is defeated, 0 otherwise"
}},
"Rules": ["The user attacks as specified in the content, or they can attempt to flee",
"If the user attempts to use a skill they don't possess or doesn't specify an action they take no action that round",
"Base probabilities for various outcomes are given below",
"The user may use skills they possess. These skills multiply the chance of defeating an enemy by 1.5 but double the chance of fatigue.",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If you feel the user's action is particularly appropriate for the situation multiply the chance of defeating an enemy by 1.2."],

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
"fatigued": "Required, 1 if the companion is fatigued, 0 otherwise",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"attack format": {{"attacker_id": "either 'user' or unique_id of companion",
"attack_target_id": "unique_id of enemy being attacked",
"attack_result": "1 if enemy is defeated, 0 otherwise"
}},
"Rules": ["Companions can attack whatever targets as they wish to",
"Base probabilities for various outcomes are given below",
"The user may use skills they possess. These skills multiply the chance of defeating an enemy by 1.5 but double the chance of fatigue.",
"Attacking the opponent with something they are resistant to multiplies the chance of defeating them by 0.5.",
"Attacking the opponent with something they are weak to doubles the chance of defeating them.",
"If you feel the user's action is particularly appropriate for the situation multiply the chance of defeating an enemy by 1.2."],

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
"Output format": {{""enemy_attacks": "Required, a list of attacks by enemies against the user or companions.  Follows 'enemy attack format'.",
"description": "Required, write a sentence or two describing what happens in this round of the fight."
}},
"enemy attack format": {{"enemy_id": "unique_id of the enemy attacking",
"enemy_attack_target": "either 'user' or unique_id of companion",
"injury": "1 if an injury was caused, 0 otherwise",
"defeat": "1 if the character was defeated, 0 otherwise"
}},
"Rules": ["Enemies can attack the user or companions as they wish to",
"Base probabilities for various outcomes are given below",
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
  }
}