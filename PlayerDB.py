import os

PLAYER_ADDED = 1
PLAYER_ALREADY_EXISTS = -1
INVALID_NICKNAME = "Computer"


def get_player_list():
    """Returns a list with all the players that played in the past and how many times they won"""
    pl_list = []
    current_dir_path = os.getcwd()
    player_list = "player_list.txt"
    file_path = os.path.join(current_dir_path, player_list)
    if not os.path.isfile(file_path):
        return pl_list
    handler = open(player_list, "r")
    player = handler.readline().strip()
    while player:
        pl_list.append(eval(player))
        player = handler.readline().strip()
    handler.close()
    return pl_list


def add_computer_player():
    """Adds the Computer player to the players list"""
    current_dir_path = os.getcwd()
    player_list = "player_list.txt"
    file_path = os.path.join(current_dir_path, player_list)
    if not os.path.isfile(file_path):
        handler = open(player_list, "w")
        temp = {"name": "Computer", "wins": 0, "player_id": -1}
        handler.write(str(temp))
        handler.write("\n")
        handler.close()


def add_new_player(new_player):
    """Adds a new player to the players list"""
    players = get_player_list()
    for player in players:
        if new_player == player["name"]:
            return PLAYER_ALREADY_EXISTS
        if new_player == "Computer":
            return INVALID_NICKNAME

    player_list = "player_list.txt"
    if len(players) == 0:
        player_id = 1
    else:
        last_player = players[-1]
        player_id = int(last_player["player_id"]) + 1
    player = {"name": new_player, "wins": 0, "player_id": player_id}
    handler = open(player_list, "a")
    handler.write(str(player))
    handler.write("\n")
    handler.close()
    return PLAYER_ADDED


def delete_player(name):
    """Deletes a player from the players list"""
    players_list = []
    player_list = "player_list.txt"
    handler = open(player_list, "r")
    player = handler.readline().strip()
    while player:
        players_list.append(eval(player))
        player = handler.readline().strip()
    handler.close()
    for index, player in enumerate(players_list):
        if name == player["name"]:
            players_list.pop(index)
    handler = open(player_list, "w")
    for player in players_list:
        lista_campuri = ["name", "wins", "player_id"]
        temp = {}
        for item in lista_campuri:
            temp[item] = player[item]
        handler.write(str(temp))
        handler.write("\n")
    handler.close()


def save_wins(winner):
    """Increments the number of wins for the player who won"""
    players_list = get_player_list()
    for player in players_list:
        if player["name"] == winner:
            player["wins"] += 1
            break
    player_list = "player_list.txt"
    handler = open(player_list, "w")
    for player in players_list:
        handler.write(str(player))
        handler.write("\n")
    handler.close()

