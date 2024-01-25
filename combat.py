import json
import sys
import random

from gameplay_prompts import prompts

def calculate_character_attack_prob(character, enemy):
    prob = 30.0 + (character["level"] - enemy["level"]) * 10.0 + 10.0 * enemy["rounds_attacked"]

    if character["fatigue"] == "slight":
        prob = prob * 0.9
    elif character["fatigue"] == "moderate":
        prob = prob * 0.7
    elif character["fatigue"] == "severe":
        prob = prob * 0.5

    if character["injuries"] == "slight":
        prob = prob * 0.9
    elif character["injuries"] == "moderate":
        prob = prob * 0.7
    elif character["injuries"] == "severe":
        prob = prob * 0.5

    if prob < 0:
        prob = 0.0
    elif prob > 100:
        prob = 100.0

    return prob

def calculate_enemy_attack_prob(enemy, character):
    injury_prob = (enemy["level"] - character["level"] + 1) * 10.0

    if character["fatigue"] == "moderate":
        injury_prob *= 1.2
    elif character["fatigue"] == "severe":
        injury_prob *= 1.5

    if injury_prob < 0:
        injury_prob = 0.0
    elif injury_prob > 100:
        injury_prob = 100.0

    if character["injuries"] == "none":
        defeat_prob = 0.0
    elif character["injuries"] == "slight":
        defeat_prob = (enemy["level"] - character["level"]) * 2.0
    elif character["injuries"] == "moderate":
        defeat_prob = (enemy["level"] - character["level"]) * 5.0
    elif character["injuries"] == "severe":
        defeat_prob = (enemy["level"] - character["level"]) * 15.0

    return injury_prob, defeat_prob

def calculate_character_fatigue_prob(character):
    return character["rounds_since_fatigue_change"] * 5.0

def calculate_flee_prob(player):
    prob = 80.0

    return prob

def calculate_probabilities(player, companions, enemies):
    attackers_probs = []
    for enemy in enemies:
        attackers_probs.append({"attacker_id": "user", "attack_target_id": enemy["unique_id"],
                                "defeat_probability": calculate_character_attack_prob(player, enemy)})

    for companion in companions:
        for enemy in enemies:
            attackers_probs.append({"attacker_id": companion["unique_id"], "attack_target_id": enemy["unique_id"],
                                    "defeat_probability": calculate_character_attack_prob(companion, enemy)})

    enemy_attack_probs = []
    for enemy in enemies:
        injury_prob, defeat_prob = calculate_enemy_attack_prob(enemy, player)
        enemy_attack_probs.append({"enemy_id": enemy["unique_id"], "enemy_attack_target": "user",
                                   "injury_probability": injury_prob, "defeat_probability": defeat_prob})

        for companion in companions:
            injury_prob, defeat_prob = calculate_enemy_attack_prob(enemy, companion)
            enemy_attack_probs.append({"enemy_id": enemy["unique_id"], "enemy_attack_target": companion["unique_id"],
                                       "injury_probability": injury_prob, "defeat_probability": defeat_prob})

    #fatigue_probs = []
    #fatigue_probs.append({"id": "user", "fatigue_probability": calculate_character_fatigue_prob(player)})
    #for companion in companions:
    #    fatigue_probs.append({"id": companion["unique_id"],
    #                          "fatigue_probability": calculate_character_fatigue_prob(companion)})

    probs = {"flee_probability": calculate_flee_prob(player),
             "attack_probabilities": attackers_probs,
             "enemy_attack_probabilities": enemy_attack_probs}
             #"fatigue_probabilities": fatigue_probs}
    return probs

def increase_injury(character):
    character_dead = False
    if character["injuries"] == "none":
        character["injuries"] = "slight"
    elif character["injuries"] == "slight":
        character["injuries"] = "moderate"
    elif character["injuries"] == "moderate":
        character["injuries"] = "severe"
    elif character["injuries"] == "severe":
        character_dead = True

    return character_dead

def increase_fatigue(character):
    if character["fatigue"] == "none":
        character["fatigue"] = "slight"
    elif character["fatigue"] == "slight":
        character["fatigue"] = "moderate"
    elif character["fatigue"] == "moderate":
        character["fatigue"] = "severe"

    character["rounds_since_fatigue_change"] = 0

def check_fatigue(character):
    prob = calculate_character_fatigue_prob(character) / 100.0
    ran = random.random()
    if ran < prob:
        increase_fatigue(character)
    else:
        character["rounds_since_fatigue_change"] += 1

