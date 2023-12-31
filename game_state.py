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
        self.quests = []
        self.quest_count = 0

    def get_location_info(self):
        companions = []
        companion_ids = []
        for companion in self.companions:
            companions.append({"unique_id": companion["unique_id"],
                               "name": companion["name"],
                               "race": companion["race"],
                               "gender": companion["gender"],
                               "profession": companion["profession"],
                               "clothes": companion["clothes"],
                               "height": companion["height"],
                               "hair": companion["hair"],
                               "eyes": companion["eyes"],
                               "build": companion["build"],
                               "equipment": companion["equipment"]
                               })
            companion_ids.append(companion["unique_id"])

        characters = []
        for character in self.world["characters"]:
            if character["location_id"] == self.current_node["unique_id"] and character["unique_id"] not in companion_ids:
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

        for quest in self.quests:
            if quest["giver_location"] == self.current_node["unique_id"]:
                characters.append(quest["npc"])

        this_json = {"location": self.current_node}
        if companions:
            this_json["party_members"] = companions
        if characters:
            this_json["characters_present"] = characters
        if self.present_monsters:
            this_json["monster_groups"] = self.present_monsters

        return this_json

    def get_monsters(self):
        return self.world["monsters"]

    def get_setting(self):
        return self.world["setting"]

    def get_map(self, short=True):
        if short:
            nodes = []
            for node in self.world["nodes"]:
                # Include everything but detailed_description
                nodes.append({"unique_id": node["unique_id"],
                              "name": node["name"],
                              "type": node["type"],
                              "description": node["description"],
                              "connections": node["connections"]})

            return nodes
        else:
            return self.world["nodes"]

    def get_boss_info(self):
        return self.world["monsters"]["dungeon_boss"]

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
        if "rounds_since_fatigue_change" not in self.player:
            self.player["rounds_since_fatigue_change"] = 0

        return self.player

    def set_player(self, player):
        self.player = player

    def set_present_monsters(self, monsters):
        self.present_monsters = monsters

    def get_present_monsters(self):
        return self.present_monsters

    def get_companions(self):
        data_out = []
        for companion in self.companions:
            if "fatigue" not in companion:
                companion["fatigue"] = "none"
            if "injuries" not in companion:
                companion["injuries"] = "none"
            if "rounds_since_fatigue_change" not in companion:
                companion["rounds_since_fatigue_change"] = 0

            data_out.append({"unique_id": companion["unique_id"],
                             "name": companion["name"],
                             "race": companion["race"],
                             "gender": companion["gender"],
                             "profession": companion["profession"],
                             "level": companion["level"],
                             "physical_description": companion["physical_description"],
                             "clothes": companion["clothes"],
                             "height": companion["height"],
                             "hair": companion["hair"],
                             "eyes": companion["eyes"],
                             "build": companion["build"],
                             "equipment": companion["equipment"],
                             "personality": companion["personality"],
                             "fatigue": companion["fatigue"],
                             "injuries": companion["injuries"],
                             "rounds_since_fatigue_change": companion["rounds_since_fatigue_change"]
                             })

        return data_out

    def get_num_quests(self):
        if not self.quests:
            return 0
        else:
            return len(self.quests)

    def get_accepted_quests(self):
        out = []
        for quest in self.quests:
            if quest["status"] == "accepted" or quest["status"] == "complete":
                out.append(quest)

        return out

    def get_urgent_quests_at_location(self):
        out = []
        for quest in self.quests:
            if quest["giver_location"] == self.current_node["unique_id"] and quest["urgency"] == "urgent":
                out.append(quest)

        return out

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
        old_node_id = self.current_node["unique_id"]

        new_node = None
        for node in self.world["nodes"]:
            if node["unique_id"] == connect_id:
                self.current_node = node
                new_node = node
                break

        # as a fallback check by name too
        if not new_node:
            for node in self.world["nodes"]:
                if node["name"] == connect_id:
                    self.current_node = node
                    new_node = node
                    break

        # if it still hasn't been found then something is wrong
        if not new_node:
            print("Sorry I could not find that location")
            return []

        for companion in self.companions:
            companion["location_id"] = new_node["unique_id"]

        monsters = None
        if new_node["type"] == "field" or new_node["type"] == "dungeon":
            monsters = self.check_for_monsters(new_node, old_node_id)

        return monsters

    def check_for_monsters(self, node, old_node_id):
        monsters = []
        for connection in node["connections"]:
            if connection["connect_id"] != "city_gate" and connection["connect_id"] != old_node_id:
                ran = random.random()
                if ran < 0.5:
                    monsters.append(connection["connect_id"])

        return monsters

    def check_for_level_up(self, monster_levels):
        if "kills_since_level_up" not in self.player:
            self.player["kills_since_level_up"] = 0
        for monster_level in monster_levels:
            level_odds = (10.0 * (monster_level - self.player["level"] + 1) + 5.0 * self.player["kills_since_level_up"]) / 100.0
            ran = random.random()
            if ran < level_odds:
                print("You leveled up!")
                self.player["level"] = self.player["level"] + 1
                self.player["kills_since_level_up"] = 0
                return True
            else:
                self.player["kills_since_level_up"] = self.player["kills_since_level_up"] + 1
        return False

    def clear_monsters(self, target_id):
        new_monsters = []
        for group in self.present_monsters:
            if group["connect_id"] != target_id:
                new_monsters.append(group)

        self.present_monsters = new_monsters

    def rest(self):
        self.player["fatigue"] = "none"
        self.player["injuries"] = "none"
        self.player["rounds_since_fatigue_change"] = 0

        for companion in self.companions:
            companion["fatigue"] = "none"
            companion["injuries"] = "none"
            companion["rounds_since_fatigue_change"] = 0

    def character_is_npc(self, target):
        for character in self.world["characters"]:
            if character["unique_id"] == target or character["name"] == target:
                return True

        return False

    def character_is_quest_giver(self, target):
        for quest in self.quests:
            if quest["npc"]["unique_id"] == target:
                return True

        return False

    def get_quests_overview(self):
        out = []
        for quest in self.quests:
            out.append({"quest_id": quest["quest_id"],
                        "quest_giver": quest["quest_giver"],
                        "giver_location": quest["giver_location"],
                        "urgency": quest["urgency"],
                        "type": quest["type"],
                        "target": quest["target"],
                        "location": quest["location"],
                        "base_reward": quest["base_reward"],
                        "short_description": quest["short_description"]})

    def get_quest_from_char(self, target):
        for quest in self.quests:
            if quest["npc"]["unique_id"] == target:
                return quest

        return None

    def add_skill(self, skill):
        self.player["skills"].append(skill)

    def add_quest(self, quest):
        if not self.quests:
            self.quests = [quest]
        else:
            self.quests.append(quest)

    def accept_quest(self, quest_id, agreed_reward):
        for quest in self.quests:
            if quest["quest_id"] == quest_id:
                quest["status"] = "accepted"
                quest["reward"] = agreed_reward

    def get_quest_counter(self):
        self.quest_count += 1
        return self.quest_count
