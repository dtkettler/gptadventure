import json
import sys
import pickle

import gpt
from gameplay_prompts import prompts
from game_state import State
from combat import go_through_attacks


class Game:
    def __init__(self, gpt_control):
        self.gpt_control = gpt_control
        self.state = None

    def new_game(self):
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

        self.state = State(world)
        self.create_character()

    def load_game(self):
        good_file = False
        while not good_file:
            filename = input("Enter filename: ")
            try:
                with open(filename, 'rb') as f:
                    self.state = pickle.load(f)
                good_file = True
            except Exception as e:
                print(e)

    def save_game(self):
        good_file = False
        while not good_file:
            filename = input("Enter filename to save game to: ")
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(self.state, f)
                good_file = True
            except Exception as e:
                print(e)

    def create_character(self):
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

            char_check = self.gpt_control.run_gpt(prompts["character_check"]["system_prompt"],
                                                  prompts["character_check"]["user_prompt"].format(self.state.get_setting(),
                                                                                                   json.dumps(character)),
                                                  temperature=0.2, json=True)

            char_check_json = json.loads(char_check)
            print(char_check_json["message"])
            if char_check_json["accept_character"]:
                good_character = True

        character["level"] = 1

        accept_equipment = False
        while not accept_equipment:
            char_stats = self.gpt_control.run_gpt(prompts["player_starting"]["system_prompt"],
                                                  prompts["player_starting"]["user_prompt"].format(self.state.get_setting(),
                                                                                                   json.dumps(character)),
                                                  temperature=0.7, json=True)
            print(char_stats)
            yn = input("Do the equipment and skills look acceptable? (Y/N) ")
            if yn.lower() == "y":
                accept_equipment = True

        character["equipment"] = json.loads(char_stats)["equipment"]
        character["skills"] = json.loads(char_stats)["skills"]
        self.state.set_player(character)

    def main(self):
        print("Welcome adventurer!")

        look = True
        playing = True
        while playing:
            if look:
                self.look_around()
            command = input("What would you like to do? ")
            look = self.interpret(command)

    def look_around(self):
        this_json = self.state.get_location_info()

        user_prompt = json.dumps(this_json)

        monsters = self.state.get_present_monsters()
        if monsters:
            user_prompt += "\n"
            for group in monsters:
                user_prompt += "A group of monsters blocks the path to {}:\n{}\n".format(group["connect_id"],
                                                                                         json.dumps(group["monsters"]))

        description = self.gpt_control.run_gpt(prompts["look_around"]["system_prompt"], user_prompt)
        print(description)

    def look_at(self, command):
        this_json = self.state.get_location_info()

        system_prompt = prompts["look_at"]["system_prompt"].format(json.dumps(this_json))

        monsters = self.state.get_present_monsters()
        if monsters:
            system_prompt += "\n"
            for group in monsters:
                system_prompt += "A group of monsters blocks the path to {}:\n{}\n".format(group["connect_id"],
                                                                                           json.dumps(group["monsters"]))

        description = self.gpt_control.run_gpt(system_prompt, command)
        print(description)

    def interpret(self, command):
        location_info = json.dumps(self.state.get_location_info())
        prompt = prompts["interpret_command"]["system_prompt"].format(location_info)

        output = self.gpt_control.run_gpt(prompt, command, temperature=0.3, json=True)
        # print(output)
        output_json = json.loads(output)
        print(output_json["description"])

        if "command" not in output_json:
            return False
        if output_json["command"] == "exit_game":
            sys.exit()
        elif output_json["command"] == "save_game":
            self.save_game()
            return False
        elif output_json["command"] == "status":
            self.display_status()
            return False
        elif output_json["command"] == "look_around":
            return True
        elif output_json["command"] == "look_at" and output_json["success"]:
            self.look_at(command)
            return False
        elif output_json["command"] == "move" and output_json["success"]:
            # Really this should be handled by the prompt but I'm finding it unreliable
            for monster_group in self.state.get_present_monsters():
                if monster_group["connect_id"] == output_json["target"]:
                    print("The path is blocked by monsters")
                    return False

            monsters = self.state.update_current_location(output_json["target"])
            if monsters:
                self.spawn_monsters(monsters)
            else:
                self.state.set_present_monsters([])
            return True
        elif output_json["command"] == "talk" and output_json["success"]:
            self.talk_to(output_json["target"])
            return True
        elif output_json["command"] == "invite" and output_json["success"]:
            self.invite(output_json["target"])
            return False
        elif output_json["command"] == "fight" and output_json["success"]:
            self.do_battle(output_json["target"])
            return True
        elif output_json["command"] == "rest" and output_json["success"]:
            self.state.rest()
            print("You rent a room and rest at the inn")
            return True
        elif not output_json["success"]:
            return False
        elif output_json["command"] == "unknown":
            return False

    def talk_to(self, target):
        character = self.state.get_character(target)

        # print("You approach {}".format(character["name"]))
        dialogue = True
        while dialogue:
            command = input("What would you like to say? ")

            attitude = self.state.get_character_attitude(character["unique_id"])

            response = self.gpt_control.run_gpt_with_history(prompts["talk_to"]["system_prompt"].format(attitude,
                                                                                                        json.dumps(character)),
                                                             command, self.state.get_character_history(character),
                                                             functions=[prompts["talk_to"]["function"]])
            self.state.update_character_history(character, command, response["message"])
            self.state.update_character_friendship(character["unique_id"], response["friendship_change"])

            print(response["message"])
            if response["finish"]:
                dialogue = False

    def invite(self, target):
        character = self.state.get_character(target)
        attitude = self.state.get_character_attitude(character["unique_id"])

        response = self.gpt_control.run_gpt_with_history(
            prompts["invite"]["system_prompt"].format(attitude, json.dumps(character)),
            prompts["invite"]["user_prompt"], self.state.get_character_history(character),
            functions=[prompts["invite"]["function"]])

        print(response["message"])
        if response["accept"]:
            self.state.add_companion(target)

    def spawn_monsters(self, monster_spawns):
        location_info = self.state.get_location_info()

        if location_info["location"]["type"] == "field":
            min_level = "1"
            max_level = "3"
            setting_monsters = self.state.get_monsters()["field_monsters"]
        elif location_info["type"] == "dungeon":
            min_level = "4"
            max_level = "8"
            setting_monsters = self.state.get_monsters()["dungeon_monsters"]
        else:
            self.state.set_present_monsters([])
            return

        system_prompt = prompts["spawn_monsters"]["system_prompt"].format(min_level, max_level, setting_monsters,
                                                                          json.dumps(location_info))

        all_monsters = []
        for monster_spawn in monster_spawns:
            user_prompt = prompts["spawn_monsters"]["user_prompt"].format(monster_spawn)
            monster_output = self.gpt_control.run_gpt(system_prompt, user_prompt, temperature=0.8, json=True)

            monster_json = json.loads(monster_output)
            for monster in monster_json["monsters"]:
                for reference_monster in setting_monsters:
                    if reference_monster["name"] == monster["type"]:
                        monster["description"] = reference_monster["description"]
                        if "resistances" in reference_monster:
                            monster["resistances"] = reference_monster["resistances"]
                        if "weaknesses" in reference_monster:
                            monster["weaknesses"] = reference_monster["weaknesses"]
            all_monsters.append({"connect_id": monster_spawn, "monsters": monster_json["monsters"]})

        #print(all_monsters)
        print("There are monsters here")
        self.state.set_present_monsters(all_monsters)

    def spawn_boss_monster(self):
        other_monsters = self.state.get_present_monsters()
        boss_stats = self.state.get_boss_info()

        boss_stats["unique_id"] = "dungeon_boss"
        boss_stats["type"] = boss_stats["name"]
        boss_stats["level"] = 12
        boss_stats["descriptor"] = "Boss"

        other_monsters.append({"connect_id": "center_of_room", "monsters": [boss_stats]})
        self.state.set_present_monsters(other_monsters)

    def do_battle(self, target):
        for monster_group in self.state.get_present_monsters():
            if monster_group["connect_id"] == target:
                monster_levels = []
                for monster in monster_group["monsters"]:
                    monster["rounds_attacked"] = 0
                    monster_levels.append(monster["level"])
                fled = go_through_attacks(self.gpt_control, self.state.get_player_status(), self.state.get_companions(),
                                          monster_group["monsters"])
                if not fled:
                    self.leveling(monster_levels)
                    self.state.clear_monsters(target)
                break

    def leveling(self, monster_levels):
        leveled = self.state.check_for_level_up(monster_levels)
        if leveled:
            status = self.state.get_player_status()
            new_skill = self.gpt_control.run_gpt(prompts["level_up_skill"]["system_prompt"].format(json.dumps(status)),
                                                 prompts["level_up_skill"]["user_prompt"].format(status["level"]),
                                                 temperature=0.8, json=True)
            new_skill = json.loads(new_skill)
            print("You learned {}!".format(new_skill['name']))
            self.state.add_skill(new_skill)

    def display_status(self):
        player = self.state.get_player_status()

        print("Name: {}".format(player["name"]))
        print("Class: {}".format(player["class"]))
        print("Level: {}".format(player["level"]))
        print("Fatigue: {}".format(player["fatigue"]))
        print("Injuries: {}".format(player["injuries"]))
        print("Skills: {}".format(", ".join([skill['name'] for skill in player["skills"]])))
        print("Equipment: {}".format(", ".join(player["equipment"])))
        print("Inventory: {}".format(", ".join(player["inventory"])))


def game_start():
    gpt_control = gpt.GPT()

    good_response = False
    while not good_response:
        newload = input("(N)ew game or (l)oad existing? (N/L) ")

        newload = newload.lower()
        if newload == "n" or newload == "l":
            good_response = True

    game = Game(gpt_control)
    if newload == "n":
        game.new_game()
    elif newload == "l":
        game.load_game()

    game.main()


if __name__ == "__main__":
    game_start()