def update_combat_stats(response_json, player, companions, enemies):
    enemies_to_remove = []
    if "attacks" in response_json:
        for attack in response_json["attacks"]:
            for enemy in enemies:
                if attack["attack_target_id"] == enemy["unique_id"]:
                    if attack["attack_result"]:
                        print("{} is defeated".format(enemy["type"]))
                        enemies_to_remove.append(enemy["unique_id"])
                    else:
                        enemy["rounds_attacked"] = enemy["rounds_attacked"] + 1

    new_enemies = []
    for enemy in enemies:
        if enemy["unique_id"] not in enemies_to_remove:
            new_enemies.append(enemy)
    enemies = new_enemies

    companions_to_remove = []
    if "enemy_attacks" in response_json:
        for enemy_attack in response_json["enemy_attacks"]:
            if enemy_attack["enemy_attack_target"] == "user":
                if enemy_attack["injury"]:
                    dead = increase_injury(player)
                else:
                    dead = False
                if dead or enemy_attack["defeat"]:
                    print("You are defeated.  Game over.")
                    sys.exit()
            else:
                for companion in companions:
                    if enemy_attack["enemy_attack_target"] == companion["unique_id"]:
                        if enemy_attack["injury"]:
                            dead = increase_injury(companion)
                        else:
                            dead = False
                        if dead or enemy_attack["defeat"]:
                            print("{} is defeated".format(companion["name"]))
                            companions_to_remove.append(companion["unique_id"])

    new_companions = []
    for companion in companions:
        if companion["unique_id"] not in companions_to_remove:
            new_companions.append(companion)
    companions = new_companions

    if len(enemies) == 0:
        battle_finished = True
    else:
        battle_finished = False

    return companions, enemies, battle_finished

def print_status(player, companions, enemies):
    print("{} (Level {}), Fatigue: {}, Injuries: {}".format(player["name"], player["level"], player["fatigue"], player["injuries"]))
    for companion in companions:
        print("{} (Level {}), Fatigue: {}, Injuries: {}".format(companion["name"], companion["level"], companion["fatigue"], companion["injuries"]))

    enemy_list = []
    for enemy in enemies:
        enemy_list.append("{} {} (Level {})".format(enemy["descriptor"], enemy["type"], enemy["level"]))

    print("Fighting: {}".format(", ".join(enemy_list)))

def go_through_attacks(gpt_control, player, companions, enemies):
    history = []

    battle_finished = False
    fled = False
    while not battle_finished:
        print_status(player, companions, enemies)

        probs = calculate_probabilities(player, companions, enemies)
        #print(probs)
        action = input("What action will you take? ")

        system_prompt = prompts["fight_user"]["system_prompt"].format(json.dumps(player),
                                                                      json.dumps(companions),
                                                                      json.dumps(enemies),
                                                                      json.dumps(probs),
                                                                      json.dumps(history))
        response = gpt_control.run_llm(system_prompt, action, temperature=0.8, json=True)

        #print(response)

        response_json = json.loads(response)
        history.append(response_json["description"])

        print(response_json["description"])

        #if "fatigued" in response_json and response_json["fatigued"]:
        #    increase_fatigue(player)
        #player["rounds_since_fatigue_change"] += 1
        if "attacks" in response_json and response_json["attacks"]:
            check_fatigue(player)

        companions, enemies, battle_finished = update_combat_stats(response_json, player, companions, enemies)

        if "fled" in response_json and response_json["fled"]:
            fled = True
            break

        for companion in companions:
            probs = calculate_probabilities(player, companions, enemies)
            system_prompt = prompts["fight_companion"]["system_prompt"].format(json.dumps(player),
                                                                               json.dumps(companions),
                                                                               json.dumps(enemies),
                                                                               json.dumps(probs),
                                                                               json.dumps(history))

            response = gpt_control.run_llm(system_prompt, prompts["fight_companion"]["user_prompt"].format(companion["name"]),
                                           temperature=0.8, json=True)

            #print(response)

            response_json = json.loads(response)
            history.append(response_json["description"])

            print(response_json["description"])

            #if "fatigued" in response_json and response_json["fatigued"]:
            #    increase_fatigue(companion)
            #companion["rounds_since_fatigue_change"] += 1
            if "attacks" in response_json and response_json["attacks"]:
                check_fatigue(companion)

            companions, enemies, battle_finished = update_combat_stats(response_json, player, companions, enemies)

        for enemy in enemies:
            probs = calculate_probabilities(player, companions, enemies)
            system_prompt = prompts["fight_enemy"]["system_prompt"].format(json.dumps(player),
                                                                           json.dumps(companions),
                                                                           json.dumps(enemies),
                                                                           json.dumps(probs),
                                                                           json.dumps(history))

            response = gpt_control.run_llm(system_prompt, prompts["fight_enemy"]["user_prompt"].format(json.dumps(enemy)),
                                           temperature=0.8, json=True)

            #print(response)

            response_json = json.loads(response)
            history.append(response_json["description"])

            print(response_json["description"])

            companions, enemies, battle_finished = update_combat_stats(response_json, player, companions, enemies)

    if not fled:
        print("Victory, all enemies defeated!")
    else:
        print("You have fled the battle")

    return fled
