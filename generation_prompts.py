prompts = {
  "create_setting": {
    "system_prompt": """You are creating the setting for a game world.
Output a JSON object with the following fields:
1. area_description - description of the region around the city, including things like climate, geography, major landmarks, flora and fauna, etc.
2. history - a few paragraphs of history of the city""",
    "user_prompt": """Create a setting for a city named {} and surrounding area in a Tolkein-esque fantasy world"""
  },
  "create_monster_setting": {
    "system_prompt": """You are creating the setting for a game world.
Based on the setting data, output a JSON object with the following fields:
1. field_monsters - a list of 3 to 5 low-level types monsters that might appear in outdoor areas
2. dungeon_monsters - a list of 3 to 5 mid-level types monster that might appear in dungeon areas
3. dungeon_boss - a single high-level monster that serves as the boss of the local dungeon

Each monster type should then contain the following fields:
1. name - Required, 1 or 2 words that names the kind of monster.
2. description - Required, a short description of the monster.
3. resistances - Optional (per monster type), a list of types of damage the monster is resistant to. Could be elements, poison, physical attacks, etc.
4. weaknesses - Optional (per monster type), similar to resistances but a list of types of damage the monster is weak to.
5. equipment - Optional (per monster type), typically only humanoid monsters will have this.  Could be basic weapons likes clubs, etc.
""",
    "user_prompt": """Create some monsters to populate the Tolkein-esque fantasy world with the following setting:
{}"""
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
For field or town areas this can be roads and paths.",
"direction": "the general direction of the connection"}}",
"Rules": ["Node type must be one of the following:
  1. 'town' - outdoor areas that are within town
  2. 'field' - outdoor areas that are outside of town",
"There should be 4 to 6 'town' nodes",
"There should be 4 to 6 'field' nodes",
"Every node must have at least one connection",
"It must be possible to go from any node in this map to any other by following connections",
"'town' nodes can include things like outdoor markets, town squares, major streets, landmarks, etc.",
"'field' nodes can include things like lakes, rivers, forests, mountains, etc.",
"There must be at least one city gate node which is considered a 'town' node",
"'field' nodes can only connect to each other or to a 'town' node if it's a city gate",
"'town' nodes can connect to each other or to 'field' nodes from a city gate node",
"There must be exactly one 'field' node with unique_id 'field_to_dungeon' that marks the entrance to a dungeon (the dungeon is not part of this map)",
"The dungeon entrance node must be at least two nodes distant from a 'town' node"
]""",
    "user_prompt": """Create a map of an original small city and surrounding area in a Tolkein-esque fantasy world.
Use the following setting information:
{}
"""
  },
  "build_town_map": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Output a JSON object that describes a town map",
"Output format": "1. A list called 'nodes' with elements that follow the node format
2. a string called 'gate_direction' that notes at which edge of the map (north, east, west, south) the gate is located",
"node format": "{{"unique_id": "string, a unique ID for each map node",
"name": "string, the name of this node",
"type": "string, the type of this node (see rules)",
"description": "string, a brief one or two sentence description of the node",
"connections": "a list of connections (see connection format)"}}",
"connection format": "{{"connect_id": "A reference to the unique_id of the connecting node",
"connect_name": "A reference to the name of the connecting node",
"how": "A description of how this node connects to the other node.
For town areas this can be roads and paths.",
"direction": "the general direction of the connection"}}",
"Rules": ["Node type must be the following:
'town' - outdoor areas that are within town",
"There should be 4 to 6 town nodes",
"Every node must have at least one connection",
"If there is a connection from node A to node B then there must also be a corresponding connection from node B to node A",
"It must be possible to go from any node in this map to any other by following connections",
"Town nodes can include things like outdoor markets, town squares, major streets, landmarks, etc.",
"There must be exactly one city gate node at an edge of the map with unique_id 'city_gate'",
"Make note of the direction (north, east, west, south) the city gate node is located at",
"The city is enclosed by walls and only the gate leads outside of the city"
]""",
    "user_prompt": """Create a map of an original small city or town in a Tolkein-esque fantasy world.
Use the following setting information:
{}
"""
  },
  "build_field_map": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Output a JSON object that describes a field map",
"Output format": "A list called 'nodes' with elements that follow the node format",
"node format": "{{"unique_id": "string, a unique ID for each map node",
"name": "string, the name of this node",
"type": "string, the type of this node (see rules)",
"description": "string, a brief one or two sentence description of the node",
"connections": "a list of connections (see connection format)"}}",
"connection format": "{{"connect_id": "A reference to the unique_id of the connecting node",
"connect_name": "A reference to the name of the connecting node",
"how": "A description of how this node connects to the other node.
For field areas this can be roads and paths.",
"direction": "the general direction of the connection"}}",
"Rules": ["Node type must be the following:
field' - outdoor areas that are outside of town",
"There should be 5 to 8 'field' nodes",
"Every node must have at least one connection",
"If there is a connection from node A to node B then there must also be a corresponding connection from node B to node A",
"It must be possible to go from any node in this map to any other by following connections",
"Field' nodes can include things like lakes, rivers, forests, mountains, etc.",
"There must be exactly one node with unique_id 'city_outskirts' that marks the outskirts of the city (the city is not part of this map)",
"There must be exactly one node with unique_id 'field_to_dungeon' that marks the entrance to a dungeon (the dungeon is not part of this map)",
"Start from the city entrance and build towards the dungeon entrance generally heading {}"
]""",
    "user_prompt": """Create a map of an outdoor area that neighbors a city or town in a Tolkein-esque fantasy world.
