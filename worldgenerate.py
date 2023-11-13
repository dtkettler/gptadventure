import json
import gpt
from prompts import prompts


gpt_control = gpt.GPT()

city_name = input("Enter a name for the main city in this setting: ")

good_setting = False
while not good_setting:
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

town_map = gpt_control.run_gpt(prompts["build_town_map"]["system_prompt"], prompts["build_town_map"]["user_prompt"].format(setting),
                               temperature=0.8, force_long=True, json=True)
print(town_map)
town_map_json = json.loads(town_map)

indoor_map = gpt_control.run_gpt(prompts["add_indoor_areas"]["system_prompt"],
                                 prompts["add_indoor_areas"]["user_prompt"].format(town_map, setting),
                                 temperature=0.8, json=True)

print(indoor_map)
indoor_map_json = json.loads(indoor_map)

for indoor_node in indoor_map_json["nodes"]:
    fixed_connections = gpt_control.run_gpt(prompts["connect_indoor_areas"]["system_prompt"],
                                            prompts["connect_indoor_areas"]["user_prompt"].format(town_map, json.dumps(indoor_node)),
                                            temperature=0.5, json=True)
    print(fixed_connections)
    fixed_connections_json = json.loads(fixed_connections)

    for new_connection in fixed_connections_json["connections"]:
        for town_node in town_map_json["nodes"]:
            if town_node["unique_id"] == new_connection["reference_id"]:
                town_node["connections"].append({"connect_id": new_connection["connect_id"],
                                                 "connect_name": new_connection["connect_name"],
                                                 "how": new_connection["how"],
                                                 "direction": new_connection["direction"]})

for node in indoor_map_json["nodes"]:
    town_map_json["nodes"].append(node)

town_map = json.dumps(town_map_json, indent=2)

field_map = gpt_control.run_gpt(prompts["build_field_map"]["system_prompt"].format(town_map_json["gate_direction"]),
                                prompts["build_field_map"]["user_prompt"].format(setting),
                                temperature=0.8, force_long=True, json=True)

print(field_map)
field_map_json = json.loads(field_map)

town_field_connection = gpt_control.run_gpt(prompts["connect_map"]["system_prompt"].format("city_gate", "city_outskirts"),
                                            prompts["connect_map"]["user_prompt"].format(town_map, field_map),
                                            temperature=0.5, json=True)
print(town_field_connection)
town_field_connection_json = json.loads(town_field_connection)

for node in town_map_json["nodes"]:
    if node["unique_id"] == "city_gate":
        node["connections"].append(town_field_connection_json["connections"][0])
        break
for node in field_map_json["nodes"]:
    if node["unique_id"] == "city_outskirts":
        node["connections"].append(town_field_connection_json["connections"][1])
        break

starting_point = gpt_control.run_gpt(prompts["find_starting_point"]["system_prompt"], town_map,
                                     temperature=0.3)

print(starting_point)

dungeon_map = gpt_control.run_gpt(prompts["build_dungeon_map"]["system_prompt"],
                                  prompts["build_dungeon_map"]["user_prompt"].format(json.dumps(monsters_json["dungeon_boss"]), setting),
                                  temperature=0.8, force_long=True, json=True)
print(dungeon_map)
dungeon_map_json = json.loads(dungeon_map)

dungeon_connections = gpt_control.run_gpt(prompts["connect_map"]["system_prompt"].format("field_to_dungeon", "first_dungeon_node"),
                                          prompts["connect_map"]["user_prompt"].format(field_map, dungeon_map),
                                          temperature=0.5, json=True)

print(dungeon_connections)
dungeon_connections_json = json.loads(dungeon_connections)

for node in field_map_json["nodes"]:
    if node["unique_id"] == "field_to_dungeon":
        node["connections"].append(dungeon_connections_json["connections"][0])
        break
for node in dungeon_map_json["nodes"]:
    if node["unique_id"] == "first_dungeon_node":
        node["connections"].append(dungeon_connections_json["connections"][1])
        break

npcs = gpt_control.run_gpt(prompts["create_npcs"]["system_prompt"],
                           prompts["create_npcs"]["user_prompt"].format(town_map, setting),
                           temperature=0.8, force_long=True, json=True)

print(npcs)
npc_json = json.loads(npcs)

total_map = {"nodes": []}

for node in town_map_json["nodes"]:
    user_prompt = prompts["describe_node"]["user_prompt"].format(setting, json.dumps(node))
    description = gpt_control.run_gpt(prompts["describe_node"]["system_prompt"], user_prompt, temperature=0.7)

    print(description)
    node["detailed_description"] = description

    total_map["nodes"].append(node)

for node in field_map_json["nodes"]:
    user_prompt = prompts["describe_node"]["user_prompt"].format(setting, json.dumps(node))
    description = gpt_control.run_gpt(prompts["describe_node"]["system_prompt"], user_prompt, temperature=0.7)

    print(description)
    node["detailed_description"] = description

    total_map["nodes"].append(node)

for node in dungeon_map_json["nodes"]:
    user_prompt = prompts["describe_node"]["user_prompt"].format(setting, json.dumps(node))
    description = gpt_control.run_gpt(prompts["describe_node"]["system_prompt"], user_prompt, temperature=0.7)

    print(description)
    node["detailed_description"] = description

    total_map["nodes"].append(node)

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
world["nodes"] = total_map["nodes"]
world["starting_point"] = starting_point
world["characters"] = npc_json["characters"]
world["setting"] = setting_json
world["monsters"] = monsters_json

with open(city_name + ".json", "w") as f:
    f.write(json.dumps(world, indent=2))

