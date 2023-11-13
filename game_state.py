import random


class State():
    def __init__(self, world):
        self.world = world
        for node in world["nodes"]:
            if str(node["unique_id"]) == world["starting_point"]:
                self.current_node = node
                break

        self.conversations = {}
        self.player = None
        self.companions = []
        self.present_monsters = []

    def get_location_info(self):
        characters = []
        for character in self.world["characters"]:
            if character["location_id"] == self.current_node["unique_id"]:
                #characters.append(character)
                characters.append({"unique_id": character["unique_id"],
                                   "name": character["name"],
                                   "race": character["race"],
                                   "gender": character["gender"],
                                   "profession": character["profession"],
                                   "physical_description": character["physical_description"],
                                   "clothes": character["clothes"],
                                   "height": character["height"],
                                   "hair": character["hair"],
                                   "eyes": character["eyes"],
                                   "build": character["build"]
                                   })

        this_json = {"location": self.current_node, "characters_present": characters}
        return this_json

    def get_monsters(self):
        return self.world["monsters"]

    def get_setting(self):
        return self.world["setting"]

    def get_character_attitude(self, target):
        for character in self.world["characters"]:
            if character["unique_id"] == target or character["name"] == target:
                self.update_character_friendship(target, 0.0)

                if character["friendship_level"] <= -7.0:
                    attitude = "Hatred - You actively hate the user, don't want to engage with them, and will try to end the conversation as soon as possible."
                elif character["friendship_level"] <= -5.0:
                    attitude = "Strong dislike - You actively dislike the user, don't want to engage with them, and will try to end the conversation."
                elif character["friendship_level"] <= -3.0:
                    attitude = "Dislike - You dislike the user and don't really want to talk to them but you can tolerate it to some degree."
                elif character["friendship_level"] <= -1.0:
                    attitude = "Annoying - You find the user kind of annoying and don't want to talk to them more than necessary but can stay polite."
                elif -1.0 < character["friendship_level"] < 1.0:
                    attitude = "Neutral - You don't really know the user.  You have no strong feelings about them, but probably won't talk much about personal information."
                elif character["friendship_level"] < 3.0:
                    attitude = "Acquaintance - You have positive feelings about the user but still don't know them that well. You can be friendly be still maintain some distance. "
                elif character["friendship_level"] < 5.0:
                    attitude = "Friendly - You treat the user as a friend and won't mind sharing some personal information."
                elif character["friendship_level"] < 7.0:
                    attitude = "Good friend - You consider the user to be one of your closest friends. You don't mind sharing personal information and actively want to talk to them more."
                else:
                    attitude = "Best friend or lover - You treat the user as either your best friend or possibly a romantic interest. You want to talk to them as much as possible."

                return attitude

    def get_character(self, target):
        for character in self.world["characters"]:
            if character["unique_id"] == target or character["name"] == target:
                if "friendship_level" not in character:
                    character["friendship_level"] = 0.0

                return character

        return None

    def get_character_history(self, character):
        if character["unique_id"] in self.conversations:
            return self.conversations["unique_id"]
        else:
            return []

    def get_player_status(self):
        if "fatigue" not in self.player:
            self.player["fatigue"] = "none"
        if "injuries" not in self.player:
            self.player["injuries"] = "none"
        if "inventory" not in self.player:
            self.player["inventory"] = []

        return self.player

    def set_player(self, player):
        self.player = player

    def add_companion(self, character_id):
        for character in self.world["characters"]:
            if character["unique_id"] == character_id:
                self.companions.append(character)

    def remove_companion(self, character_id):
        self.companions = []

    def update_character_history(self, character, command, response):
        if character["unique_id"] in self.conversations:
            self.conversations["unique_id"].append({"user": command, "assistant": response})
        else:
            self.conversations["unique_id"] = [{"user": command, "assistant": response}]

    def update_character_friendship(self, character_id, friendship_change):
        for character in self.world["characters"]:
            if character["unique_id"] == character_id:
                if "friendship_level" not in character:
                    character["friendship_level"] = friendship_change
                else:
                    character["friendship_level"] += friendship_change
                break

    def update_current_location(self, connect_id):
        new_node = None
        for node in self.world["nodes"]:
            if node["unique_id"] == connect_id:
                self.current_node = node
                new_node = node
                break
        for companion in self.companions:
            companion["location_id"] = new_node["unique_id"]

        monsters = None
        if new_node["type"] == "field" or new_node["type"] == "dungeon":
            monsters = self.check_for_monsters(new_node)

        return monsters

    def check_for_monsters(self, node):
        monsters = []
        for connection in node["connections"]:
            ran = random.random()
            if ran < 0.5:
                monsters.append(connection["connect_id"])

        return monsters