Use the following setting information:
{}
"""
  },
  "add_indoor_areas": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Given the existing map, output a JSON object that adds additional indoor areas",
"Output format": "A list called 'nodes' with elements that follow the node format",
"node format": "{{"unique_id": "string, a unique ID for each map node",
"name": "string, the name of this node",
"type": "string, the type of this node (see rules)",
"description": "string, a brief one or two sentence description of the node",
"connections": "a list of connections (see connection format)"}}",
"connection format": "{{"connect_id": "A reference to the unique_id of the connecting node",
"connect_name": "A reference to the name of the connecting node",
"how": "A description of how to get from this node to the connecting node.
When going from indoor to town areas there should be some sort of exit to the street.
Between indoor areas there should be a door or passageway.",
"direction": "The general direction of the connection. Between indoor nodes this can also include stairs up and down"}}"
"Rules": ["New nodes that are added must be of the type:
'indoor' - interiors of buildings",
"There should be 4 to 6 indoor nodes added",
"Indoor nodes can include things like taverns, blacksmiths, inns, guilds, storage rooms, etc.",
"Indoor nodes can only connect to town nodes or to each other but the latter is less common",
"If there is a connection between two indoor nodes it must exist in both directions",
"There does not have to be only one connection in a given direction"
]""",
    "user_prompt": """Given the existing map of a Tolkein-esque fantasy world, add new nodes to represent indoor areas.
Existing map:
{}

Use the following setting information:
{}"""
  },
  "connect_indoor_areas": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Given the existing map and the indoor node, output a JSON object that adds a reciprocal connection",
"Output format": "A list called 'connections' with elements that follow the connection format",
"connection format": "{{"connect_id": "A reference to the unique_id of indoor node being connected to",
"connect_name": "A reference to the name of the indoor node being connected to",
"how": "Create a description of how to get from the town node to the indoor node being connected to.
Should describe doors, entranceways, etc.",
"direction": "The general direction of the connection."
"reference_id": "The unique_id of the town node of the existing map that the connection is coming from",
}}"
"Rules": ["If there is a connection from the indoor node to a town node then add a corresponding connection from that town node to the indoor node",
"There does not have to be only one connection in a given direction",
"The 'how' for this connection should be an original description",
"Only output the new connections",
"If there is no connection from the indoor node to a town node then just return an empty list"
]""",
    "user_prompt": """Given the existing map and the list of indoor nodes, fix the connections so they are reciprocated.
Existing map:
{}

Indoor node:
{}"""
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
"It must be possible to go from any node in this map to any other by following connections",
"There must be exactly one starting dungeon node with unique_id 'first_dungeon_node'",
"There must also be exactly one dungeon boss node with unique_id 'dungeon_boss'",
]""",
    "user_prompt": """Create a map of a small underground dungeon in a Tolkein-esque fantasy world.
Create a dungeon suitable for the dungeon boss:
{}

Use the following setting information:
{}
"""
  },
  "connect_map": {
    "system_prompt": """"Role": "You are building a map for a text adventure game world",
"Task": "Given the two existing maps, output a JSON object that creates connections between:
1. the node with unique_id '{0}'
2. the node with unique_id '{1}'",
"Output format": "Output a list called 'connections' that follows the format of connections in the existing maps",
"Rules": ["There should be exactly two connections in the list",
"The connection from '{0}' to '{1}' is first",
"The connection from '{1}' to '{0}' is second"
"'connect_id' refers to the node that is being connected to"
]""",
    "user_prompt": """first map:
{}

second map:
{}"""
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
6. level - an integer between 1 and 10 that represents the character's level, though higher levels should be less common
7. physical_description - a one or two sentence description of what the character looks like
8. personality - a one or two sentence description of this character's personality
9. location_id - the unique_id of the node where the character is currently located
10. relationships - optional, a list describing this character's relationships with other characters.  Has the following fields:
  1. relation_id - a reference to the unique_id of the character they have a relationship with
  2. relationship - the nature of their relationship, i.e. 'lover', 'father', 'mother', 'son', 'daughter', etc.  Make sure the reciprocal relationship also exists.

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
"relationship_status": "Married, dating someone, single, not interested, etc."
}}""",
    "user_prompt": """setting_info = {}

character_info = {}"""
  },
  "character_backstory": {
    "system_prompt": """You are describing the backstory of characters in a game world.
Based on the data in the content write a backstory for this character
Make sure their experiences are appropriate for their level.
A level 1 character would still be inexperienced, level 5 would be fairly experienced, and level 10 would be an expert in their field.""",
    "user_prompt": """setting_info = {}

character_info = {}"""
  }
}
