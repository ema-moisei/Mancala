"""
Mmancala:
    1. Acces game -> prezentare mancala(imagine start)
    2. Menu: - Game rules
             - Short Hystory
             - Sound : fundal, game sounds
             - Scores: by player
             - Start game: - Select players: - New player: -Select nickname
                                            - Human players list: - if None: Add player
                                            - Computer player
                                            - Continue: -select random who starts
                                                        -actual game
                                                        -show the winner/ tie
                                                        -play again/ change players/back to menu


actual game: - Objective: collect as many rocks as you can in your bank (right side)
             - each player have: a row of 6 holes, each containing 4 rocks and an emplty banck
             - select a random player who will start the game -> players turns will be flagged by a sign on their's
               avatar
             - the first player will select a hole
             - you can only move the rocks on your side
             - that hole will be cleared and the rocks will be placed one in each of the following pits in sequence
               (counterclockwise), but it will skip the opponent bank
                - if the last rock ends in the bank:
                        - that player have an extra move
                - if the last rock ends in an empty hole in the current player's base and if in the parallel hole are
                      rocks:
                        - the current player will move in the bank that last rock and all the rocks in the parallel hole
             - if only one player is out of rock:
                - the game end's and all the other player's rock will go in their bank
             - when the game end's:
                - the score will be shown
                - the winer/ tie
                - the score will be saved in a file
                - play again/ change player/ menu
"""


import random
import sys

from pyqt5_plugins.examplebutton import QtWidgets

import PlayerDB

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QListWidget, QScrollBar, \
    QListWidgetItem, QHBoxLayout, QLineEdit, QGraphicsView, QVBoxLayout, QMessageBox, QStackedLayout
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QPainter, QPalette, QFont
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint


