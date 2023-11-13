import json
import sys
import pickle

import gpt
from prompts import prompts
from game_state import State


def look_around(gpt_control, state):
    this_json = state.get_location_info()

    user_prompt = json.dumps(this_json)

    description = gpt_control.run_gpt(prompts["look_around"]["system_prompt"], user_prompt)
    print(description)

def look_at(gpt_control, state, command):
    this_json = state.get_location_info()

    system_prompt = prompts["look_at"]["system_prompt"].format(json.dumps(this_json))

    description = gpt_control.run_gpt(system_prompt, command)
    print(description)

def talk_to(gpt_control, state, target):
    character = state.get_character(target)

    #print("You approach {}".format(character["name"]))
    dialogue = True
    while dialogue:
        command = input("What would you like to say? ")

        attitude = state.get_character_attitude(character["unique_id"])

        response = gpt_control.run_gpt_with_history(prompts["talk_to"]["system_prompt"].format(attitude,
                                                                                               json.dumps(character)),
                                                    command, state.get_character_history(character),
                                                    functions=[prompts["talk_to"]["function"]])
        state.update_character_history(character, command, response["message"])
        state.update_character_friendship(character["unique_id"], response["friendship_change"])

        print(response["message"])
        if response["finish"]:
            dialogue = False

def invite(gpt_control, state, target):
    character = state.get_character(target)
    attitude = state.get_character_attitude(character["unique_id"])

    response = gpt_control.run_gpt_with_history(prompts["invite"]["system_prompt"].format(attitude, json.dumps(character)),
                                                prompts["invite"]["user_prompt"], state.get_character_history(character),
                                                functions=[prompts["invite"]["function"]])

    print(response["message"])
    if response["accept"]:
        state.add_companion(target)

def load_game():
    good_file = False
    while not good_file:
        filename = input("Enter filename: ")
        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
            good_file = True
        except Exception as e:
            print(e)
    return state

def save_game(state):
    good_file = False
    while not good_file:
        filename = input("Enter filename to save game to: ")
        try:
            with open(filename, 'wb') as f:
                pickle.dump(state, f)
            good_file = True
        except Exception as e:
            print(e)

def display_status(state):
    player = state.get_player_status()

    print("Name: {}".format(player["name"]))
    print("Class: {}".format(player["class"]))
    print("Fatigue: {}".format(player["fatigue"]))
    print("Injuries: {}".format(player["injuries"]))
    print("Equipment: {}".format(", ".join(player["equipment"])))
    print("Inventory: {}".format(", ".join(player["inventory"])))

def interpret(gpt_control, state, command):
    location_info = json.dumps(state.get_location_info())
    prompt = prompts["interpret_command"]["system_prompt"].format(location_info)

    output = gpt_control.run_gpt(prompt, command, temperature=0.3, json=True)
    #print(output)
    output_json = json.loads(output)
    print(output_json["description"])

    if "command" not in output_json:
        return False
    if output_json["command"] == "exit_game":
        sys.exit()
    elif output_json["command"] == "save_game":
        save_game(state)
        return False
    elif output_json["command"] == "status":
        display_status(state)
        return False
    elif output_json["command"] == "look_around":
        return True
    elif output_json["command"] == "look_at" and output_json["success"]:
        look_at(gpt_control, state, command)
        return False
    elif output_json["command"] == "move" and output_json["success"]:
        state.update_current_location(output_json["target"])
        return True
    elif output_json["command"] == "talk" and output_json["success"]:
        talk_to(gpt_control, state, output_json["target"])
        return True
    elif output_json["command"] == "invite" and output_json["success"]:
        invite(gpt_control, state, output_json["target"])
        return False
    elif not output_json["success"]:
        return False
    elif output_json["command"] == "unknown":
        return False

def main(gpt_control, state):
    print("Welcome adventurer!")

    look = True
    playing = True
    while playing:
        if look:
            look_around(gpt_control, state)
        command = input("What would you like to do? ")
        look = interpret(gpt_control, state, command)

def create_character(gpt_control, state):
    good_character = False
    while not good_character:
        char_name = input("Enter your character's name: ")
        char_class = input("Enter your character's class: ")
        char_race = input("Enter your character's race: ")
        char_gender = input("Enter your character's gender: ")
        char_description = input("Enter a short description of your character: ")

        character = {"name": char_name,
                     "class": char_class,
                     "race": char_race,
                     "gender": char_gender,
                     "description": char_description}

        char_check = gpt_control.run_gpt(prompts["character_check"]["system_prompt"],
                                         prompts["character_check"]["user_prompt"].format(state.get_setting(), json.dumps(character)),
                                         temperature=0.2, json=True)

        char_check_json = json.loads(char_check)
        print(char_check_json["message"])
        if char_check_json["accept_character"]:
            good_character = True

    character["level"] = 1

    accept_equipment = False
    while not accept_equipment:
        char_stats = gpt_control.run_gpt(prompts["player_starting"]["system_prompt"],
                                         prompts["player_starting"]["user_prompt"].format(state.get_setting(), json.dumps(character)),
                                         temperature=0.7, json=True)
        print(char_stats)
        yn = input("Do the equipment and skills look acceptable? (Y/N) ")
        if yn.lower() == "y":
            accept_equipment = True

    character["equipment"] = json.loads(char_stats)["equipment"]
    character["skills"] = json.loads(char_stats)["skills"]
    state.set_player(character)

def game_start():
    gpt_control = gpt.GPT()

    good_response = False
    while not good_response:
        newload = input("(N)ew game or (l)oad existing? (N/L) ")

        newload = newload.lower()
        if newload == "n" or newload == "l":
            good_response = True

    if newload == "n":
        good_file = False
        while not good_file:
            filename = input("Enter filename for world data: ")
            try:
                with open(filename) as f:
                    world = json.load(f)
                good_file = True
            except Exception as e:
                print("Error loading file")
                print(e)

        state = State(world)
        create_character(gpt_control, state)

    elif newload == "l":
        state = load_game()

    main(gpt_control, state)


if __name__ == "__main__":
    game_start()
