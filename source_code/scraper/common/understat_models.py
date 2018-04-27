# -*- coding: utf-8 -*-


class Performance(object):
    def __init__(self):
        """Player model class

        :rtype: object
        """
        self.apps = 0
        self.min = 0
        self.goals = 0
        self.assist = 0
        self.shots = None
        self.KP = None
        self.sh90 = None
        self.kp90 = None
        self.xG = None
        self.xA = None
        self.xG90 = None
        self.xA90 = None
        self.xAKP = None
        self.ShxG = None

    @property
    def __unicode__(self):
        string = 'Apps: ' + self.apps + '\n'
        string = string + 'Min: ' + str(self.min) + '\n'
        string = string + 'Goals: ' + str(self.goals) + '\n'
        string = string + 'Assist: ' + str(self.assist) + '\n'
        string = string + 'Shots: ' + str(self.shots) + '\n'
        string = string + 'KP: ' + str(self.KP) + '\n'
        string = string + 'Sh90: ' + str(self.sh90) + '\n'
        string = string + 'KP90: ' + str(self.kp90) + '\n'
        string = string + 'xG: ' + str(self.xG) + '\n'
        string = string + 'xA: ' + str(self.xA) + '\n'
        string = string + 'xG90: ' + str(self.xG90) + '\n'
        string = string + 'xA90: ' + str(self.xA90) + '\n'
        string = string + 'xAKP: ' + str(self.xAKP) + '\n'
        string = string + 'ShxG: ' + str(self.ShxG) + '\n'
        return string

class Player(object):
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.season = ''
        self.team = ''
        self.general = None
        self.performance_by_position = {}
        self.performance_by_situation = []
        self.performance_by_shot_zones = []
        self.performance_by_shot_types = []


class Team(object):
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.situation = []
        self.formation = []
        self.game_state = []
        self.timing = []
        self.shot_zones = []
        self.attack_speed = []
        self.result = []
