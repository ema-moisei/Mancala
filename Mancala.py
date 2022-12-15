import random
import sys
import os
import time

import PlayerDB

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QListWidget, QScrollBar, \
    QListWidgetItem, QHBoxLayout, QLineEdit, QGraphicsView, QVBoxLayout, QMessageBox, QStackedLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QPainter, QPalette, QFont
from PyQt5 import QtGui, QtCore, QtWidgets, QtMultimedia, QtTest
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint, QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from pyqt5_plugins.examplebutton import QtWidgets


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

        self.playlist = QMediaPlaylist()
        self.player = QMediaPlayer()

        self.game = Game(self)

        self.widgets = {}

        self.rules = False
        self.scores = False
        self.sound = True
        self.mute_button = {"y": 5, "x": 0, "sy": 1, "sx": 1}
        self.scores_mute_button = {"y": 0, "x": 0, "sy": 1, "sx": 1}
        self.rules_mute_button = {"y": 5, "x": 11, "sy": 1, "sx": 1}

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
        Play = {"name": "Play", "function": self.choose_players, "img": "background.png", "y": 5, "x": 10, "sy": 1,
                "sx": 2, "ml": 0, "mr": 0}
        self.menu_buttons = [Rules, Play, Scores, History]

        self.scores_scroll_bar = {"y": 2, "x": 0, "sy": 4, "sx": 12}

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

        self.rules_img = {"y": 0, "x": 0, "sy": 9, "sx": 15}

        self.first_player_side = {"y": 3, "x": 3}
        self.second_player_side = {"y": 2, "x": 8}
        self.f_pl_label = {"y": 5, "x": 5, "sy": 1, "sx": 2}
        self.s_pl_label = {"y": 0, "x": 5, "sy": 1, "sx": 2}
        self.first_player_side_widgets = {}
        self.second_player_side_widgets = {}
        self.first_player_side_img = {}
        self.second_player_side_img = {}
        self.f_pl_bank = {"y": 2, "x": 9, "sy": 2, "sx": 1}
        self.s_pl_bank = {"y": 2, "x": 2, "sy": 2, "sx": 1}
        self.first_player_bank = ""
        self.second_player_bank = ""
        self.current_player = ""
        self.computer_side = {}
        self.computer_selected_hole = -1

        self.play_again = {"y": 5, "x": 10, "sy": 1, "sx": 2}
        self.tie_label = {"y": 5, "x": 2, "sy": 1, "sx": 1}
        self.winner = {"y": 2, "x": 5, "sy": 1, "sx": 2}
        self.winner_w = {"y": 3, "x": 1, "sy": 1, "sx": 4}
        self.loser_w = {"y": 3, "x": 7, "sy": 1, "sx": 4}

    def start_music(self):
        """Gets the mp3 file and starts play the song in loop"""
        url = QUrl.fromLocalFile("Blue-Ridge_Looping.mp3")
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.playlist)
        self.player.play()

    def start_image(self):
        """Opens the gui window, starts the music and opens the game menu"""
        self.window.show()
        self.window.setStyleSheet("background-image: url(start.png);")
        QtTest.QTest.qWait(1000)
        self.start_music()
        self.menu_background()

    def set_grid(self):
        """Sets the number of columns and rows, and their dimension in pixels"""
        for i in range(self.col_min_wid[0]):
            self.grid.setColumnMinimumWidth(i, self.col_min_wid[1])
        for i in range(self.row_min_hei[0]):
            self.grid.setRowMinimumHeight(i, self.row_min_hei[1])

    def clear_widget(self):
        """Clears the widgets from the grid and resets the variables that stored situational information"""
        self.widgets = {}
        self.score_list = {}
        self.r_list = {}
        self.l_list = {}
        self.left_chosen_players = ""
        self.right_chosen_players = ""
        self.selected_player = "", ""
        self.first_player_side_widgets = {}
        self.second_player_side_widgets = {}
        self.first_player_side_img = {}
        self.second_player_side_img = {}
        self.first_player_bank = ""
        self.second_player_bank = ""
        self.current_player = ""
        self.computer_side = {}
        self.computer_selected_hole = -1
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def clicked_rules_menu(self):
        """The actions that will happen when rules button is clicked"""
        self.rules = True
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(rules.png);")
        back_button = self.create_menu_button("Back", self.menu_background, "brick2.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

        self.create_music_button(self.rules_mute_button["y"], self.rules_mute_button["x"],
                                 self.rules_mute_button["sy"], self.rules_mute_button["sx"])

    def clicked_scores(self):
        """The actions that will happen when scores button is clicked"""
        self.scores = True
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
        scroll_bar.setStyleSheet("background : #138CFC;")
        list_widget.setVerticalScrollBar(scroll_bar)

        self.grid.addWidget(list_widget, self.scores_scroll_bar["y"], self.scores_scroll_bar["x"],
                            self.scores_scroll_bar["sy"], self.scores_scroll_bar["sx"])
        self.widgets["scroll_bar"] = scroll_bar

        back_button = self.create_menu_button("Back", self.menu_background, "brick1.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

        self.create_music_button(self.scores_mute_button["y"], self.scores_mute_button["x"],
                                 self.scores_mute_button["sy"], self.scores_mute_button["sx"])

    def clicked_history(self):
        """The actions that will happen when history button is clicked"""
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(history.png);")
        back_button = self.create_menu_button("Back", self.menu_background, "brick3.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

        self.create_music_button(self.mute_button["y"], self.mute_button["x"],
                                 self.mute_button["sy"], self.mute_button["sx"])

    @staticmethod
    def create_menu_button(button_label, function, img, parent, margin_l=0, margin_r=0):
        """Sets a button design for the game menu"""
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

    def clicked_mute_button(self):
        """The actions that will happen when music button is clicked (in order to stop the music)"""
        self.widgets["sound_on"].deleteLater()
        self.widgets["sound_on"] = None
        self.widgets["sound_on"] = ""

        self.player.stop()
        self.sound = False

        mute_button = self.create_mute_button("", self.clicked_sound_on, "mute.png", "sound_on.png", self.window)
        mute_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if self.rules is True:
            self.grid.addWidget(mute_button, self.rules_mute_button["y"], self.rules_mute_button["x"],
                                self.rules_mute_button["sy"], self.rules_mute_button["sx"])
        elif self.scores is True:
            self.grid.addWidget(mute_button, self.scores_mute_button["y"], self.scores_mute_button["x"],
                                self.scores_mute_button["sy"], self.scores_mute_button["sx"])
        else:
            self.grid.addWidget(mute_button, self.mute_button["y"], self.mute_button["x"],
                                self.mute_button["sy"], self.mute_button["sx"])
        self.widgets["mute_button"] = mute_button

    def clicked_sound_on(self):
        """The actions that will happen when mute button is clicked (in order to play the music)"""
        self.widgets["mute_button"].deleteLater()
        self.widgets["mute_button"] = None
        self.widgets["mute_button"] = ""

        self.player.play()
        self.sound = True

        sound_on = self.create_mute_button("", self.clicked_mute_button, "sound_on.png", "mute.png", self.window)
        sound_on.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if self.rules is True:
            self.grid.addWidget(sound_on, self.rules_mute_button["y"], self.rules_mute_button["x"],
                                self.rules_mute_button["sy"], self.rules_mute_button["sx"])
        elif self.scores is True:
            self.grid.addWidget(sound_on, self.scores_mute_button["y"], self.scores_mute_button["x"],
                                self.scores_mute_button["sy"], self.scores_mute_button["sx"])
        else:
            self.grid.addWidget(sound_on, self.mute_button["y"], self.mute_button["x"],
                                self.mute_button["sy"], self.mute_button["sx"])
        self.widgets["sound_on"] = sound_on

    @staticmethod
    def create_mute_button(button_label, function, img_0, img_1, parent, margin_l=0, margin_r=0):
        """Sets the design for music button"""
        button = QPushButton(button_label, parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#460A1C';
            border-radius: 45px;
            color: '#460A1C';
            height: 90px;
            width : 90px;
            background-image: url(''' + img_0 + ');' +
            '''padding: 0px 0;
            margin-top: 0px}
            *:hover{
                background-image: url(''' + img_1 + ''')

            }
            '''
        )
        button.clicked.connect(function)
        return button

    def create_music_button(self, y, x, sy, sx):
        """Create the music button and add it to the grid"""
        if self.sound is True:
            sound_on = self.create_mute_button("", self.clicked_mute_button, "sound_on.png", "mute.png", self.window)
            sound_on.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(sound_on, y, x, sy, sx)
            self.widgets["sound_on"] = sound_on
        else:
            mute_button = self.create_mute_button("", self.clicked_sound_on, "mute.png", "sound_on.png", self.window)
            mute_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(mute_button, y, x, sy, sx)
            self.widgets["mute_button"] = mute_button

    def set_menu_buttons(self, button_list):
        """Sets all the buttons on the game menu page"""
        if self.widgets:
            self.clear_widget()
        for button in button_list:
            button_el = self.create_menu_button(button["name"], button["function"], button["img"],
                                                self.window, button["ml"], button["mr"])
            button_el.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button_el, button["y"], button["x"], button["sy"], button["sx"])
            self.widgets[button["name"]] = button_el

    def menu_background(self):
        """Sets all the widgets on menu page and adds the computer player to the data base if it is the case"""
        self.rules = False
        self.scores = False
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(menu.png);")
        self.set_grid()
        self.set_menu_buttons(self.menu_buttons)
        self.create_music_button(self.mute_button["y"], self.mute_button["x"],
                                 self.mute_button["sy"], self.mute_button["sx"])

        PlayerDB.add_computer_player()

    def add_error_label(self, text, key, y, x, sy, sx):
        """Sets the design for error labels"""
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            border: 4px solid '#460A1C';
            border-radius: 45px;
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

    def add_player(self, nickname):
        """Adds a new player to the data base"""
        add_player = PlayerDB.add_new_player(nickname)
        if add_player == -1:
            self.add_error_label("This player already exists", "player_already_exists", self.pl_al_exists["y"],
                                 self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
            QTimer.singleShot(1500, self.widgets["player_already_exists"].hide)

        if add_player == "Computer":
            self.add_error_label("You can't add this nickname", "Computer_nickname", self.pl_al_exists["y"],
                                 self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
            QTimer.singleShot(1500, self.widgets["Computer_nickname"].hide)

        self.select_player(self.sel_r["y"], self.sel_r["x"], self.sel_r["sy"], self.sel_r["sx"], "r")
        self.select_player(self.sel_l["y"], self.sel_l["x"], self.sel_l["sy"], self.sel_l["sx"], "l")
        self.widgets["lineedit"].clear()

    def create_line_edit(self, y, x, sy=1, sx=1):
        """Creates a line edit in order to be able to add new players to the game"""
        hbox = QHBoxLayout(self.window)
        lineedit = QLineEdit(self.window)
        lineedit.setStyleSheet("background-image: url(bluebackground.png); background-position: center;")
        lineedit.setPlaceholderText("Add player...")
        lineedit.setMaxLength(12)
        lineedit.returnPressed.connect(lambda: self.add_player(lineedit.text()))
        self.window.setLayout(hbox)
        self.grid.addWidget(lineedit, y, x, sy, sx)
        self.widgets["lineedit"] = lineedit

    def clicked_del_button(self):
        """The actions that will happen when delete player button is clicked"""
        if self.selected_player[0] == "":
            return

        if self.selected_player[0] == "Computer":
            self.add_error_label("You can't detele this player", "del_computer", self.pl_al_exists["y"],
                                 self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
            QtTest.QTest.qWait(1500)
            self.widgets["del_computer"].hide()
            return

        if self.right_chosen_players and self.left_chosen_players:
            if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                self.widgets["hidden_play_button"].hide()

        PlayerDB.delete_player(self.selected_player[0])
        self.select_player(self.sel_r["y"], self.sel_r["x"], self.sel_r["sy"], self.sel_r["sx"], "r")
        self.select_player(self.sel_l["y"], self.sel_l["x"], self.sel_l["sy"], self.sel_l["sx"], "l")
        location = self.selected_player[1]

        if self.right_chosen_players and self.left_chosen_players:
            if self.right_chosen_players == self.left_chosen_players:
                if location == "l":
                    self.widgets["right_label"].deleteLater()
                    self.widgets["right_label"] = None
                    self.widgets.pop("right_label")
                    self.right_chosen_players = ""

                if location == "r":
                    self.widgets["left_label"].deleteLater()
                    self.widgets["left_label"] = None
                    self.widgets.pop("left_label")
                    self.left_chosen_players = ""

                if "different_player" in self.widgets.keys():
                    self.widgets["different_player"].hide()

        if location == "r":
            self.widgets["right_label"].deleteLater()
            self.widgets["right_label"] = None
            self.widgets.pop("right_label")
            self.right_chosen_players = ""
        elif location == "l":
            self.widgets["left_label"].deleteLater()
            self.widgets["left_label"] = None
            self.widgets.pop("left_label")
            self.left_chosen_players = ""

        self.r_list.pop(self.selected_player[0])
        self.l_list.pop(self.selected_player[0])

    def del_player_button(self, y, x, sy=1, sx=1):
        """Sets the delete player button"""
        del_button = QPushButton("Delete selected player", self.window)
        del_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        del_button.setStyleSheet(
            '''
            color: '#138CFC';
            border-radius: 45px;
            height: 900px;
            width : 90px;
            font: bold 10px;
            font-family: 'Trebuchet MS';
            font-size: 20px;
            background-image: url(button_backgound.png);}
            '''
        )
        del_button.clicked.connect(self.clicked_del_button)
        self.grid.addWidget(del_button, y, x, sy, sx)
        self.widgets["del_button"] = del_button

    def add_pl_label(self, text, key, y, x, sy, sx):
        """Sets the design for player labels"""
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            border-radius: 45px;
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

    def selected_pl_r(self, item):
        """Actions that will happen if the player was selected from the right list"""
        nickname = QListWidgetItem(item).text()
        self.selected_player = nickname, "r"
        if "right_label" not in self.widgets.keys():
            self.add_pl_label(nickname, "right_label", self.player_r["y"], self.player_r["x"],
                              self.player_r["sy"], self.player_r["sx"])
        else:
            self.widgets["right_label"].deleteLater()
            self.widgets["right_label"] = None
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
                self.add_error_label("Please select a different player!", "different_player", self.pl_al_exists["y"],
                                     self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
                if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                    self.widgets["hidden_play_button"].hide()

    def selected_pl_l(self, item):
        """Actions that will happen if the player was selected from the left list"""
        nickname = QListWidgetItem(item).text()
        self.selected_player = nickname, "l"
        if "left_label" not in self.widgets.keys():
            self.add_pl_label(nickname, "left_label", self.player_l["y"], self.player_l["x"],
                              self.player_l["sy"], self.player_l["sx"])
        else:
            self.widgets["left_label"].deleteLater()
            self.widgets["left_label"] = None
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
                self.add_error_label("Please select a different player!", "different_player", self.pl_al_exists["y"],
                                     self.pl_al_exists["x"], self.pl_al_exists["sy"], self.pl_al_exists["sx"])
                if "hidden_play_button" in self.widgets.keys() and self.widgets["hidden_play_button"] is not None:
                    self.widgets["hidden_play_button"].hide()

    def select_player(self, y, x, sy, sx, location):
        """Add the players from the data base if any"""
        layout = QGridLayout(self.window)
        self.window.setLayout(layout)
        list_widget = QListWidget(self.window)

        list_widget.setStyleSheet("background-image: url(background.png); background-position: center;")

        player_list = PlayerDB.get_player_list()
        if len(player_list) > 0:
            for player in player_list:
                item = QListWidgetItem(player["name"])
                item.setFont(QFont('Trebuchet MS', 15))
                item.setForeground(Qt.darkRed)
                if location == "r":
                    self.r_list[player["name"]] = item
                    self.widgets["r_list"] = self.r_list
                    list_widget.addItem(item)
                elif location == "l":
                    if player["name"] != "Computer":
                        self.l_list[player["name"]] = item
                        self.widgets["l_list"] = self.l_list
                        list_widget.addItem(item)

        if location == "r":
            list_widget.itemClicked.connect(self.selected_pl_r)

        if location == "l":
            list_widget.itemClicked.connect(self.selected_pl_l)

        scroll_bar = QScrollBar(self.window)
        scroll_bar.setStyleSheet("background : #138CFC;")
        list_widget.setVerticalScrollBar(scroll_bar)

        self.grid.addWidget(list_widget, y, x, sy, sx)
        self.widgets["list_widget"] = list_widget

    def create_play_button(self, play_button, parent):
        """Sets the design for play button"""
        button = QPushButton(play_button["name"], parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            '''
            border-radius: 45px;
            height: 150px;
            width : 100px;
            background-image: url(hidden_play_button.png);
            '''
        )
        button.clicked.connect(play_button["function"])
        self.grid.addWidget(button, play_button["y"], play_button["x"], play_button["sy"], play_button["sx"])
        self.widgets["hidden_play_button"] = button
        button.hide()

    def choose_players(self):
        """The part of the application where you choose who with who will play, all the widgets are added to the grid"""
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

        self.create_music_button(self.mute_button["y"], self.mute_button["x"],
                                 self.mute_button["sy"], self.mute_button["sx"])

    def back_to_game(self):
        """Hides the widgets that represents the image with the rules and the specific back button"""
        self.widgets["rules_board"].hide()
        self.widgets["back_from_rules"].hide()

    def clicked_rules_board(self):
        """The actions that will happen when rules button is clicked when you are in the middle of the game"""
        label = QLabel("", self.window)
        pixmap = QPixmap('rules.png')
        label.setPixmap(pixmap)

        label.setAlignment(Qt.AlignCenter)

        self.grid.addWidget(label, self.rules_img["y"], self.rules_img["x"], self.rules_img["sy"], self.rules_img["sx"])
        self.widgets["rules_board"] = label

        back_button = self.create_menu_button("Back to game", self.back_to_game, "brick2.png", self.window)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_button, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_from_rules"] = back_button

    def clicked_leave_option(self, option):
        """Verifies what option you choose after Leave button was clicked"""
        if option.text() == "Cancel":
            pass
        if option.text() == "OK":
            self.game.restart()
            self.menu_background()

    def clicked_leave(self):
        """The actions that will happen when Leave button is clicked"""
        leave_msg = QMessageBox(self.window)
        leave_msg.setWindowTitle("Leave the game")
        leave_msg.setText("Are you sure you want to leave the game? \n All the progress will be lost!")
        leave_msg.setIcon(QMessageBox.Question)
        leave_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        leave_msg.setDefaultButton(QMessageBox.Cancel)

        leave_msg.buttonClicked.connect(self.clicked_leave_option)

        x = leave_msg.exec_()

        self.widgets["leave_msg"] = leave_msg

    @staticmethod
    def mancala_button(button_label, function, parent, margin_l=0, margin_r=0):
        """Sets the design for mancala holes buttons"""
        button = QPushButton(button_label, parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#251c13';
            border-radius: 45px;
            color: #c79869;
            font-family: 'shanti';
            font-size: 35px;
            height: 150px;
            width : 100px;
            background: transparent;
            padding: 0px 0;
            margin-top: 0px}
            *:hover{
                background: rgba(199, 152, 105, 90)

            }
            '''
        )
        button.clicked.connect(function)
        return button

    @staticmethod
    def hole_img(text, parent, margin_l=0, margin_r=0):
        """Sets the design for mancala holes images"""
        label = QLabel(text, parent)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#251c13';
            border-radius: 45px;
            color: #c79869;
            font-family: 'shanti';
            font-size: 35px;
            height: 150px;
            width : 100px;
            background: transparent;
            padding: 0px 0;
            margin-top: 0px}
            '''
        )
        label.setWordWrap(True)
        return label

    @staticmethod
    def bank_img(text, parent, margin_l=0, margin_r=0):
        """Sets the design for mancala banks"""
        label = QLabel(text, parent)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#251c13';
            border-radius: 45px;
            color: #c79869;
            font-family: 'shanti';
            font-size: 35px;
            height: 150px;
            width : 100px;
            background: transparent;
            padding: 0px 0;
            margin-top: 0px}
            '''
        )
        label.setWordWrap(True)
        return label

    @staticmethod
    def computer_selected_hole_img(text, parent, margin_l=0, margin_r=0):
        """Sets the design for mancala holes buttons when the computer selects it"""
        label = QLabel(text, parent)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "*{margin-left: " + str(margin_l) + "px;" +
            "margin-right: " + str(margin_r) + "px;" +
            '''
            border: 4px solid '#251c13';
            border-radius: 45px;
            color: #c79869;
            font-family: 'shanti';
            font-size: 35px;
            height: 150px;
            width : 100px;
            background: rgba(199, 152, 105, 90);
            padding: 0px 0;
            margin-top: 0px}
            '''
        )
        label.setWordWrap(True)
        return label

    def set_first_player_bank_img(self):
        """Sets the bank image for the first player"""
        if self.first_player_bank:
            self.first_player_bank.deleteLater()
            self.first_player_bank = None
            self.first_player_bank = ""

        x = self.f_pl_bank["x"]
        y = self.f_pl_bank["y"]
        sx = self.f_pl_bank["sx"]
        sy = self.f_pl_bank["sy"]
        label = self.bank_img(str(self.game.first_pl_bank[0]), self.window)
        self.grid.addWidget(label, y, x, sy, sx)
        self.first_player_bank = label

    def set_second_player_bank_img(self):
        """Sets the bank for the second player"""
        if self.second_player_bank:
            self.second_player_bank.deleteLater()
            self.second_player_bank = None
            self.second_player_bank = ""

        x = self.s_pl_bank["x"]
        y = self.s_pl_bank["y"]
        sx = self.s_pl_bank["sx"]
        sy = self.s_pl_bank["sy"]
        label = self.bank_img(str(self.game.second_pl_bank[0]), self.window)
        self.grid.addWidget(label, y, x, sy, sx)
        self.second_player_bank = label

    def set_first_player_side_img(self):
        """Sets the holes images for the first player"""
        if self.first_player_side_img:
            for i in range(6):
                self.first_player_side_img[i].deleteLater()
                self.first_player_side_img[i] = None
            self.first_player_side_img = {}

        if self.first_player_side_widgets:
            for i in range(6):
                self.first_player_side_widgets[i].deleteLater()
                self.first_player_side_widgets[i] = None
            self.first_player_side_widgets = {}

        x = self.first_player_side["x"]
        for i in range(6):
            label = self.hole_img(str(self.game.first_pl_holes[i]), self.window)
            self.grid.addWidget(label, self.first_player_side["y"], x)
            self.first_player_side_img[i] = label
            x += 1

    def set_second_player_side_img(self):
        """Sets the holes images for the second player"""
        if self.second_player_side_img:
            for i in range(6):
                self.second_player_side_img[i].deleteLater()
                self.second_player_side_img[i] = None
            self.second_player_side_img = {}

        if self.second_player_side_widgets:
            for i in range(6):
                self.second_player_side_widgets[i].deleteLater()
                self.second_player_side_widgets[i] = None
            self.second_player_side_widgets = {}

        if self.computer_side:
            for i in range(6):
                self.computer_side[i].deleteLater()
                self.computer_side[i] = None
            self.computer_side = {}

        x = self.second_player_side["x"]
        for i in range(6):
            label = self.hole_img(str(self.game.second_pl_holes[i]), self.window)
            self.grid.addWidget(label, self.second_player_side["y"], x)
            self.second_player_side_img[i] = label
            x -= 1

    def set_computer_side(self):
        """Sets the holes images for the computer player, when the computer selected a hole"""
        if self.computer_side:
            for i in range(6):
                self.computer_side[i].deleteLater()
                self.computer_side[i] = None
            self.computer_side = {}

        if self.second_player_side_img:
            for i in range(6):
                self.second_player_side_img[i].deleteLater()
                self.second_player_side_img[i] = None
            self.second_player_side_img = {}

        x = self.second_player_side["x"]
        for i in range(6):
            if i != self.computer_selected_hole:
                label = self.hole_img(str(self.game.second_pl_holes[i]), self.window)
                self.grid.addWidget(label, self.second_player_side["y"], x)
                self.computer_side[i] = label
                x -= 1
            else:
                label = self.computer_selected_hole_img(str(self.game.second_pl_holes[i]), self.window)
                self.grid.addWidget(label, self.second_player_side["y"], x)
                self.computer_side[i] = label
                x -= 1

    def selected_hole_first_player(self):
        """Choose what will happen after the first player selects a hole"""
        self.current_player = self.game.first_player
        temp = self.window.sender()
        for key, value in self.first_player_side_widgets.items():
            if value == temp:
                if self.game.second_player != "Computer":
                    new_board, next_player = self.game.move(self.game.first_player, key)
                    self.evaluate_board_multiplayer(new_board, next_player)
                else:
                    self.game.move(self.game.first_player, key)

    def set_first_player_side(self):
        """Sets the buttons for board holes for the first player"""
        if self.first_player_side_widgets:
            for i in range(6):
                self.first_player_side_widgets[i].deleteLater()
                self.first_player_side_widgets[i] = None
            self.first_player_side_widgets = {}

        if self.first_player_side_img:
            for i in range(6):
                self.first_player_side_img[i].deleteLater()
                self.first_player_side_img[i] = None
            self.first_player_side_img = {}

        x = self.first_player_side["x"]
        for i in range(6):
            button = self.mancala_button(str(self.game.first_pl_holes[i]), self.selected_hole_first_player, self.window)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button, self.first_player_side["y"], x)
            self.first_player_side_widgets[i] = button
            x += 1

    def selected_hole_second_player(self):
        """Choose what will happen after the second player selects a hole"""
        self.current_player = self.game.second_player
        temp = self.window.sender()
        for key, value in self.second_player_side_widgets.items():
            if value == temp:
                new_board, next_player = self.game.move(self.game.second_player, key)
                self.evaluate_board_multiplayer(new_board, next_player)

    def set_second_player_side(self):
        """Sets the buttons for board holes for the second player"""
        if self.second_player_side_widgets:
            for i in range(6):
                self.second_player_side_widgets[i].deleteLater()
                self.second_player_side_widgets[i] = None
            self.second_player_side_widgets = {}

        if self.second_player_side_img:
            for i in range(6):
                self.second_player_side_img[i].deleteLater()
                self.second_player_side_img[i] = None
            self.second_player_side_img = {}

        x = self.second_player_side["x"]
        for i in range(6):
            button = self.mancala_button(str(self.game.second_pl_holes[i]), self.selected_hole_second_player,
                                         self.window)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.grid.addWidget(button, self.second_player_side["y"], x)
            self.second_player_side_widgets[i] = button
            x -= 1

    def evaluate_board_singleplayer(self, new_board, next_player):
        """Updates the images/ buttons of the board if you are playing with the computer"""
        if not new_board and not next_player:
            self.set_first_player_side_img()
            self.set_second_player_side_img()
            self.set_first_player_bank_img()
            self.set_second_player_bank_img()
            QtTest.QTest.qWait(2000)
            self.end_game()
        if new_board and next_player:
            # if is the first player turn
            if self.current_player == self.game.first_player:
                # if the current player has an extra moves
                if self.current_player == next_player:
                    self.set_first_player_side()
                    self.set_first_player_bank_img()
                # if the current player has no an extra moves
                else:
                    self.widgets["second_player"].show()
                    self.widgets["first_player"].hide()
                    self.set_first_player_side_img()
                    self.set_second_player_side_img()
                    self.set_first_player_bank_img()
                    QtTest.QTest.qWait(2000)
            # if is the computer's turn
            else:
                # if the current player has an extra moves
                if self.current_player == next_player:
                    self.set_second_player_side_img()
                    self.set_second_player_bank_img()
                    QtTest.QTest.qWait(2000)
                # if the current player has no an extra moves
                else:
                    self.widgets["first_player"].show()
                    self.widgets["second_player"].hide()
                    self.set_first_player_side()
                    self.set_second_player_side_img()
                    self.set_second_player_bank_img()

    def evaluate_board_multiplayer(self, new_board, next_player):
        """Updates the images/ buttons of the board if the players are humans"""
        if not new_board and not next_player:
            self.set_first_player_side_img()
            self.set_second_player_side_img()
            self.set_first_player_bank_img()
            self.set_second_player_bank_img()
            QtTest.QTest.qWait(2000)
            self.end_game()
        if new_board and next_player:

            self.set_first_player_bank_img()
            self.set_second_player_bank_img()
            # if the current player has no an extra moves
            if self.current_player != next_player:
                if self.current_player == self.game.first_player:
                    self.widgets["second_player"].show()
                    self.widgets["first_player"].hide()
                    self.set_second_player_side()
                    self.set_first_player_side_img()
                else:
                    self.widgets["first_player"].show()
                    self.widgets["second_player"].hide()
                    self.set_first_player_side()
                    self.set_second_player_side_img()
            # if the current player has an extra moves
            else:
                if self.current_player == self.game.first_player:
                    self.widgets["first_player"].show()
                    self.widgets["second_player"].hide()
                    self.set_first_player_side()
                    self.set_second_player_side_img()
                else:
                    self.widgets["second_player"].show()
                    self.widgets["first_player"].hide()
                    self.set_second_player_side()
                    self.set_first_player_side_img()

    def board(self):
        """The part of the application with the actual game"""
        temp_l = self.left_chosen_players
        temp_r = self.right_chosen_players
        self.clear_widget()
        self.window.setStyleSheet("background-image: url(board.png);")

        self.left_chosen_players = temp_l
        self.right_chosen_players = temp_r

        first_player, second_player = self.game.choose_first_player([self.left_chosen_players,
                                                                     self.right_chosen_players])

        self.set_first_player_side()
        self.set_second_player_side_img()
        self.set_first_player_bank_img()
        self.set_second_player_bank_img()

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

        self.create_music_button(self.mute_button["y"], self.mute_button["x"],
                                 self.mute_button["sy"], self.mute_button["sx"])

    def add_label(self, text, key, y, x, sy, sx):
        """Sets the design for the labels that shows the players and their total wins"""
        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            '''
            color: '#138CFC';
            border-radius: 45px;
            height: 150px;
            width : 100px;
            font: bold 10px;
            font-family: 'Trebuchet MS';
            font-size: 20px;
            background: rgba(70, 10, 28, 200);
            padding: 0px 0;
            margin-top: 0px
            '''
        )
        self.grid.addWidget(label, y, x, sy, sx)
        label.setWordWrap(True)
        self.widgets[key] = label

    def end_game(self):
        """The part of the application that shows the result of the game"""
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

        else:
            players_list = PlayerDB.get_player_list()
            for player in players_list:
                if player["name"] == winner:
                    winner_wins = player["wins"] + 1
                if player["name"] == loser:
                    loser_wins = player["wins"]

            self.window.setStyleSheet("background-image: url(not_tie.png);")
            self.add_label("The Winner is: " + str(winner), "winner", self.winner["y"], self.winner["x"],
                           self.winner["sy"], self.winner["sx"])

            self.add_label(str(winner) + " total wins: " + str(winner_wins), "winner_wins",
                           self.winner_w["y"], self.winner_w["x"], self.winner_w["sy"], self.winner_w["sx"])
            self.add_label(str(loser) + " total wins: " + str(loser_wins), "loser_wins",
                           self.loser_w["y"], self.loser_w["x"], self.loser_w["sy"], self.loser_w["sx"])
            PlayerDB.save_wins(winner)

        play_again = self.create_menu_button("Play again", self.choose_players, "background.png", self.window)
        play_again.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(play_again, self.play_again["y"], self.play_again["x"], self.play_again["sy"],
                            self.play_again["sx"])
        self.widgets["play_again"] = play_again

        back_to_menu = self.create_menu_button("Back to menu", self.menu_background, "background.png", self.window)
        back_to_menu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(back_to_menu, self.back_button["y"], self.back_button["x"], self.back_button["sy"],
                            self.back_button["sx"])
        self.widgets["back_to_menu"] = back_to_menu

        self.create_music_button(self.mute_button["y"], self.mute_button["x"],
                                 self.mute_button["sy"], self.mute_button["sx"])


