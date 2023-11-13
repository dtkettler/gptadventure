import json
import gpt
from prompts import prompts


gpt_control = gpt.GPT()

city_name = input("Enter a name for the main city in this setting: ")

good_setting = False
while not good_setting:
    #setting = gpt_control.run_gpt(prompts["create_setting"]["system_prompt"], prompts["create_setting"]["user_prompt"],
    #                             temperature=0.7)
    setting = gpt_control.run_gpt(prompts["create_setting"]["system_prompt"],
                                  prompts["create_setting"]["user_prompt"].format(city_name), temperature=0.8,
                                  json=True)
    print(setting)

    response = input("Does this setting sound good? (Y/N) ")
    if response.strip().lower() == "y":
        good_setting = True

setting_json = json.loads(setting)
setting_json["city_name"] = city_name
setting = json.dumps(setting_json, indent=2)

monsters = gpt_control.run_gpt(prompts["create_monster_setting"]["system_prompt"],
                               prompts["create_monster_setting"]["user_prompt"].format(setting), temperature=0.8,
                               json=True)

print(monsters)
monsters_json = json.loads(monsters)

map = gpt_control.run_gpt(prompts["build_map2"]["system_prompt"], prompts["build_map"]["user_prompt"].format(setting),
                                 temperature=0.8, force_long=True, json=True)
print(map)

map_json = json.loads(map)

starting_point = gpt_control.run_gpt(prompts["find_starting_point"]["system_prompt"], map,
                                     temperature=0.3)

print(starting_point)

map_with_indoor = gpt_control.run_gpt(prompts["add_indoor_areas"]["system_prompt"],
                                      prompts["add_indoor_areas"]["user_prompt"].format(map, setting),
                                      temperature=0.8, json=True)

print(map_with_indoor)

fixed_nodes = gpt_control.run_gpt(prompts["connect_indoor_areas"]["system_prompt"],
                                  prompts["connect_indoor_areas"]["user_prompt"].format(map, map_with_indoor),
                                  temperature=0.3, json=True)

print(fixed_nodes)

indoor_json = json.loads(map_with_indoor)
fixed_nodes_json = json.loads(fixed_nodes)

new_map = {"nodes": []}

for original_node in map_json["nodes"]:
    for new_node in fixed_nodes_json["nodes"]:
        if new_node["unique_id"] == original_node["unique_id"]:
            for new_connection in new_node["connections"]:
                original_node["connections"].append(new_connection)
            break

    new_map["nodes"].append(original_node)

for node in indoor_json["nodes"]:
    new_map["nodes"].append(node)

map = json.dumps(new_map, indent=2)

print(map)

dungeon_map = gpt_control.run_gpt(prompts["build_dungeon_map"]["system_prompt"],
                                  prompts["build_dungeon_map"]["user_prompt"].format(json.dumps(monsters_json["dungeon_boss"]), setting),
                                 temperature=0.8, force_long=True, json=True)
print(dungeon_map)

dungeon_map_json = json.loads(dungeon_map)

#npcs = gpt_control.run_gpt(prompts["create_npcs"]["system_prompt"],
#                           prompts["create_npcs"]["user_prompt"].format(map, setting),
#                           temperature=0.8, force_long=True, json=True)
#
#print(npcs)
#npc_json = json.loads(npcs)

dungeon_connections = gpt_control.run_gpt(prompts["connect_dungeon"]["system_prompt"],
                                          prompts["connect_dungeon"]["user_prompt"].format(map, dungeon_map),
                                          temperature=0.5, json=True)

print(dungeon_connections)

dungeon_connections_json = json.loads(dungeon_connections)
for node in new_map["nodes"]:
    if node["unique_id"] == "field_to_dungeon":
        node["connections"].append(dungeon_connections_json["connections"][0])
        break
for node in dungeon_map_json["nodes"]:
    if node["unique_id"] == "first_dungeon_node":
        node["connections"].append(dungeon_connections_json["connections"][1])
        break

for node in new_map["nodes"]:
    user_prompt = prompts["describe_node"]["user_prompt"].format(setting, json.dumps(node))
    description = gpt_control.run_gpt(prompts["describe_node"]["system_prompt"], user_prompt, temperature=0.7)

    print(description)
    node["detailed_description"] = description

for node in dungeon_map_json["nodes"]:
    user_prompt = prompts["describe_node"]["user_prompt"].format(setting, json.dumps(node))
    description = gpt_control.run_gpt(prompts["describe_node"]["system_prompt"], user_prompt, temperature=0.7)

    print(description)
    node["detailed_description"] = description

    new_map["nodes"].append(node)

for npc in npc_json["characters"]:
    user_prompt = prompts["character_details"]["user_prompt"].format(setting, json.dumps(npc))
    character_details = gpt_control.run_gpt(prompts["character_details"]["system_prompt"], user_prompt, temperature=0.8,
                                            force_long=True, json=True)

    print(character_details)
    character_details_json = json.loads(character_details)

    npc["clothes"] = character_details_json["clothes"]
    npc["height"] = character_details_json["height"]
    npc["hair"] = character_details_json["hair"]
    npc["eyes"] = character_details_json["eyes"]
    npc["build"] = character_details_json["build"]
    npc["equipment"] = character_details_json["equipment"]
    npc["hobby"] = character_details_json["hobby"]
    npc["likes"] = character_details_json["likes"]
    npc["dislikes"] = character_details_json["dislikes"]
    npc["relationship_status"] = character_details_json["relationship_status"]

    backstory = gpt_control.run_gpt(prompts["character_backstory"]["system_prompt"], user_prompt, temperature=0.8)

    print(backstory)
    npc["backstory"] = backstory

world = {}
world["nodes"] = new_map["nodes"]
world["starting_point"] = starting_point
world["characters"] = npc_json["characters"]
world["setting"] = setting_json
world["monsters"] = monsters_json

with open(city_name + ".json", "w") as f:
    f.write(json.dumps(world, indent=2))