class Interface:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowIcon(QIcon('M.png'))
        self.window.setWindowTitle("Mancala")
        self.window.setFixedWidth(1500)
        self.window.setFixedHeight(900)
        self.col_min_wid = [12, 125]
        self.row_min_hei = [6, 150]
        self.grid = QGridLayout()
        self.window.setLayout(self.grid)

        self.game = Game()

        self.widgets = {}

        self.leave_button = {"y": 0, "x": 10, "sy": 1, "sx": 2}
        self.back_button = {"y": 0, "x": 10, "sy": 1, "sx": 2}
        self.rules_board = {"y": 0, "x": 0, "sy": 1, "sx": 2}

        self.score_list = {}

        Rules = {"name": "Rules", "function": self.clicked_rules_menu, "img": "brick2.png", "y": 0, "x": 0, "sy": 1,
                 "sx": 2, "ml": 0, "mr": 0}
        Scores = {"name": "Scores", "function": self.clicked_scores, "img": "brick1.png", "y": 1, "x": 0, "sy": 1,
                  "sx": 2, "ml": 0, "mr": 0}
        History = {"name": "History", "function": self.clicked_history, "img": "brick3.png", "y": 2, "x": 0, "sy": 1,
                   "sx": 2, "ml": 0, "mr": 0}
        Play = {"name": "Play", "function": self.choose_players, "img": "background.png", "y": 6, "x": 10, "sy": 1,
                "sx": 2, "ml": 0, "mr": 0}
        self.menu_buttons = [Rules, Play, Scores, History]

        self.player_l = {"name": "blueish.png", "y": 1, "x": 2, "sy": 2, "sx": 3}
        self.player_r = {"name": "blueish.png", "y": 1, "x": 7, "sy": 2, "sx": 3}
        self.choose_players_images = [self.player_l, self.player_r]

        self.lineedit_l = {"y": 3, "x": 5, "sy": 1, "sx": 2}

        self.sel_l = {"y": 4, "x": 2, "sy": 2, "sx": 3}
        self.sel_r = {"y": 4, "x": 7, "sy": 2, "sx": 3}
        self.r_list = {}
        self.l_list = {}
        self.left_chosen_players = ""
        self.right_chosen_players = ""
        self.selected_player = "", ""

        self.del_button = {"y": 5, "x": 5, "sy": 1, "sx": 2}

        self.hidden_play_button = {"name": "", "img": "hidden_play_button.png", "function": self.board,
                                   "y": 1, "x": 5, "sy": 2, "sx": 2}
        self.pl_al_exists = {"y": 1, "x": 5, "sy": 2, "sx": 2}

        self.first_player_side = {"y": 3, "x": 3}
        self.second_player_side = {"y": 2, "x": 8}
        self.f_pl_label = {"y": 5, "x": 5, "sy": 1, "sx": 2}
        self.s_pl_label = {"y": 0, "x": 5, "sy": 1, "sx": 2}
        self.first_player_side_widgets = {}
        self.second_player_side_widgets = {}
        self.current_player = ""
        self.rock = {"name": "rock.png", "y": 1, "x": 2, "sy": 2, "sx": 3}

        self.tie_label = {"y": 5, "x": 2, "sy": 5, "sx": 4}
        self.winner = {"y": 1, "x": 5, "sy": 3, "sx": 3}
        self.winner_w = {"y": 5, "x": 2, "sy": 5, "sx": 4}
        self.loser_w = {"y": 5, "x": 8, "sy": 5, "sx": 4}

    def start_image(self):
        self.window.show()
        self.window.setStyleSheet("background-image: url(start.png);")
        QTimer.singleShot(300, self.menu_background)

    def set_grid(self):
        for i in range(self.col_min_wid[0]):
            self.grid.setColumnMinimumWidth(i, self.col_min_wid[1])
        for i in range(self.row_min_hei[0]):
            self.grid.setRowMinimumHeight(i, self.row_min_hei[1])

    def clicked_rules_menu(self):
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(rules.png);")
        back_button = self.create_menu_button("Back", self.menu_background, "brick2.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    def clicked_scores(self):
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(scores.png);")
        layout = QGridLayout(self.window)
        self.window.setLayout(layout)
        list_widget = QListWidget(self.window)

        list_widget.setStyleSheet("background-image: url(brick1.png); background-position: center;")

        player_list = PlayerDB.get_player_list()
        if len(player_list) > 0:
            for player in player_list:
                line = "Name: " + player["name"] + ", Wins: " + str(player["wins"])
                item = QListWidgetItem(line)
                item.setFont(QFont('Trebuchet MS', 15))
                item.setForeground(Qt.darkRed)
                list_widget.addItem(item)
                self.score_list[player["name"]] = item
                self.widgets["score_list"] = self.score_list

        scroll_bar = QScrollBar(self.window)
        scroll_bar.setStyleSheet("background : lightgreen;")
        list_widget.setVerticalScrollBar(scroll_bar)

        self.grid.addWidget(list_widget, 2, 0, 4, 12)

        back_button = self.create_menu_button("Back", self.menu_background, "brick1.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    def clicked_history(self):
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(history.png);")
        back_button = self.create_menu_button("Back", self.menu_background, "brick3.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    @staticmethod
    def create_menu_button(button_label, function, img, parent, margin_l=0, margin_r=0):
        button = QPushButton(button_label, parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#460A1C';
            border-radius: 15px;
            color: '#460A1C';
            font: bold 30px;
            font-family: 'Trebuchet MS';
            font-size: 30px;
            height: 90px;
            width : 90px;
            background-image: url(''' + img + ');' +
            '''padding: 0px 0;
            margin-top: 0px}
            '''
        )
        button.clicked.connect(function)
        return button

    def set_menu_buttons(self, button_list):
        if self.widgets:
            self.clear_widget()
        for button in button_list:
            button_el = self.create_menu_button(button["name"], button["function"], button["img"],
                                                self.window, button["ml"], button["mr"])
            button_el.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button_el, button["y"], button["x"], button["sy"], button["sx"])
            self.widgets[button["name"]] = button_el

    def clear_widget(self):
        self.widgets = {}
        self.r_list = {}
        self.l_list = {}
        self.score_list = {}
        self.first_player_side_widgets = {}
        self.second_player_side_widgets = {}
        self.left_chosen_players = ""
        self.right_chosen_players = ""
        self.selected_player = "", ""
        self.current_player = ""
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def menu_background(self):
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(menu3.png);")
        self.set_grid()
        self.set_menu_buttons(self.menu_buttons)

    def create_img(self, img_list):
        for image in img_list:
            image_el = QPixmap(image["name"])
            player = QLabel(self.window)
            player.setPixmap(image_el)
            self.grid.addWidget(player, image["y"], image["x"], image["sy"], image["sx"])
            self.widgets[image["name"]] = image_el

    def add_player(self, nickname):
        add_player = PlayerDB.add_new_player(nickname)
        if add_player < 0:
            self.add_error_label("This player already exists", "player_already_exists", self.pl_al_exists["y"],
                                 self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
            QTimer.singleShot(1500, self.widgets["player_already_exists"].hide)

        self.select_player(self.sel_r["y"], self.sel_r["x"], self.sel_r["sy"], self.sel_r["sx"], "r")
        self.select_player(self.sel_l["y"], self.sel_l["x"], self.sel_l["sy"], self.sel_l["sx"], "l")
        self.widgets["lineedit"].clear()

    def create_line_edit(self, y, x, sy=1, sx=1):
        hbox = QHBoxLayout(self.window)
        lineedit = QLineEdit(self.window)
        lineedit.setStyleSheet("background-image: url(bluebackground.png); background-position: center;")
        lineedit.setPlaceholderText("Add player...")
        lineedit.setMaxLength(20)
        lineedit.returnPressed.connect(lambda: self.add_player(lineedit.text()))
        self.window.setLayout(hbox)
        self.grid.addWidget(lineedit, y, x, sy, sx)
        self.widgets["lineedit"] = lineedit
        print(self.widgets)

    def add_label(self, text, key, y, x, sy, sx):
        label = QLabel(text, self.window)
        self.grid.addWidget(label, y, x, sy, sx)
        label.setWordWrap(True)
        self.widgets[key] = label

    def clicked_del_button(self):
        if self.selected_player[0] == "":
            return
        if self.right_chosen_players and self.left_chosen_players:
            if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                self.widgets["hidden_play_button"].hide()
        PlayerDB.delete_player(self.selected_player[0])
        self.select_player(self.sel_r["y"], self.sel_r["x"], self.sel_r["sy"], self.sel_r["sx"], "r")
        self.select_player(self.sel_l["y"], self.sel_l["x"], self.sel_l["sy"], self.sel_l["sx"], "l")
        location = self.selected_player[1]
        if location == "r":
            if self.right_chosen_players == "Computer":
                self.add_error_label("You can't detele this player", "del_computer", self.pl_al_exists["y"],
                                     self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
                QTimer.singleShot(1500, self.widgets["del_computer"].hide)
                return
            self.right_chosen_players = ""
        elif location == "l":
            self.left_chosen_players = ""

        # self.create_img([self.choose_players_images[1]])
        # self.create_img([self.choose_players_images[0]])
        self.r_list.pop(self.selected_player[0])
        self.l_list.pop(self.selected_player[0])

    def del_player_button(self, y, x, sy=1, sx=1):
        del_button = QPushButton("Delete selected player", self.window)
        del_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        del_button.setStyleSheet(
            '''
            color: '#138CFC';
            border-radius: 45px;
            height: 150px;
            width : 100px;
            font: bold 10px;
            font-family: 'Trebuchet MS';
            font-size: 20px;
            background-image: url(button_backgound.png);}
            '''
        )
        del_button.clicked.connect(self.clicked_del_button)
        del_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(del_button, y, x, sy, sx)
        self.widgets["del_button"] = del_button

    def add_pl_label(self, text, key, y, x, sy, sx):
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            color: '#460A1C';
            font: bold 30px;
            font-family: 'Trebuchet MS';
            font-size: 30px;
            height: 150px;
            width : 100px;
            background-image: url(blueish.png);}
            '''
            )
        self.grid.addWidget(label, y, x, sy, sx)
        label.setWordWrap(True)
        self.widgets[key] = label

    def add_error_label(self, text, key, y, x, sy, sx):
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            color: '#460A1C';
            font: bold 30px;
            font-family: 'Trebuchet MS';
            font-size: 20px;
            height: 150px;
            width : 100px;
            background-image: url(blueish.png);}
            '''
            )
        self.grid.addWidget(label, y, x, sy, sx)
        label.setWordWrap(True)
        self.widgets[key] = label

    def selected_pl_r(self, item):
        print("da", QListWidgetItem(item).text(), item)
        nickname = QListWidgetItem(item).text()
        self.selected_player = nickname, "r"
        print(self.selected_player)
        if "right_label" not in self.widgets.keys():
            self.add_pl_label(nickname, "right_label", self.player_r["y"], self.player_r["x"],
                              self.player_r["sy"], self.player_r["sx"])
        else:
            self.widgets.pop("right_label")
            self.add_pl_label(nickname, "right_label", self.player_r["y"], self.player_r["x"],
                              self.player_r["sy"], self.player_r["sx"])
        self.right_chosen_players = nickname
        if self.left_chosen_players:
            if self.right_chosen_players != self.left_chosen_players:
                if "different_player" in self.widgets.keys():
                    self.widgets["different_player"].hide()
                self.widgets["hidden_play_button"].show()
            else:
                self.add_pl_label(nickname, "right_label", self.player_r["y"], self.player_r["x"],
                                  self.player_r["sy"], self.player_r["sx"])
                self.right_chosen_players = ""
                self.add_error_label("Please select a different player!", "different_player", self.pl_al_exists["y"],
                                     self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
                # QTimer.singleShot(1500, self.widgets["different_player"].hide)
                # self.create_img([self.choose_players_images[1]])
                if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                    self.widgets["hidden_play_button"].hide()
                    self.widgets["right_label"].hide()
                    self.widgets.pop("right_label")

    def selected_pl_l(self, item):
        print("da", QListWidgetItem(item).text(), item)
        nickname = QListWidgetItem(item).text()
        self.selected_player = nickname, "l"
        print(self.selected_player)
        if "left_label" not in self.widgets.keys():
            self.add_pl_label(nickname, "left_label", self.player_l["y"], self.player_l["x"],
                              self.player_l["sy"], self.player_l["sx"])
        else:
            self.widgets.pop("left_label")
            self.add_pl_label(nickname, "left_label", self.player_l["y"], self.player_l["x"],
                              self.player_l["sy"], self.player_l["sx"])
        self.left_chosen_players = nickname
        if self.right_chosen_players:
            if self.right_chosen_players != self.left_chosen_players:
                if "different_player" in self.widgets.keys():
                    self.widgets["different_player"].hide()
                self.widgets["hidden_play_button"].show()
            else:
                self.add_pl_label(nickname, "left_label", self.player_l["y"], self.player_l["x"],
                                  self.player_l["sy"], self.player_l["sx"])
                self.left_chosen_players = ""
                self.add_error_label("Please select a different player!", "different_player", self.pl_al_exists["y"],
                                     self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
                # QTimer.singleShot(1500, self.widgets["different_player"].hide)
                # self.create_img([self.choose_players_images[0]])
                if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                    self.widgets["hidden_play_button"].hide()
                    self.widgets["left_label"].hide()
                    self.widgets.pop("left_label")

    def select_player(self, y, x, sy, sx, location):
        layout = QGridLayout(self.window)
        self.window.setLayout(layout)
        list_widget = QListWidget(self.window)

        list_widget.setStyleSheet("background-image: url(background.png); background-position: center;")

        if location == "r":
            item = QListWidgetItem("Computer")
            item.setFont(QFont('Trebuchet MS', 15))
            item.setForeground(Qt.darkRed)
            list_widget.addItem(item)
            self.widgets["Computer"] = item

        player_list = PlayerDB.get_player_list()
        if len(player_list) > 0:
            for player in player_list:
                item = QListWidgetItem(player["name"])
                item.setFont(QFont('Trebuchet MS', 15))
                item.setForeground(Qt.darkRed)
                list_widget.addItem(item)
                if location == "r":
                    self.r_list[player["name"]] = item
                    self.widgets["r_list"] = self.r_list
                elif location == "l":
                    self.l_list[player["name"]] = item
                    self.widgets["l_list"] = self.l_list

        if location == "r":
            list_widget.itemClicked.connect(self.selected_pl_r)

        if location == "l":
            list_widget.itemClicked.connect(self.selected_pl_l)

        scroll_bar = QScrollBar(self.window)
        scroll_bar.setStyleSheet("background : lightgreen;")
        list_widget.setVerticalScrollBar(scroll_bar)

        self.grid.addWidget(list_widget, y, x, sy, sx)

    def create_play_button(self, play_button, parent):
        button = QPushButton(play_button["name"], parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            '''
            border-radius: 45px;
            height: 150px;
            width : 100px;
            background-image: url(hidden_play_button.png);}
            '''
        )
        button.clicked.connect(play_button["function"])
        self.grid.addWidget(button, play_button["y"], play_button["x"], play_button["sy"], play_button["sx"])
        self.widgets["hidden_play_button"] = button
        button.hide()

    def choose_players(self):
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(choose_players.png);")

        self.create_line_edit(self.lineedit_l["y"], self.lineedit_l["x"], self.lineedit_l["sy"], self.lineedit_l["sx"])

        self.select_player(self.sel_r["y"], self.sel_r["x"], self.sel_r["sy"], self.sel_r["sx"], "r")
        self.select_player(self.sel_l["y"], self.sel_l["x"], self.sel_l["sy"], self.sel_l["sx"], "l")

        self.del_player_button(self.del_button["y"], self.del_button["x"], self.del_button["sy"], self.del_button["sx"])
        self.create_play_button(self.hidden_play_button, self.window)

        back_button = self.create_menu_button("Back", self.menu_background, "background.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    @staticmethod
    def mancala_button(button_label, function, parent, margin_l=0, margin_r=0):
        button = QPushButton(button_label, parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#138CFC';
            border-radius: 45px;
            color: white;
            font-family: 'shanti';
            font-size: 16px;
            height: 150px;
            width : 100px;
            background: transparent;
            padding: 0px 0;
            margin-top: 0px}
            *:hover{
                background: '#BC006C'

            }
            '''
        )
        button.clicked.connect(function)
        return button

    def show_current_player_side(self, next_player):
        if self.current_player != next_player:
            if self.current_player == self.game.first_player:
                for key, value in self.first_player_side_widgets.items():
                    value.hide()
                self.widgets["first_player"].hide()
                for key, value in self.second_player_side_widgets.items():
                    value.show()
                self.widgets["second_player"].show()
            else:
                for key, value in self.second_player_side_widgets.items():
                    value.hide()
                self.widgets["second_player"].hide()
                for key, value in self.first_player_side_widgets.items():
                    value.show()
                self.widgets["first_player"].show()

    def evaluate_board(self, new_board, next_player):
        if not new_board and not next_player:
            self.end_game()
        if self.game.second_player != "Computer":
            if new_board and next_player:
                self.show_current_player_side(next_player)
                print("functie pentru update the holes images")

    def selected_hole_first_player(self):
        self.current_player = self.game.first_player
        temp = self.window.sender()
        print("item", temp)
        for key, value in self.first_player_side_widgets.items():
            if value == temp:
                print(self.game.first_player, key)
                new_board, next_player = self.game.move(self.game.first_player, key)
                self.evaluate_board(new_board, next_player)
                if self.game.second_player == "Computer":
                    self.evaluate_board(self.game.second_player_turn, self.game.first_player)

    def set_fist_player_side(self):
        if self.second_player_side_widgets:
            for key, value in self.second_player_side_widgets.items():
                value.hide()
        x = self.first_player_side["x"]
        for i in range(6):
            button = self.mancala_button(str(i), self.selected_hole_first_player, self.window)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button, self.first_player_side["y"], x)
            self.first_player_side_widgets[i] = button
            x += 1

    def selected_hole_second_player(self):
        self.current_player = self.game.second_player
        temp = self.window.sender()
        print("item", temp)
        for key, value in self.second_player_side_widgets.items():
            if value == temp:
                print(self.game.second_player, key)
                new_board, next_player = self.game.move(self.game.second_player, key)
                self.evaluate_board(new_board, next_player)

    def set_second_player_side(self):
        x = self.second_player_side["x"]
        for i in range(6):
            button = self.mancala_button(str(i), self.selected_hole_second_player, self.window)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button, self.second_player_side["y"], x)
            self.second_player_side_widgets[i] = button
            x -= 1
            button.hide()

    def back_to_game(self):
        self.widgets["rules_board"].hide()
        self.widgets["back_from_rules"].hide()

    def clicked_rules_board(self):
        label = QLabel("", self.window)
        pixmap = QPixmap('rules.png')
        label.setPixmap(pixmap)

        label.setAlignment(Qt.AlignCenter)

        self.grid.addWidget(label, 0, 0, 9, 15)
        self.widgets["rules_board"] = label

        back_button = self.create_menu_button("Back to game", self.back_to_game, "brick2.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    def clicked_leave_option(self, option):
        if option.text() == "Cancel":
            pass
        if option.text() == "OK":
            self.menu_background()

    def clicked_leave(self):
        leave_msg = QMessageBox(self.window)
        leave_msg.setWindowTitle("Leave the game")
        leave_msg.setText("Are you sure you want to leave the game? \n All the progress will be lost!")
        leave_msg.setIcon(QMessageBox.Question)
        leave_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        leave_msg.setDefaultButton(QMessageBox.Cancel)

        leave_msg.buttonClicked.connect(self.clicked_leave_option)

        x = leave_msg.exec_()

    def create_rock_img(self, text, key, y, x, sy, sx):
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            color: '#460A1C';
            font: bold 30px;
            font-family: 'Trebuchet MS';
            font-size: 30px;
            height: 150px;
            width : 100px;
            background-image: url(rock1.png);}
            '''
        )
        self.grid.addWidget(label, y, x, sy, sx)
        label.setWordWrap(True)
        self.widgets[key] = label

    def shoot(self):
        self.anim = QtCore.QPropertyAnimation(self.label, b'geometry')  #
        self.anim.setDuration(2000)  #
        self.anim.setStartValue(QtCore.QRect(3, 3, 1, 1))  #
        self.anim.setEndValue(QtCore.QRect(5, 5, 2, 2))  #
        self.anim.start()  #

    def board(self):
        temp_l = self.left_chosen_players
        temp_r = self.right_chosen_players
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(board.png);")

        self.left_chosen_players = temp_l
        self.right_chosen_players = temp_r

        self.set_fist_player_side()
        self.set_second_player_side()

        print(self.left_chosen_players, self.right_chosen_players, "left, right")

        # self.create_rock_img("p", "rock", 3, 3, 1, 1)

        # label = self.widgets["rock"]

        first_player, second_player = self.game.choose_first_player([self.left_chosen_players,
                                                                     self.right_chosen_players])

        self.add_pl_label(first_player, "first_player", self.f_pl_label["y"], self.f_pl_label["x"],
                          self.f_pl_label["sy"], self.f_pl_label["sx"])
        self.add_pl_label(second_player, "second_player", self.s_pl_label["y"], self.s_pl_label["x"],
                          self.s_pl_label["sy"], self.s_pl_label["sx"])
        self.widgets["second_player"].hide()

        leave_button = self.create_menu_button("Leave", self.clicked_leave, "background.png", self.window)
        leave_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(leave_button, self.leave_button["y"], self.leave_button["x"], self.leave_button["sy"],
                            self.leave_button["sx"])
        self.widgets["back_from_rules"] = leave_button

        rules_board = self.create_menu_button("Rules", self.clicked_rules_board, "brick2.png", self.window)
        rules_board.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(rules_board, self.rules_board["y"], self.rules_board["x"], self.rules_board["sy"],
                            self.rules_board["sx"])
        self.widgets["rules_board"] = rules_board

    def end_game(self):
        self.clear_widget()

        winner_wins = -1
        loser_wins = -1
        if self.game.first_pl_bank > self.game.second_pl_bank:
            winner = self.game.first_player
            loser = self.game.second_player
        elif self.game.first_pl_bank < self.game.second_pl_bank:
            winner = self.game.second_player
            loser = self.game.first_player
        else:
            winner = ""
            loser = ""

        if winner == "":
            self.window.setStyleSheet("background-image: url(tie.png);")
            self.add_label("Tie", "Tie", self.tie_label["y"], self.tie_label["x"],
                           self.tie_label["sy"], self.tie_label["sx"])

        else:
            players_list = PlayerDB.get_player_list()
            for player in players_list:
                if player["name"] == winner:
                    winner_wins = player["wins"] + 1
                if player["name"] == loser:
                    loser_wins = player["wins"]

                self.window.setStyleSheet("background-image: url(end_game.png);")
                self.add_label("The Winner is:" + str(winner), "winner", self.winner["y"], self.winner["x"],
                               self.winner["sy"], self.winner["sx"])
                self.add_label(str(winner) + "Tottal wins:" + str(winner_wins), "winner_wins",
                               self.winner_w["y"], self.winner_w["x"], self.winner_w["sy"], self.winner_w["sx"])
                self.add_label(str(loser) + "Tottal wins:" + str(loser_wins), "loser_wins",
                               self.loser_w["y"], self.loser_w["x"], self.loser_w["sy"], self.loser_w["sx"])
                PlayerDB.save_wins(winner)

        # gif = QLabel(self.window)
        # gif.setFixedSize(1500, 900)
        # gif.setAlignment(Qt.AlignCenter)
        # movie = QMovie("winner.gif")
        # gif.setMovie(movie)
        # movie.start()


class Game:
    def __init__(self):
        self.first_pl_holes = [4, 4, 4, 4, 4, 4]
        self.first_pl_bank = [0]
        self.second_pl_holes = [4, 4, 4, 4, 4, 4]
        self.second_pl_bank = [0]
        self.first_player_turn = [self.first_pl_bank, self.second_pl_holes, self.first_pl_holes]
        self.second_player_turn = [self.second_pl_bank, self.first_pl_holes, self.second_pl_holes]
        self.loop_game = True
        self.first_player = ""
        self.second_player = ""
        self.first_game = True

    def restart(self):
        self.first_pl_holes = [4, 4, 4, 4, 4, 4]
        self.first_pl_bank = [0]
        self.second_pl_holes = [4, 4, 4, 4, 4, 4]
        self.second_pl_bank = [0]
        self.loop_game = True
        self.first_player = ""
        self.second_player = ""

    def choose_first_player(self, players_list):
        if not self.first_game:
            self.restart()
        if players_list[0] == "Computer" or players_list[1] == "Computer":
            if players_list[0] == "Computer":
                self.first_player = players_list[1]
                self.second_player = players_list[0]
                first_player = players_list[1]
                second_player = players_list[0]
            else:
                self.first_player = players_list[0]
                self.second_player = players_list[1]
                first_player = players_list[0]
                second_player = players_list[1]
            self.first_game = False
            return first_player, second_player
        else:
            random_nr = random.randint(0, 1)
            if random_nr == 0:
                first_player = players_list[0]
                second_player = players_list[1]
                self.first_player = first_player
                self.second_player = second_player
            else:
                first_player = players_list[1]
                second_player = players_list[0]
                self.first_player = first_player
                self.second_player = second_player
            self.first_game = False
            return first_player, second_player

    def verify_state(self):
        first_pl_holes_state = False
        second_pl_holes_state = False
        for index, hole in enumerate(self.first_pl_holes):
            if self.first_pl_holes[index] != 0:
                first_pl_holes_state = True
                break
        for index, hole in enumerate(self.second_pl_holes):
            if self.second_pl_holes[index] != 0:
                second_pl_holes_state = True
                break
        if not first_pl_holes_state and not second_pl_holes_state:
            self.loop_game = False
        if not first_pl_holes_state or not second_pl_holes_state:
            if not first_pl_holes_state:
                for index, hole in enumerate(self.second_pl_holes):
                    self.second_pl_bank[0] += self.second_pl_holes[index]
                    self.second_pl_holes[index] = 0
            if not second_pl_holes_state:
                for index, hole in enumerate(self.first_pl_holes):
                    self.first_pl_bank[0] += self.first_pl_holes[index]
                    self.first_pl_holes[index] = 0
            self.loop_game = False

    def computer_move(self):
        extra_move = False
        rocks = 0
        hole = -1
        while not rocks:
            holes = [0, 1, 2, 3, 4, 5]
            hole = random.choice(holes)
            rocks = self.second_pl_holes[hole]
        last_hole_value = -1
        last_list = []
        last_index = None
        turn = self.second_player_turn
        self.second_pl_holes[hole] = 0
        next_hole = hole + 1
        for i in range(hole + 1, len(self.second_pl_holes)):
            last_hole_value = self.second_pl_holes[next_hole]
            last_index = next_hole
            last_list = self.second_pl_holes
            self.second_pl_holes[next_hole] += 1
            next_hole += 1
            rocks -= 1
            if rocks == 0:
                break
        while rocks:
            for lista in turn:
                for index, hole in enumerate(lista):
                    last_hole_value = lista[index]
                    last_index = index
                    last_list = lista
                    lista[index] += 1
                    rocks -= 1
                    if rocks == 0:
                        break
                if rocks == 0:
                    break
            if rocks == 0:
                break
        if last_list == turn[2] and last_hole_value == 0:
            if turn[1][len(turn[1]) - last_index - 1] != 0:
                turn[0][0] += turn[1][len(turn[1])-last_index-1] + 1
                turn[1][len(turn[1]) - last_index - 1] = 0
                turn[2][last_index] = 0
        if len(last_list) == 1:
            extra_move = True
        self.verify_state()

        print(self.first_pl_holes)
        print(self.first_pl_bank)
        print(self.second_pl_holes)
        print(self.second_pl_bank)

        if self.loop_game:
            if extra_move:
                self.computer_move()
            else:
                self.second_player_turn = turn

    def move(self, current_player, hole):
        last_hole_value = -1
        last_list = []
        last_index = None
        extra_move = False
        if current_player == self.first_player:
            turn = self.first_player_turn
            rocks = self.first_pl_holes[hole]
            if rocks == 0:
                return [], self.first_player
            next_player = self.second_player
            self.first_pl_holes[hole] = 0
            next_hole = hole + 1
            for i in range(hole + 1, len(self.first_pl_holes)):
                last_hole_value = self.first_pl_holes[next_hole]
                last_index = next_hole
                last_list = self.first_pl_holes
                self.first_pl_holes[next_hole] += 1
                next_hole += 1
                rocks -= 1
                if rocks == 0:
                    break
        else:
            turn = self.second_player_turn
            rocks = self.second_pl_holes[hole]
            if rocks == 0:
                return [], self.second_player
            next_player = self.first_player
            self.second_pl_holes[hole] = 0
            next_hole = hole + 1
            for i in range(hole + 1, len(self.second_pl_holes)):
                last_hole_value = self.second_pl_holes[next_hole]
                last_index = next_hole
                last_list = self.second_pl_holes
                self.second_pl_holes[next_hole] += 1
                next_hole += 1
                rocks -= 1
                if rocks == 0:
                    break
        while rocks:
            for lista in turn:
                for index, hole in enumerate(lista):
                    last_hole_value = lista[index]
                    last_index = index
                    last_list = lista
                    lista[index] += 1
                    rocks -= 1
                    if rocks == 0:
                        break
                if rocks == 0:
                    break
            if rocks == 0:
                break
        if last_list == turn[2] and last_hole_value == 0:
            if turn[1][len(turn[1]) - last_index - 1] != 0:
                turn[0][0] += turn[1][len(turn[1])-last_index-1] + 1
                turn[1][len(turn[1]) - last_index - 1] = 0
                turn[2][last_index] = 0
        if len(last_list) == 1:
            extra_move = True
        self.verify_state()

        print(self.first_pl_holes)
        print(self.first_pl_bank)
        print(self.second_pl_holes)
        print(self.second_pl_bank)

        if self.loop_game:
            if self.second_player == "Computer" and not extra_move:
                self.computer_move()
            if extra_move:
                return turn, current_player
            else:
                return turn, next_player
        else:
            return [], ""


if __name__ == "__main__":
    interface = Interface()
    interface.start_image()
    sys.exit(interface.app.exec())