class Game:
    def __init__(self, main_interface):
        self.interface = main_interface
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
        """Resets the values for the board"""
        self.first_pl_holes = [4, 4, 4, 4, 4, 4]
        self.first_pl_bank = [0]
        self.second_pl_holes = [4, 4, 4, 4, 4, 4]
        self.second_pl_bank = [0]
        self.first_player_turn = [self.first_pl_bank, self.second_pl_holes, self.first_pl_holes]
        self.second_player_turn = [self.second_pl_bank, self.first_pl_holes, self.second_pl_holes]
        self.loop_game = True
        self.first_player = ""
        self.second_player = ""

    def choose_first_player(self, players_list):
        """Choose who will be the first/ second player"""
        if not self.first_game:
            self.restart()
        if players_list[0] == "Computer" or players_list[1] == "Computer":
            # the Computer will always be the second player
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
        """Verifies if the players holes are empty, or if a player side is empty"""
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
            single_side_clear = first_pl_holes_state ^ second_pl_holes_state
            if single_side_clear:
                self.interface.set_first_player_side_img()
                self.interface.set_second_player_side_img()
                self.interface.set_first_player_bank_img()
                self.interface.set_second_player_bank_img()
                QtTest.QTest.qWait(2000)
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
        """Choose a random move for the Computer"""
        self.interface.current_player = "Computer"
        extra_move = False
        rocks = 0
        hole = -1
        while not rocks:
            holes = [0, 1, 2, 3, 4, 5]
            hole = random.choice(holes)
            self.interface.computer_selected_hole = hole
            rocks = self.second_pl_holes[hole]
        self.interface.set_computer_side()
        QtTest.QTest.qWait(2000)
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

        if self.loop_game:
            if extra_move:
                self.interface.evaluate_board_singleplayer(turn, "Computer")
                self.computer_move()
            else:
                self.second_player_turn = turn
                self.interface.evaluate_board_singleplayer(turn, self.first_player)
        else:
            self.interface.evaluate_board_singleplayer([], "")

    def move(self, current_player, hole):
        """Calculates how the board will look after a hole was picked"""
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

        if self.loop_game:
            if self.second_player == "Computer":
                if extra_move:
                    self.interface.evaluate_board_singleplayer(turn, current_player)
                else:
                    self.interface.evaluate_board_singleplayer(turn, next_player)
                    self.computer_move()
            else:
                if extra_move:
                    return turn, current_player
                else:
                    return turn, next_player
        else:
            if self.second_player == "Computer":
                self.interface.evaluate_board_singleplayer([], "")
            else:
                return [], ""


if __name__ == "__main__":
    interface = Interface()
    interface.start_image()
    sys.exit(interface.app.exec())
